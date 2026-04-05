from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.book import Book
from app.schemas.book import BookCreate, BookOut, BookUpdate

router = APIRouter(prefix="/books", tags=["books"])


def _get_book_or_404(book_id: int, db: Session) -> Book:
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book


@router.post("", response_model=BookOut, status_code=status.HTTP_201_CREATED)
def create_book(payload: BookCreate, db: Session = Depends(get_db)):
    existing = db.query(Book).filter(Book.isbn == payload.isbn).first()
    if existing:
        raise HTTPException(status_code=400, detail="ISBN already exists")

    available_copies = payload.available_copies
    if available_copies is None:
        available_copies = payload.total_copies
    if available_copies > payload.total_copies:
        raise HTTPException(status_code=400, detail="available_copies cannot exceed total_copies")

    book = Book(
        title=payload.title,
        author=payload.author,
        isbn=payload.isbn,
        published_year=payload.published_year,
        total_copies=payload.total_copies,
        available_copies=available_copies,
    )
    db.add(book)
    db.commit()
    db.refresh(book)
    return book


@router.get("", response_model=list[BookOut])
def list_books(db: Session = Depends(get_db)):
    return db.query(Book).order_by(Book.id.desc()).all()


@router.get("/{book_id}", response_model=BookOut)
def get_book(book_id: int, db: Session = Depends(get_db)):
    return _get_book_or_404(book_id, db)


@router.put("/{book_id}", response_model=BookOut)
def update_book(book_id: int, payload: BookUpdate, db: Session = Depends(get_db)):
    book = _get_book_or_404(book_id, db)

    if payload.isbn and payload.isbn != book.isbn:
        existing = db.query(Book).filter(Book.isbn == payload.isbn).first()
        if existing:
            raise HTTPException(status_code=400, detail="ISBN already exists")

    data = payload.model_dump(exclude_unset=True)
    future_total = data.get("total_copies", book.total_copies)
    future_available = data.get("available_copies", book.available_copies)
    if future_available > future_total:
        raise HTTPException(status_code=400, detail="available_copies cannot exceed total_copies")

    for key, value in data.items():
        setattr(book, key, value)

    db.commit()
    db.refresh(book)
    return book


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    book = _get_book_or_404(book_id, db)
    db.delete(book)
    db.commit()
    return None


@router.post("/{book_id}/borrow", response_model=BookOut)
def borrow_book(book_id: int, db: Session = Depends(get_db)):
    book = _get_book_or_404(book_id, db)
    if book.available_copies <= 0:
        raise HTTPException(status_code=400, detail="No available copies")

    book.available_copies -= 1
    db.commit()
    db.refresh(book)
    return book


@router.post("/{book_id}/return", response_model=BookOut)
def return_book(book_id: int, db: Session = Depends(get_db)):
    book = _get_book_or_404(book_id, db)
    if book.available_copies >= book.total_copies:
        raise HTTPException(status_code=400, detail="All copies are already in library")

    book.available_copies += 1
    db.commit()
    db.refresh(book)
    return book