# Build stage
FROM node:20-alpine AS build

WORKDIR /app

COPY package*.json ./
RUN npm ci --silent

COPY . .

# Переменные окружения для билда
ARG REACT_APP_API_URL=https://doazhu.pro
ENV REACT_APP_API_URL=$REACT_APP_API_URL

RUN npm run build

# Production stage
FROM nginx:alpine

# Копируем билд
COPY --from=build /app/build /usr/share/nginx/html

# Удаляем дефолтный конфиг (будет монтироваться извне для прода)
RUN rm -f /etc/nginx/conf.d/default.conf

EXPOSE 80 443

CMD ["nginx", "-g", "daemon off;"]
