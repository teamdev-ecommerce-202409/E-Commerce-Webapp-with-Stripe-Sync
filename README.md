# E-Commerce-Webapp-with-Stripe-Sync

## コンテナ起動手順

### .envファイルをPJディレクトリに作成
```
MYSQL_DB_NAME=＜アプリで使用するテーブルの名前＞
MYSQL_TEST_DB_NAME=test_＜アプリで使用するテーブルの名前＞
MYSQL_ROOT_PASSWORD=＜rootユーザーのパスワード＞
MYSQL_APP_USER=＜appユーザーの名前＞
MYSQL_APP_USER_PASSWORD=＜appユーザーのパスワード＞
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_ENGINE=django.db.backends.mysql
```

### dockerコマンドを実行
```
mkdir -p mysql/data
docker build -t django_mysql_image .
docker container run \
  --name django_mysql_container \
  -p 8081:8080 \
  -v /path/to/mysql/data:/var/lib/mysql \
  -v /path/to/src:/var/lib/mysql \
  django_mysql_image
```

### docker hubからイメージを取得して実行(後日作成)
```
docker pull genji1/XXXXXXXX
docker container run \
  --name django_mysql_container \
  -p 8081:8080 \
  -v /path/to/your/local/directory:/var/lib/mysql \
  genji1/XXXXXXXX
```
