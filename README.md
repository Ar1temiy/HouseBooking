# 🏠 HouseBooking

**Современная full-stack платформа для поиска, выбора и бронирования домов — быстро, прозрачно и удобно.**

<p align="left">
  <img alt="Python" src="https://img.shields.io/badge/Python-3.11%2B-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img alt="Vue" src="https://img.shields.io/badge/Vue-3.5-42b883?style=for-the-badge&logo=vuedotjs&logoColor=white" />
</p>

---

## 🎬 Screenshot / Demo

![Screenshot](docs/demoapi.png)

🔗 **Live Demo:** [https://your-demo-link.example.com](https://your-demo-link.example.com)

> Добавьте актуальный GIF или скриншот интерфейса в `docs/screenshot.png`, чтобы сразу показать UX проекта новым пользователям.

---

## 📖 Overview

**HouseBooking** — это веб-приложение для бронирования домов и объектов размещения с понятным пользовательским интерфейсом и API-first архитектурой.

---

## ✨ Features

- 🏘️ Просмотр каталога домов с быстрым доступом к карточке каждого объекта.
- 📅 Проверка доступности по датам через отдельный endpoint занятых интервалов.
- 🔐 JWT-аутентификация: регистрация и вход с выдачей access token.
- 👤 Личный кабинет пользователя с просмотром собственных бронирований.
- 🧾 Создание и отмена бронирований пользователем.
- 🛡️ Ролевая модель (client/admin) для разделения пользовательских и админских прав.
- 🧑‍💼 Админ-функции: создание, редактирование и удаление домов.
- ✅ Админ-модерация бронирований (подтверждение/отмена).
- 📡 REST API с OpenAPI/Swagger-документацией «из коробки».
- 📱 Адаптивный интерфейс на Vue 3 для комфортного использования с разных устройств.
- ⚡ Быстрый DX: Vite для фронтенда и Uvicorn для запуска API.

---

## 🛠️ Tech Stack

| Layer | Technologies |
|---|---|
| **Frontend** | ![Vue](https://img.shields.io/badge/Vue-3-42b883?logo=vuedotjs&logoColor=white) ![Vite](https://img.shields.io/badge/Vite-7-646CFF?logo=vite&logoColor=white) ![Vue Router](https://img.shields.io/badge/Vue_Router-5-4FC08D?logo=vuedotjs&logoColor=white) ![Axios](https://img.shields.io/badge/Axios-HTTP-5A29E4?logo=axios&logoColor=white) |
| **Backend** | ![FastAPI](https://img.shields.io/badge/FastAPI-0.128-009688?logo=fastapi&logoColor=white) ![Uvicorn](https://img.shields.io/badge/Uvicorn-ASGI-4051B5) ![Pydantic](https://img.shields.io/badge/Pydantic-v2-E92063) |
| **Database** | ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-4169E1?logo=postgresql&logoColor=white) ![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-D71F00) ![Alembic](https://img.shields.io/badge/Alembic-Migrations-222222) |
| **Auth & Security** | ![JWT](https://img.shields.io/badge/JWT-Bearer-000000?logo=jsonwebtokens&logoColor=white) Password Hashing |
| **Dev Tools** | ![Git](https://img.shields.io/badge/Git-Version_Control-F05032?logo=git&logoColor=white) ![npm](https://img.shields.io/badge/npm-Node_Package_Manager-CB3837?logo=npm&logoColor=white) |

---

## 🔐 Environment Variables

Ниже перечислены ключевые переменные окружения для backend и frontend.

| Variable | Scope | Description | Example |
|---|---|---|---|
| `DB_HOST` | Backend | Хост PostgreSQL | `localhost` |
| `DB_PORT` | Backend | Порт PostgreSQL | `5432` |
| `DB_USER` | Backend | Пользователь БД | `postgres` |
| `DB_PASS` | Backend | Пароль БД | `postgres` |
| `DB_NAME` | Backend | Имя базы данных | `housebooking` |
| `APP_NAME` | Backend | Название API в OpenAPI | `Houses Booking API` |
| `JWT_SECRET_KEY` | Backend | Секрет для подписи JWT | `super-secret-key` |
| `JWT_ALGORITHM` | Backend | Алгоритм JWT | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Backend | Время жизни access token | `30` |
| `VITE_API_URL` | Frontend | Базовый URL API | `http://127.0.0.1:8000/api` |

> ⚠️ Никогда не коммитьте реальные секреты в репозиторий. Используйте `.env` и менеджеры секретов в production.

---

## 📂 Project Structure

```text
HouseBooking/
├── backend/
│   ├── alembic/
│   │   └── versions/
│   ├── app/
│   │   ├── api/
│   │   │   ├── routes/
│   │   │   │   ├── auth.py
│   │   │   │   ├── bookings.py
│   │   │   │   ├── houses.py
│   │   │   │   └── users.py
│   │   │   ├── deps.py
│   │   │   └── routers.py
│   │   ├── core/
│   │   ├── crud/
│   │   ├── db/
│   │   ├── models/
│   │   ├── schemas/
│   │   └── main.py
│   ├── requirements.txt
│   └── alembic.ini
├── frontend/
│   └── frontend/
│       ├── src/
│       │   ├── api/
│       │   ├── components/
│       │   ├── router/
│       │   └── views/
│       ├── package.json
│       └── vite.config.js
├── docs/
│   ├── screenshot.png
│   └── swagger-placeholder.png
└── README.md
```

---

## 📡 API Documentation

FastAPI автоматически генерирует интерактивную документацию API:

- **Swagger UI:** `http://127.0.0.1:8000/docs`
- **ReDoc:** `http://127.0.0.1:8000/redoc`

В Swagger вы можете:

- просматривать схемы запросов/ответов;
- тестировать endpoint'ы прямо из браузера;
- авторизоваться через Bearer Token для защищённых ручек.

![Swagger UI Placeholder](docs/swagger-placeholder.png)

---

<p align="center">
  Сделано с ❤️ для сообщества разработчиков и будущих путешественников.
</p>
# 🏠 HouseBooking
