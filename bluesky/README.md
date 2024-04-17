# BlueSkyの自動投稿システム
[公式SDKドキュメント](https://docs.bsky.app/)

複数枚での画像投稿が公式のSDKではできなかったので、<br>
**SDKの中身のコードを解析して、複数枚アップロードを実現**した.

## 使い方
BlueSkyアカウントの作成
<br><br>
### 1. .envファイルの作成
```shell
cp .env.sample .env
```

### 2. .envファイルをログインメールアドレスとパスワードを設定する
```dotenv
LOGIN_EMAIL=
LOGIN_PASSWORD=
```

### 3. コンテナの起動
```shell
docker compose up -d
```

### 4. コンテナへ接続
```shell
docker compose exec python bash
```

### 5. 実行
```shell
python main.py
```

実際に投稿されたら成功

---