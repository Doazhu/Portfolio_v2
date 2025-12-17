#!/bin/bash
set -e

echo "🚀 Deploying doazhu.pro..."

# Проверка .env файла
if [ ! -f .env ]; then
    echo "❌ Файл .env не найден! Скопируй .env.example в .env и заполни значения"
    exit 1
fi

# Проверка SSL сертификатов
if [ ! -f nginx/ssl/fullchain.pem ] || [ ! -f nginx/ssl/privkey.pem ]; then
    echo "❌ SSL сертификаты не найдены в nginx/ssl/"
    echo "   Положи туда fullchain.pem и privkey.pem от Timeweb"
    exit 1
fi

# Загрузка переменных
source .env

# Остановка старых контейнеров
echo "📦 Stopping old containers..."
docker compose -f docker-compose.prod.yml down

# Сборка и запуск
echo "🔨 Building and starting services..."
docker compose -f docker-compose.prod.yml build --no-cache
docker compose -f docker-compose.prod.yml up -d

# Проверка статуса
echo "✅ Checking services..."
sleep 5
docker compose -f docker-compose.prod.yml ps

echo ""
echo "🎉 Deployment complete!"
echo "   Site: https://doazhu.pro"
echo "   Admin: https://doazhu.pro/admin"
