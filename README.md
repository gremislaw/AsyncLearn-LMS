# AsyncLearn LMS

Асинхронная платформа онлайн-обучения с видеоуроками, платежами и системой отслеживания прогресса.

## Архитектура проекта

Проект построен по принципу чистой архитектуры с использованием микросервисной архитектуры:

- **Backend**: FastAPI приложение с асинхронными эндпоинтами
- **Базы данных**: 
  - PostgreSQL для основного хранения данных
  - MongoDB для отслеживания прогресса
  - Redis для кэширования и очередей задач
- **Система сообщений**:
  - Kafka для email-уведомлений
  - RabbitMQ для конвертации видео
- **Фронтенд**: React админ-панель
- **Инфраструктура**: Docker, Kubernetes, мониторинг

## Технологический стек

- **Backend**: FastAPI, Pydantic v2, SQLAlchemy 2.0, AsyncIO
- **Базы данных**: PostgreSQL, MongoDB, Redis
- **Система сообщений**: Kafka, RabbitMQ
- **Фронтенд**: React
- **Инфраструктура**: Docker, Kubernetes, Helm
- **Мониторинг**: Prometheus, Grafana
- **CI/CD**: GitLab CI

## Быстрый старт

### Требования
- Docker и Docker Compose
- Docker Hub учетная запись (для сборки образов)

### Запуск проекта

1. Клонируйте репозиторий:
```bash
git clone https://github.com/your-username/async-learn-lms.git
cd async-learn-lms
```

2. Настройте переменные окружения:
```bash
cp .env.example .env
# Отредактируйте .env файл с вашими настройками
```

3. Запустите все сервисы:
```bash
docker-compose up --build
```

4. Проверьте работоспособность:
```bash
curl http://localhost:8000/health
```

## API Эндпоинты

### Аутентификация
```
POST /auth/register - Регистрация нового пользователя
POST /auth/login - Логин пользователя
GET /users/me - Получение информации о текущем пользователе
```

### Курсы
```
GET /courses - Получение списка курсов
POST /courses - Создание нового курса (только для admin)
GET /courses/{id} - Получение информации о курсе
GET /courses/{id}/lessons - Получение уроков курса
```

### Платежи
```
POST /courses/{id}/purchase - Покупка курса
```

### Прогресс
```
POST /progress/{lesson_id} - Обновление прогресса просмотра урока
GET /progress/{course_id} - Получение прогресса по курсу
```

### Администрирование
```
POST /admin/upload-video - Загрузка видео (только для admin)
```

### Системные
```
GET /health - Проверка состояния сервиса
```

## Примеры использования API

### Регистрация пользователя
```bash
curl -X POST "http://localhost:8000/auth/register" -H "Content-Type: application/json" -d '{"username": "testuser", "email": "test@example.com", "password": "strongpassword", "role": "student"}'
```

### Логин пользователя
```bash
curl -X POST "http://localhost:8000/auth/login" -H "Content-Type: application/json" -d '{"username": "testuser", "password": "strongpassword"}'
```

### Получение списка курсов
```bash
curl -X GET "http://localhost:8000/courses" -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### Покупка курса
```bash
curl -X POST "http://localhost:8000/courses/1/purchase" -H "Authorization: Bearer YOUR_JWT_TOKEN" -H "Content-Type: application/json" -d '{"payment_method": "mock"}'
```

## Тестирование

Для запуска тестов используйте:
```bash
docker-compose exec backend pytest
```

## Мониторинг

- Grafana доступен по адресу: http://localhost:3000
- Prometheus доступен по адресу: http://localhost:9090

## Скриншоты

### Админ-панель
![Админ-панель](https://via.placeholder.com/800x400?text=Admin+Dashboard+Screenshot)

### Тесты
![Тесты](https://via.placeholder.com/800x400?text=Tests+Screenshot)

### Grafana
![Grafana](https://via.placeholder.com/800x400?text=Grafana+Dashboard+Screenshot)

## Лицензия

MIT License
