from atproto import Client, models
from typing import List
import requests
from io import BytesIO
from atproto_client.models.app.bsky.embed.images import Main, Image

class BlueSkyClient:
    """
    クラス BlueSkyClient

    BlueSkyソーシャルメディア・プラットフォームとやり取りするためのクライアント。

    属性
        client (クライアント)： APIリクエストに使用するクライアントのインスタンス。

    メソッド
        __init__(self, email: str, password: str) -> None：
            BlueSkyClientクラスのインスタンスを初期化します。

        post_image(self, images: List[str], text: str) -> None：
            画像とテキストを含む新しい投稿を作成します。

        _to_embed(self, link_images: List[str]) -> Main：
            画像リンクのリストを埋め込みオブジェクトに変換する。

    """
    def __init__(self, email: str, password: str):
        """
        クラスのインスタンスを初期化します。

        引数
            email (str)： ユーザのメールアドレス。
            password (str)： ユーザーアカウントのパスワード。

        """
        self.client = Client(base_url='https://bsky.social')
        self.client.login(email, password)

    def post_image(self, images: List[str], text: str):
        """
        引数
            images (リスト[str])： 画像のURLまたはファイルパスのリスト。
            text (str)： 投稿に含まれるテキスト。

        """
        embed_images = self._to_embed(images)

        self.client.com.atproto.repo.create_record(
            models.ComAtprotoRepoCreateRecord.Data(
                repo=self.client.me.did,
                collection=models.ids.AppBskyFeedPost,
                record=models.AppBskyFeedPost.Main(
                    created_at=self.client.get_current_time_iso(),
                    text=text,
                    embed=embed_images,
                    langs=['ja']
                ),
            )
        )


    def _to_embed(self, link_images: List[str]) -> Main:
        """
         引数
             link_images (リスト[str])： 埋め込む画像リンクのリスト。

         戻り値
             Main: Mainオブジェクトに埋め込まれた画像。
         """
        images: List[Image] = []
        for image in link_images:
            # 画像を取得
            response = requests.get(image)

            # 画像をバイト形式に変換
            image_binary = BytesIO(response.content)
            upload = self.client.com.atproto.repo.upload_blob(image_binary)
            image = models.AppBskyEmbedImages.Image(alt='', image=upload.blob)
            images.append(image)
        return models.AppBskyEmbedImages.Main(images=images)