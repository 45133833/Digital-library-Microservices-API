from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session
from pydantic import BaseModel
from typing import List, Optional
from .database import engine, create_db_and_tables, get_session
from .models import User, UserPublic, Author, AuthorPublic, Book, BookPublic, BookPublicWithDetails
from .crud import (
    create_user, get_users, get_user, update_user, delete_user,
    create_author, get_authors, get_author, update_author, delete_author,
    create_book, get_books, get_book_with_details, update_book, delete_book
)

app = FastAPI(
    title="Digital Library Microservices API",
    description="Books, Authors, Users with Relationships",
    version="1.0.0",
    docs_url="/docs"  # Swagger UI
)

# Dependency
def get_db():
    with Session(engine) as session:
        yield session

# Startup
@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# ==================== User Endpoints ====================
@app.post("/users", response_model=UserPublic)
def create_user_endpoint(user: User, db: Session = Depends(get_db)):
    return create_user(db, user)

@app.get("/users", response_model=List[UserPublic])
def get_users_endpoint(db: Session = Depends(get_db)):
    return get_users(db)

@app.get("/users/{user_id}", response_model=UserPublic)
def get_user_endpoint(user_id: int, db: Session = Depends(get_db)):
    user = get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.put("/users/{user_id}", response_model=UserPublic)
def update_user_endpoint(user_id: int, user: User, db: Session = Depends(get_db)):
    updated = update_user(db, user_id, user)
    if not updated:
        raise HTTPException(status_code=404, detail="User not found")
    return updated

@app.delete("/users/{user_id}")
def delete_user_endpoint(user_id: int, db: Session = Depends(get_db)):
    if not delete_user(db, user_id):
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}

# ==================== Author Endpoints ====================
@app.post("/authors", response_model=AuthorPublic)
def create_author_endpoint(author: Author, db: Session = Depends(get_db)):
    return create_author(db, author)

@app.get("/authors", response_model=List[AuthorPublic])
def get_authors_endpoint(db: Session = Depends(get_db)):
    return get_authors(db)

@app.get("/authors/{author_id}", response_model=AuthorPublic)
def get_author_endpoint(author_id: int, db: Session = Depends(get_db)):
    author = get_author(db, author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    return author

@app.put("/authors/{author_id}", response_model=AuthorPublic)
def update_author_endpoint(author_id: int, author: Author, db: Session = Depends(get_db)):
    updated = update_author(db, author_id, author)
    if not updated:
        raise HTTPException(status_code=404, detail="Author not found")
    return updated

@app.delete("/authors/{author_id}")
def delete_author_endpoint(author_id: int, db: Session = Depends(get_db)):
    if not delete_author(db, author_id):
        raise HTTPException(status_code=404, detail="Author not found")
    return {"message": "Author deleted successfully"}

# ==================== Book Endpoints (مع Relationships) ====================
@app.post("/books", response_model=BookPublic)
def create_book_endpoint(book: Book, db: Session = Depends(get_db)):
    return create_book(db, book)

@app.get("/books", response_model=List[BookPublic])
def get_books_endpoint(db: Session = Depends(get_db)):
    return get_books(db)

@app.get("/books/{book_id}", response_model=BookPublicWithDetails)
def get_book_with_details_endpoint(book_id: int, db: Session = Depends(get_db)):
    book = get_book_with_details(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@app.put("/books/{book_id}", response_model=BookPublic)
def update_book_endpoint(book_id: int, book: Book, db: Session = Depends(get_db)):
    updated = update_book(db, book_id, book)
    if not updated:
        raise HTTPException(status_code=404, detail="Book not found")
    return updated

@app.delete("/books/{book_id}")
def delete_book_endpoint(book_id: int, db: Session = Depends(get_db)):
    if not delete_book(db, book_id):
        raise HTTPException(status_code=404, detail="Book not found")
    return {"message": "Book deleted successfully"}