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


autorization:
{
  "username": "myusername",
  "password": "mypassword"
}

more information:
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJteXVzZXJuYW1lIn0.XI7omJww32ltJpU6JQ6vLasyxUmSAiDG1ZMWD6XDyGY",
  "token_type": "bearer"
}

----------TEST CURL-----------
-input:
curl -X 'POST' \
  'http://localhost:8000/notes/' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJteXVzZXJuYW1lIn0.XI7omJww32ltJpU6JQ6vLasyxUmSAiDG1ZMWD6XDyGY' \
  -H 'Content-Type: application/json' \
  -d '{
  "title": "Моя третья заметка",
  "content": "Ашибка на ашышбе"
}'
-output:
{
  "title": "Моя третья заметка",
  "content": "Ошибка на ошибке",
  "id": 3,
  "owner_id": 1
}

-input:
curl -X 'POST' \
  'http://localhost:8000/notes/' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJteXVzZXJuYW1lIn0.XI7omJww32ltJpU6JQ6vLasyxUmSAiDG1ZMWD6XDyGY' \
  -H 'Content-Type: application/json' \
  -d '{
  "title": "Моя третья заметка",
  "content": "Ват такай запрас я сделол"
}'
-output:
{
  "title": "Моя третья заметка",
  "content": "Вот такой запрос я сделал",
  "id": 4,
  "owner_id": 1
}
