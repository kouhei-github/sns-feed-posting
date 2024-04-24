aws ecr get-login-password --region ap-northeast-1 --profile  test | docker login --username AWS --password-stdin 471112763014.dkr.ecr.ap-northeast-1.amazonaws.com
docker build -t youtube-uploader .
docker tag youtube-uploader:latest 471112763014.dkr.ecr.ap-northeast-1.amazonaws.com/youtube-uploader:latest
docker push 471112763014.dkr.ecr.ap-northeast-1.amazonaws.com/youtube-uploader:latest
aws lambda update-function-code --function-name youtube_uploader --image-uri 471112763014.dkr.ecr.ap-northeast-1.amazonaws.com/youtube-uploader:latest --profile  test --region=ap-northeast-1 --no-cli-pager
