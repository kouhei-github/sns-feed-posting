# youtube_uploader
moviesのフォルダに格納したファイルをyoutubeにuploadするコード

# 注意点
・gcpでOath認証設定をしたあとにupload_video.pyと同じディレクトリに以下の形式のjsonファイルを作成
```json
{
  "web": {
    "client_id": "",
    "client_secret": "",
    "redirect_uris": [],
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://accounts.google.com/o/oauth2/token"
  }
}
```
・実行する際のコマンドは以下

```git bash
$ python upload_video.py --file="./movies/sample001.mp4" \
>                        --title="Sample Movie" \                 
>                        --description="This is a sample movie." \
>                        --category="22" \                        
>                        --privacyStatus="private"  

```
