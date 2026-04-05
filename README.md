# Library Books API (No Docker, No MongoDB)

Backend project nho gon quan ly sach thu vien voi FastAPI + SQLite.

## 1) Tao virtual environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

## 2) Cai dependencies

```powershell
pip install -r requirements.txt
```

## 3) Chay server

```powershell
uvicorn app.main:app --reload
```

Mo:
- API root: http://127.0.0.1:8000/
- Swagger docs: http://127.0.0.1:8000/docs
- Health check: http://127.0.0.1:8000/health

## Cau truc

```text
app/
  core/config.py
  db/database.py
  models/book.py
  schemas/book.py
  routers/health.py
  routers/books.py
  main.py
```

## Endpoints mau

- GET `/`
- GET `/health`
- POST `/books`
- GET `/books`
- GET `/books/{book_id}`
- PUT `/books/{book_id}`
- DELETE `/books/{book_id}`
- POST `/books/{book_id}/borrow`
- POST `/books/{book_id}/return`
