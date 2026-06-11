FROM node:18-alpine

WORKDIR /app

# Копирование файла зависимостей
COPY package*.json ./

# Установка зависимостей
RUN npm install

# Копирование приложения
COPY . .

# Открываем порт
EXPOSE 3000

# Команда запуска
CMD ["npm", "start"]
