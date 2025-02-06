# Stocks Products API

## Запуск контейнера

1. Создайте файл .env в корневой директории проекта и заполните его переменными окружения:
    SECRET_KEY=****
    DEBUG=****
    ALLOWED_HOSTS=****
2. Постройте образ:
   docker build -t stocks-products-api .
3. Запустите контейнер:
    docker run -d -p 8000:8000 --name stocks-products-container stocks-products-api
4. Откройте приложение в браузере:
    http://localhost:8000
5. Для работы с API используйте:
    http://localhost:8000/api/v1/
