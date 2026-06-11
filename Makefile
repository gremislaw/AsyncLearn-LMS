.PHONY: help install test lint format build up down restart logs clean migrate

help: ## Показать эту справку
	@echo "Доступные команды:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  [36m%-15s[0m %s
", $$1, $$2}'

install: ## Установка зависимостей
	@echo "Установка зависимостей бэкенда..."
	cd backend && pip install -r requirements.txt
	@echo "Установка зависимостей фронтенда..."
	cd frontend && npm install

test: ## Запуск тестов
	@echo "Запуск тестов бэкенда..."
	cd backend && python -m pytest tests/ -v --cov=app --cov-report=term-missing
	@echo "Запуск тестов фронтенда..."
	cd frontend && npm test -- --coverage --watchAll=false

lint: ## Проверка кода линтерами
	@echo "Проверка кода бэкенда..."
	cd backend && python -m flake8 app/ --max-line-length=120
	@echo "Проверка кода фронтенда..."
	cd frontend && npm run lint

format: ## Форматирование кода
	@echo "Форматирование кода бэкенда..."
	cd backend && python -m black app/
	@echo "Форматирование кода фронтенда..."
	cd frontend && npm run format

build: ## Сборка Docker образов
	docker-compose build

up: ## Запуск всех сервисов
	docker-compose up -d

down: ## Остановка всех сервисов
	docker-compose down

restart: ## Перезапуск всех сервисов
	docker-compose restart

logs: ## Просмотр логов
	docker-compose logs -f

clean: ## Очистка всех ресурсов
	docker-compose down -v
	docker system prune -f

migrate: ## Применение миграций базы данных
	cd backend && alembic upgrade head

migrate-create: ## Создание новой миграции
	cd backend && alembic revision --autogenerate -m "$(message)"

db-reset: ## Сброс и пересоздание базы данных
	docker-compose down -v
	docker-compose up -d postgres mongo redis kafka zookeeper rabbitmq
	@echo "Ожидание запуска баз данных..."
	@sleep 10
	cd backend && alembic upgrade head
	docker-compose up -d backend frontend
