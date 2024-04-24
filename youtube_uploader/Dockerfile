FROM public.ecr.aws/lambda/python:3.11

# pipのアップデート
RUN pip install --upgrade pip

# pipでインストールしたいモジュールをrequirements.txtに記述しておいて、
# コンテナ内でpipにインストールさせる
# requirements.txtの書き方は[pip freeze]コマンドから参考に出来る
# アプリケーションコードをコンテナにコピー
COPY ./src ${LAMBDA_TASK_ROOT}
COPY ./requirements.txt ${LAMBDA_TASK_ROOT}
RUN pip install -r ${LAMBDA_TASK_ROOT}/requirements.txt

RUN yum install atk cups-libs gtk3 libXcomposite alsa-lib \
    libXcursor libXdamage libXext libXi libXrandr libXScrnSaver \
    libXtst pango at-spi2-atk libXt xorg-x11-server-Xvfb \
    xorg-x11-xauth dbus-glib dbus-glib-devel -y

# 言語設定
ENV LANGUAGE=ja

## ダウンロードしてきたブラウザとドライバを配置
#COPY --from=build /opt/chrome-linux /opt/chrome
#COPY --from=build /opt/chromedriver /opt/

COPY src/* /var/task
WORKDIR /var/task/

CMD [ "lambda_function.lambda_handler" ]