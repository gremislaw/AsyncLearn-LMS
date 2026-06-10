.PHONY: up down test logs

up:
	docker-compose up --build -d

down:
	docker-compose down -v

test:
	cd backend && pytest -v

logs:
	docker-compose logs -f backend
