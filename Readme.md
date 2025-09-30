<h3>Тестовый проект FastAPI + PostgreSQL + Alembic + Docker + Docker Compose<h3>

<p>О чем, что делает:
Изначально - сервис для создания тасок, изменение их статуса, 
crud операции над тасками и пользователями. 
Позже был подкручен выпуск jwt, перевыпуск access по refresh, авторизация на нужных endpoint по jwt. 
Также, подключена работа с файлами, возможность загрузки на сервер, выгрузки (в том числе чанками в стриминговом потоке, а так же фоновой асинхронной задачей)
</p>

Используемый стек:
- Python
  - FastAPI (version 0.116.1) (async)
  - Alembic (version 1.16.5)
  - SQLAlchemy (version 2.0.41) (orm, async)
  - Aiofiles (version 24.1.0)
  - PyJWT (version 2.9.0)
- PostgreSQL
- Docker
- Docker Compose 

<h3>Установка и запуск</h3>
> DOCKER COMPOSE
```
docker compose up -d --build
docker compose exec app alembic upgrade head
```
