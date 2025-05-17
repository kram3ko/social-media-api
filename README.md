
# 📱 Social Media Django API

A RESTful API for a social media platform built with **Django**, supporting:

- User authentication & registration  
- Profiles, posts, comments, and likes  
- Follow/unfollow system  
- Fully documented Swagger/OpenAPI interface
- Docker Compose support
- Redis caching
- Celery for background tasks
- PostgreSQL database
- Django Rest Framework for API development
- Random post by celery beat with request to external API

---

## 📑 Table of Contents

- [📌 Description](#-description)  
- [🚀 Getting Started](#-getting-started)  
- [🔧 Migrations & Superuser](#-migrations--superuser)  
- [📚 API Documentation](#-api-documentation)  
- [📬 API Request Examples](#-api-request-examples)  
- [📁 Project Structure](#-project-structure)  
- [📨 Contact](#-contact)  

---

## 📌 Description

This project implements basic social network features:

- User registration and authentication  
- User profiles  
- Posts, likes, comments  
- User follows (follow/unfollow other users)  

---

## 🚀 Getting Started

### 🧰 Clone the repository

```bash
git clone git@github.com:kram3ko/social-media-api.git
cd <project-folder>
```

### 📦 Install dependencies (using uv)

```bash
pip install uv
uv sync
```

### 🐳 Docker Compose (alternative setup)

Build and run with Docker Compose:

```bash
docker-compose build
docker-compose up
```

---

## 🔧 Migrations & Superuser

### Apply migrations

```bash
python manage.py migrate
```

### Create a superuser

```bash
python manage.py createsuperuser
```

### Run the development server

```bash
python manage.py runserver
```

---

## 📚 API Documentation

Available after starting the server:

- **Swagger UI:** [http://localhost:8000/api/docs/](http://localhost:8000/api/docs/)  
- **OpenAPI Spec:** [http://localhost:8000/api/schema/](http://localhost:8000/api/schema/)  

Documentation includes schemas, descriptions, sample requests and responses for all endpoints.

---

## ⚙️ Set up environment variables

1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```
2. Update `.env` with your configuration values.

---


## 📨 Contact

Maintained by [Volodymyr Vynogradov](https://github.com/kram3ko)  
For any inquiries or issues, feel free to open an issue or pull request.

---
