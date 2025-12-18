#!/bin/bash
set -e

echo "🚀 Deploying doazhu.pro..."

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
