from make_container import InstagramAPI 
import os

insta_business_id = os.environ.get('INSTA_BUSINESS_ID')
access_token = os.environ.get('TOKEN')

def lambda_handler(event, context):
    # eventから必要な情報を取得
    media_urls = event['media_urls']
    
    return {'statusCode': 200, 'body': content_publish_api(media_urls)}

# ステップ③: ステップ②のグループ化コンテナIDをを使って投稿
"""
Instagram上でコンテンツを公開するプロセスを処理する機能。
InstagramAPI クラスと対話して、提供されたメディア URL に基づいてさまざまなタイプのコンテナを作成します。
次に、コンテナーの検証を待ち、コンテンツを公開するための API リクエストを作成します。
成功した場合は応答を返し、そうでない場合は、プロセス中に発生した例外を処理して出力します。
"""
def content_publish_api(media_urls):
    make_contena_api = InstagramAPI(insta_business_id, access_token)
    
    # ステップ②関数（グループコンテナIDを作成）
    print("Content Publish API Result:")
    if len(media_urls) == 1 and media_urls[0]['type'] == 'IMAGE':
        postData = make_contena_api.make_image_container_api(media_urls[0]['media_url'], "#Awesome")
        
    elif len(media_urls) == 1 and media_urls[0]['type'] == 'VIDEO':
        postData = make_contena_api.make_reel_container_api(media_urls[0]['media_url'])
        
    elif len(media_urls) > 1:
        print("Content Publish API Result: make_carousel_container_api")
        postData = make_contena_api.make_carousel_container_api(media_urls, "#Awesome")
        
    elif len(media_urls) == 1 and media_urls[0]['type'] == 'STORIES':
        postData = make_contena_api.make_image_story_container_api(media_urls[0]['media_url'])
        
    elif len(media_urls) == 1 and media_urls[0]['type'] == 'REELS':
        postData = make_contena_api.make_reel_container_api(media_urls[0]['media_url'])

    if not postData:
        return None
    
    #Waiting for instagram container validation
    make_contena_api.wait_validation_container(postData['creation_id'])
    
    url = f'https://graph.facebook.com/v17.0/{insta_business_id}/media_publish?'
    response = make_contena_api.make_api_request(url, 'POST', postData)
    
    try:
        return response
    except Exception as e:
        print('Instagram APIのレスポンスの解析中にエラーが発生しました:', e)
        return None

# サンプル投稿用の画像と動画の配列
sample_media_urls = [
    {
        'media_url': 'https://picsum.photos/200/300.jpg',
        'type': 'IMAGE'
    },
    {
        'media_url': 'https://picsum.photos/200/300.jpg',
        'type': 'IMAGE'
    },
    {
        'media_url': 'https://static.videezy.com/system/resources/previews/000/014/045/original/30_seconds_digital_clock_display_of_sixteen_segments.mp4',
        'type': 'VIDEO'
    }
]

# 実行例
if __name__ == "__main__":
    print("Content Publish API Result:", content_publish_api(sample_media_urls))
