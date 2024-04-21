# Hammer referrals

## Описание
Приложение для Django REST Framework, реализующее функционал реферальной системы
и авторизации пользователей по номеру телефона.

Ссылка на развернутый проект - `https://pleasehiretony.bounceme.net/api/`

Приложение не содержит в себе фронтенд-версии и представляет набор доступных
эндпоинтов API.

***

Использованный стек технологий:
- Python
- PostgreSQL
- Django
- Drango REST Framework
- Docker
- Nginx/Gunicorn

Сторонние библиотеки:
- django-phonenumber-field

***

## Установка
1. Склонируйте репозиторий на сервер

```
git clone git@github.com:R4zeel/django-referral-system.git
```

2. Перейдите в директорию ../django-referral-system/infra и создайте там
файл `.env` с параметрами окружения

```
POSTGRES_USER=<username>
POSTGRES_PASSWORD=<password>
POSTGRES_DB=django
DB_HOST=db
DB_PORT=5432
SECRET_KEY=<django-secret-key>
ALLOWED_HOSTS=<hosts>
```

3. Находясь в той же директории запустите контейнеры командой:

```
sudo docker compose up -d
```

3. Примените миграции и склонируйте статические файлы для бэкенда командами:

```
sudo docker compose -f docker-compose.production.yml exec backend python manage.py migrate
sudo docker compose -f docker-compose.production.yml exec backend python manage.py collectstatic
```

## Список доступных запросов

### Список всех пользователей
При вызове профиля пользователя также отображаются люди, использовавшие реферральный код
этого пользователя.

GET `http://127.0.0.1:8000/api/users/`.

### Профиль пользователя
GET `http://127.0.0.1:8000/api/users/<user_id>/`.

### Авторизация
В приложении используется авторизация по номеру телефона: 
1. Пользователь вводит номер телефона и получает код подтверждения
2. Пользователь вводит код и подтверждает свой телефон
3. Пользователю присваевается токен авторизации

В проекте нет интеграции с операторами мобильных данных, поэтому код приходит
в ответе на запрос, а не через SMS.

Получение кода подтверждения: 
POST запрос, должен содержать номер телефона.
 `http://127.0.0.1:8000/api/users/get_verify_code/`

Подтверждение номера телефона и получение токена: 
POST запрос, должен содержать номер телефона и код подтверждения.
`http://127.0.0.1:8000/api/users/auth/`

### Ввод реферального кода
POST запрос, должен содержать реферальный код, предоставленный другим пользователем.
Доступно только авторизированным пользователям.
`http://127.0.0.1:8000/api/referrals/referral_code/`