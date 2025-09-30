<h3>Тестовый проект FastAPI + PostgreSQL + Alembic + Docker + Docker Compose</h3>

<h5>О чем, что делает:</h5>
Изначально - сервис для создания тасок, изменение их статуса, 
crud операции над тасками и пользователями. <br>
Позже был подкручен выпуск jwt, перевыпуск access по refresh, авторизация на нужных endpoint по jwt. <br>
Также, подключена работа с файлами, возможность загрузки на сервер, выгрузки (в том числе чанками в стриминговом потоке, а так же фоновой асинхронной задачей)


<h5>Используемый стек:</h5>
- Python
  - FastAPI (version 0.116.1) (async)
  - Alembic (version 1.16.5)
  - SQLAlchemy (version 2.0.41) (orm, async)
  - Aiofiles (version 24.1.0)
  - PyJWT (version 2.9.0)
- PostgreSQL
- Docker
- Docker Compose 

<h5>Установка и запуск</h5>
> DOCKER COMPOSE<br>
```sh
docker compose up -d --build<br>
docker compose exec app alembic upgrade head}
```
