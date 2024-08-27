until nc -z -v -w30 db 5432
do
  echo "Ждёмс connection..."
  sleep 1
done
uvicorn app.main:app --host 0.0.0.0 --port 8000
