
## 🚀 Production Deploy (doazhu.pro)

### Быстрый деплой

```bash
# 1. Создай .env файл
cp .env.example .env
nano .env  # Заполни DB_PASSWORD, ADMIN_PASSWORD, SECRET_KEY

# 2. Положи SSL сертификаты от Timeweb
cp /path/to/fullchain.pem nginx/ssl/
cp /path/to/privkey.pem nginx/ssl/

# 3. Запусти деплой
./deploy.sh
```

### Переменные окружения (.env)
```env
DB_PASSWORD=your_secure_db_password
ADMIN_USERNAME=admin
ADMIN_PASSWORD=your_secure_admin_password
SECRET_KEY=openssl_rand_hex_32_output
```

### Структура деплоя
- **nginx** — reverse proxy + SSL + статика фронтенда
- **backend** — FastAPI на Gunicorn
- **db** — PostgreSQL 16

---

## Backend

---

### 💻 Local Development

```bash
cd backend
pip install -r requirements.txt

# Redis
docker run -d -p 6379:6379 redis:alpine

# Dev server (SQLite)
DEBUG=true uvicorn main:app --reload
```

---

### 🔐 Админка

| Env | URL |
|-----|-----|
| Dev | http://localhost:8000/admin |
| Prod | https://doazhu.pro/admin |

Логин/пароль задаются через `ADMIN_USERNAME` / `ADMIN_PASSWORD`

---

### 📊 Модели

| Модель | Поля |
|--------|------|
| Project | title, description, image_url, github_url, live_url, tech_stack, is_featured, order |
| Skill | name, category, level (%), icon, order |
| Message | name, email, subject, message, is_read |
| Settings | key, value, description |

---

### 🔗 API

| Метод | URL | Описание |
|-------|-----|----------|
| GET | `/health` | Health check |
| GET | `/api/projects` | Проекты (?featured_only=true) |
| GET | `/api/projects/{id}` | Один проект |
| GET | `/api/skills` | Навыки (?category=Frontend) |
| POST | `/api/contact` | Отправить сообщение |
| GET | `/api/settings/{key}` | Настройка |

---

### 📁 Структура

```
backend/
├── main.py          # FastAPI app + routes
├── models.py        # TortoiseORM модели
├── admin.py         # fastapi-admin views
├── config.py        # Pydantic Settings
├── init_admin.py    # CLI создания админа
├── Dockerfile
└── requirements.txt
```

---

## Frontend

Цветовая схема "Toxic Hazard"
--toxic-yellow: #CCFF00   /* Главный акцент */--neon-lemon: #FFF01F     /* Hover состояния */--void-black: #080808     /* Фон */--dark-graphite: #1A1A1A  /* Карточки/блоки */--light-gray: #E0E0E0     /* Текст */--medium-gray: #888888    /* Вторичный текст */

Шрифты (только 2!)
Sprite Graffiti (--font-heading) — заголовки h1/h2/h3
Montserrat (--font-body) — весь остальной текст

Ключевые моменты
Главная — Hero по центру + SpiralRibbon (SVG анимация рисования) + вторая секция Showcase со статистикой
Хедер — console.log("Hey, im Doazhu") с анимацией печати, используй max-width не width (баг при скролле)
Timeline — framer-motion whileInView для scroll-анимаций, точки позиционируются через right: -7px относительно карточек
Футер — SVG иконки инлайн (Telegram, GitHub, VK)

Контакты владельца
Email: me@doazhu.pro
Website: doazhu.pro
Telegram: @Doazhu
Статистика для Showcase
5 лет в разработке
119+ проектов
24/7 на связи

Частые проблемы
overflow: hidden на главной — нужен для спиральки, но только на .home-page контейнере
Шрифты: не добавлять третий шрифт, только Sprite Graffiti + Montserrat
Timeline: линия и точки — left: 50% для линии, точки через right/left: -7px от карточек