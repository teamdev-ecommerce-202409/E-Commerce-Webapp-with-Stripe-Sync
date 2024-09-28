# E-Commerce-Webapp-with-Stripe-Sync

## コンテナ起動手順

### docker hubからイメージを取得して実行(後日作成)
```
docker pull genji1/XXXXXXXX
docker container run \
  --name django_mysql_container \
  -p 8081:8080 \
  -v /path/to/your/local/directory:/var/lib/mysql \
  genji1/XXXXXXXX
```
