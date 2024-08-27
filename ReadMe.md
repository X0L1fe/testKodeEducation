
# testKodeEducation

## Содержание

- [Описание проекта](#описание-проекта)
- [Структура проекта](#структура-проекта)
- [Основные компоненты](#основные-компоненты)
- [Авторизация](#авторизация)
- [Примеры использования API](#примеры-использования-api)
  - [Создание заметки](#создание-заметки)
  - [Второй пример создания заметки](#второй-пример-создания-заметки)
- [Использование Postman](#использование-postman)
- [Установка и запуск проекта](#установка-и-запуск-проекта)
  - [Настройка готовой БД PostrgeSQL](#установка-базы-данных-PostrgeSQL)
  - [Установка зависимостей](#установка-зависимостей)
  - [Запуск приложения](#запуск-приложения)
  - [Запуск с использованием Docker](#запуск-с-использованием-docker)
- [Тестирование](#тестирование)
- [Контакты](#контакты)

## Описание проекта

Это проект для управления заметками с использованием авторизации. Он включает создание, редактирование и удаление заметок, а также авторизацию пользователей.

## Структура проекта

```plaintext
testKodeEducation/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── routes/
│   │   ├── auth.py
│   │   ├── misc.py
│   │   └── notes.py
│   ├── models.py
│   ├── schemas.py
│   ├── crud.py
│   ├── utils.py
│   ├── spellcheck.py
├── tests/
│   ├── __init__.py
│   ├── test_auth.py
│   └─ test_notes.txt
├── config.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── README.md
└──wait-db.sh
```

## Основные компоненты

- **app/** - Основная директория приложения.
  - **routes/** - Маршруты для авторизации и работы с заметками.
  - **auth.py** - Логика аунтефикации.
  - **crud.py** - Функции для взаимодействия с базой данных.
  - **database.py** - Инициализация базы данных.
  - **main.py** - Основной файл приложения для его запуска.
  - **models.py** - Описание моделей данных.
  - **schemas.py** - Схемы данных для валидации.
  - **spellcheck.py** - Интеграция с [ЯндексСпеллер](https://yandex.ru/dev/speller/).
  - **utils.py** - Вспомогательные утилиты.
- **tests/** - Тесты для приложения.
  - **test_auth.py** - Тесты для регистрации и авторизации.
  - **test_notes.txt** - Тесты для работы с заметками(переименуйте `.txt` в `.py`).
- **config.py** - Файл с константами базы данных для работы с Docker и локально.
- **docker-compose.yml** - Конфигурация для Docker Compose.
- **Dockerfile** - Dockerfile для сборки образа приложения.
- **pytest.ini** - Конфигрурация для PyTest.
- **README.md** - Текущий файл с описанием проекта.
- **requirements.txt** - Зависимости проекта.
- **wait-db.sh** - Цикличное подключение к базе данных в случае проблем.

## Авторизация

Пример запроса на авторизацию:

```json
{
  "username": "myusername",
  "password": "mypassword"
}
```

### Пример ответа:

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJteXVzZXJuYW1lIn0.XI7omJww32ltJpU6JQ6vLasyxUmSAiDG1ZMWD6XDyGY",
  "token_type": "bearer"
}
```

## Примеры использования API

### Создание заметки

- **Запрос:**

```bash
curl -X 'POST'   'http://localhost:8000/notes/'   -H 'accept: application/json'   -H 'Authorization: Bearer <ВАШ_ТОКЕН>'   -H 'Content-Type: application/json'   -d '{
  "title": "Моя третья заметка",
  "content": "Ашибка на ашышбе"
}'
```

- **Ответ:**

```json
{
  "title": "Моя заметка",
  "content": "Ошибка на ошибке",
  "id": 3,
  "owner_id": 1
}
```

### Второй пример создания заметки

- **Запрос:**

```bash
curl -X 'POST'   'http://localhost:8000/notes/'   -H 'accept: application/json'   -H 'Authorization: Bearer <ВАШ_ТОКЕН>'   -H 'Content-Type: application/json'   -d '{
  "title": "Моя третья заметка",
  "content": "Ват такай запрас я сделол"
}'
```

- **Ответ:**

```json
{
  "title": "Моя третья заметка",
  "content": "Вот такой запрос я сделал",
  "id": 4,
  "owner_id": 1
}
```

## Использование Postman

1. Импортируйте прилагаемую коллекцию Postman.
2. Используйте пример данных для входа:
   - **username**: `myusername`
   - **password**: `mypassword`
3. Запустите запрос на авторизацию для получения токена.
4. Скопируйте токен и используйте его в дальнейших запросах, добавляя его в заголовок `Authorization` как `Bearer <ВАШ_ТОКЕН>`.

## Использование Postman

### Шаг 1: Регистрация пользователя

1. Откройте Postman.
2. Создайте новый `POST` запрос к `http://localhost:8000/register`.
3. В `Body` выберите `raw` и `JSON`.
4. Введите данные для регистрации, например:

    ```json
    {
        "username": "myusername",
        "password": "mypassword"
    }
    ```
5. Нажмите `Send`. Если регистрация успешна, вы получите JSON с информацией о пользователе.

### Шаг 2: Получение токена

1. Создайте новый `POST` запрос к `http://localhost:8000/token`.
2. В `Body` выберите `x-www-form-urlencoded`.
3. Введите следующие параметры:
   - `username`: `myusername`
   - `password`: `mypassword`
4. Нажмите `Send`. Если аутентификация успешна, вы получите `access_token`.

### Шаг 3: Создание заметки

1. Создайте новый `POST` запрос к `http://localhost:8000/notes/`.
2. В `Headers` добавьте:
   - `Authorization`: `Bearer <ваш access_token>`
3. В `Body` выберите `raw` и `JSON`.
4. Введите данные для заметки, например:

    ```json
    {
        "title": "Моя заметка в Postman",
        "content": "Ашибка в Postman"
    }
    ```
5. Нажмите `Send`. Если заметка успешно создана, вы получите JSON с её данными.

### Шаг 4: Чтение заметок

1. Создайте новый `GET` запрос к `http://localhost:8000/notes/`.
2. В `Headers` добавьте:
   - `Authorization`: `Bearer <ваш access_token>`
3. Нажмите `Send`. Вы получите список заметок, созданных текущим пользователем.

## Установка и запуск проекта

### Настройка готовой БД PostrgeSQL 

Параметры сервера: 
- **host:** `127.0.0.1`
- **port:** `5432`
- **DB name:** `KodeEducation`

Инициализация БД:
1. После создания нажать ``ПКМ`` по `KodeEducation`
2. `Restore` и выбрать это [backup](https://github.com/X0L1fe/testKodeEducation/raw/main/KodeEducation_DB.sql)
3. Поздравляю! Теперь у вас есть мой backup базы данных

### Установка зависимостей

```bash
pip install -r requirements.txt
```

### Запуск приложения

```bash
uvicorn app.main:app --reload
```

### Запуск с использованием Docker

```bash
docker-compose up --build
```

## Тестирование

Для запуска тестов выполните:

```bash
pytest
```

## Контакты

Если у вас есть вопросы или предложения, свяжитесь со мной по:
- **Электронной почте:** `lighttolight228@gmail.com`;
- **Telegram:** [Inrigt](https://t.me/Inrigt)
