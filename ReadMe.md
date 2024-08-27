
# testKodeEducation

Это проект для управления заметками с использованием авторизации. Он включает создание, редактирование и удаление заметок, а также авторизацию пользователей.

## Структура проекта

```plaintext
testKodeEducation/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── routes/
│   │   ├── auth.py
│   │   ├── notes.py
│   ├── models.py
│   ├── schemas.py
│   ├── crud.py
│   ├── utils.py
│   ├── config.py
├── tests/
│   ├── __init__.py
│   ├── test_auth.py
│   ├── test_notes.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

### Основные компоненты

- **app/** - Основная директория приложения.
  - **routes/** - Маршруты для авторизации и работы с заметками.
  - **models.py** - Описание моделей данных.
  - **schemas.py** - Схемы данных для валидации.
  - **crud.py** - Функции для взаимодействия с базой данных.
  - **utils.py** - Вспомогательные утилиты.
  - **config.py** - Конфигурация приложения.
- **tests/** - Тесты для приложения.
  - **test_auth.py** - Тесты для авторизации.
  - **test_notes.py** - Тесты для работы с заметками.
- **Dockerfile** - Dockerfile для сборки образа приложения.
- **docker-compose.yml** - Конфигурация для Docker Compose.
- **requirements.txt** - Зависимости проекта.
- **README.md** - Текущий файл с описанием проекта.

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
  "title": "Моя третья заметка",
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

## Установка и запуск проекта

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
pytest tests/
```

## Контакты

Если у вас есть вопросы или предложения, свяжитесь со мной по электронной почте: `lighttolight228@gmail.com`.
