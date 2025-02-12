from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Настройка CORS для разрешения запросов с React

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://doazhu.ru", "https://doazhu.ru"],  
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/items")
