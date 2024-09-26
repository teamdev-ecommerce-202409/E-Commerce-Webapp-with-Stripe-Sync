#!/bin/bash

# すべてのコンテナを停止して削除
docker stop $(docker ps -aq)
docker rm $(docker ps -aq)

# すべてのイメージを削除
docker rmi $(docker images -q)

# すべてのボリュームを削除（ボリュームが存在する場合のみ）
volumes=$(docker volume ls -q)
if [ -n "$volumes" ]; then
    docker volume rm $volumes
fi

# すべてのネットワークを削除（デフォルトネットワークは除外）
networks=$(docker network ls -q | grep -v 'bridge\|host\|none')
if [ -n "$networks" ]; then
    docker network rm $networks
fi

# Dockerシステム全体のクリーンアップ
docker system prune -a --volumes -f

# ビルドキャッシュをクリア
docker builder prune -a -f

