import http.client  # httplibはPython3はhttp.clientへ移行
import httplib2
import os
import random
import sys
import time

from apiclient.discovery import build
from apiclient.errors import HttpError
from apiclient.http import MediaFileUpload
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow

import boto3
import urllib.parse
import uuid

import errno

import json

s3 = boto3.client('s3')

httplib2.RETRIES = 1
MAX_RETRIES = 10
RETRIABLE_EXCEPTIONS = (httplib2.HttpLib2Error,
                        IOError,
                        http.client.NotConnected,
                        http.client.IncompleteRead,
                        http.client.ImproperConnectionState,
                        http.client.CannotSendRequest,
                        http.client.CannotSendHeader,
                        http.client.ResponseNotReady,
                        http.client.BadStatusLine)
RETRIABLE_STATUS_CODES = [500, 502, 503, 504]
# CLIENT_SECRETS_FILE = "client_secrets.json"
CLIENT_SECRETS_FILE = './client_secrets.json'
MISSING_CLIENT_SECRETS_MESSAGE = """
WARNING: Please configure OAuth 2.0

To make this sample run you will need to populate the client_secrets.json file
found at:

   %s

with information from the API Console
https://console.developers.google.com/

For more information about the client_secrets.json file format, please visit:
https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
""" % os.path.abspath(os.path.join(os.path.dirname(__file__),
                                   CLIENT_SECRETS_FILE))

YOUTUBE_UPLOAD_SCOPE = "https://www.googleapis.com/auth/youtube.upload"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"


VALID_PRIVACY_STATUSES = ("public", "private", "unlisted")


def get_authenticated_service(args):
    flow = flow_from_clientsecrets(CLIENT_SECRETS_FILE,
                                   scope=YOUTUBE_UPLOAD_SCOPE,
                                   message=MISSING_CLIENT_SECRETS_MESSAGE)

    # storage = Storage("%s-oauth2.json" % sys.argv[0])
    storage = Storage("./bootstrap.py-oauth2.json")
    credentials = storage.get()

    if credentials is None or credentials.invalid:
        credentials = run_flow(flow, storage, args)

    return build(YOUTUBE_API_SERVICE_NAME,
                 YOUTUBE_API_VERSION,
                 http=credentials.authorize(httplib2.Http()))


def initialize_upload(youtube, options):
    tags = None
    if options.keywords:
        tags = options.keywords.split(",")

    body = dict(
        snippet=dict(
            title=options.title,
            description=options.description,
            tags=tags,
            categoryId=options.category
        ),
        status=dict(
            privacyStatus=options.privacyStatus
        )
    )

    insert_request = youtube.videos().insert(
        part=",".join(body.keys()),
        body=body,
        media_body=MediaFileUpload(options.file, chunksize=-1, resumable=True)
    )

    resumable_upload(insert_request)


def resumable_upload(insert_request):
    response = None
    error = None
    retry = 0
    while response is None:
        try:
            print("Uploading file...")  # print文
            status, response = insert_request.next_chunk()
            if response is not None:
                if 'id' in response:
                    print("Video id '%s' was successfully uploaded." % response['id'])
                else:
                    exit("The upload failed with an unexpected response: %s" % response)
        except HttpError as e:
            if e.resp.status in RETRIABLE_STATUS_CODES:
                error = "A retriable HTTP error %d occurred:\n%s" % \
                        (e.resp.status, e.content)
            else:
                raise
        except RETRIABLE_EXCEPTIONS as e:
            error = "A retriable error occurred: %s" % e
        if error is not None:
            print(error)
            retry += 1
            if retry > MAX_RETRIES:
              exit("No longer attempting to retry.")
            max_sleep = 2 ** retry
            sleep_seconds = random.random() * max_sleep
            print("Sleeping %f seconds and then retrying..." % sleep_seconds)
            time.sleep(sleep_seconds)

def lambda_handler(event, context):
    print(event)
    bodies = json.loads(event['body'])
    datas = bodies['data']

    for data in datas:
        # eventから必要な情報を取得
        s3_url = data['file_url']
        title = data['title']
        description = data['description']

        if 'win' not in sys.platform:
           # S3 URLからバケット名とオブジェクトキーを取り出す
            s3_info = urllib.parse.urlparse(s3_url)
            bucket = s3_info.netloc
            key = s3_info.path.lstrip('/')

            # S3から動画ファイルをダウンロード
            # S3から動画ファイルをダウンロードするための一時的なパスを作成します。
            tmp_dir = '/tmp/{}{}'.format(uuid.uuid4(), key)
            download_path = os.path.join(tmp_dir, os.path.basename(s3_url))

            # ディレクトリが存在しない場合は、ディレクトリを作成します。
            if not os.path.exists(os.path.dirname(download_path)):
                try:
                    os.makedirs(os.path.dirname(download_path))
                except OSError as exc:  # Guard against race condition
                    if exc.errno != errno.EEXIST:
                        raise

            # ファイルをダウンロードします。
            s3.download_file(bucket, key, download_path)
            video_path = os.path.join(tmp_dir, 'sample001.mp4')

        else:
            # ローカル環境の場合、動画のローカルパスを直接指定
            video_path = s3_url

        argparser.add_argument("--file", required=True, help="Video file to upload")
        argparser.add_argument("--title", help="Video title", default="Test Title")
        argparser.add_argument("--description",
                               help="Video description",
                               default="Test Description")
        argparser.add_argument("--category", default="22",
                               help="Numeric video category. " +
                                    "See https://developers.google.com/youtube/v3/docs/videoCategories/list")
        argparser.add_argument("--keywords", help="Video keywords, comma separated",
                               default="")
        argparser.add_argument("--privacyStatus", choices=VALID_PRIVACY_STATUSES,
                               default=VALID_PRIVACY_STATUSES[0],
                               help="Video privacy status.")
        args = argparser.parse_args([
            '--file', video_path,  # ここをvideo_pathに変更
            '--title', title,
            '--description', description,
            '--keywords', 'test',
            '--privacyStatus', 'public'
        ])

        if not os.path.exists(args.file):
            exit("Please specify a valid file using the --file= parameter.")

        youtube = get_authenticated_service(args)
        try:
            initialize_upload(youtube, args)
        except HttpError as e:
            print("An HTTP error %d occurred:\n%s" % (e.resp.status, e.content))

if __name__ == "__main__":
    lambda_handler(event =
    {
  "spreadId": "スプレッドシートID",
  "sheetName": "シート1",
  "data": [
    {
      "file_url": "./movies/sample001.mp4",
      "title": "LambdaTest",
      "description": "LambdaTestSucceed"
    }
  ]
}, context=None)

