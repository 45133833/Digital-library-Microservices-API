from sqlmodel import Session, select
from typing import List, Optional
from .models import User, Author, Book, BookPublicWithDetails

# ==================== User CRUD ====================
def create_user(session: Session, user: User) -> User:
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

def get_users(session: Session) -> List[User]:
    return session.exec(select(User)).all()

def get_user(session: Session, user_id: int) -> Optional[User]:
    return session.get(User, user_id)

def update_user(session: Session, user_id: int, user_data: User) -> Optional[User]:
    user = session.get(User, user_id)
    if not user:
        return None
    user.email = user_data.email
    user.username = user_data.username
    user.full_name = user_data.full_name
    session.commit()
    session.refresh(user)
    return user

def delete_user(session: Session, user_id: int) -> bool:
    user = session.get(User, user_id)
    if not user:
        return False
    session.delete(user)
    session.commit()
    return True

# ==================== Author CRUD ====================
def create_author(session: Session, author: Author) -> Author:
    session.add(author)
    session.commit()
    session.refresh(author)
    return author

def get_authors(session: Session) -> List[Author]:
    return session.exec(select(Author)).all()

def get_author(session: Session, author_id: int) -> Optional[Author]:
    return session.get(Author, author_id)

def update_author(session: Session, author_id: int, author_data: Author) -> Optional[Author]:
    author = session.get(Author, author_id)
    if not author:
        return None
    author.name = author_data.name
    author.birth_year = author_data.birth_year
    author.nationality = author_data.nationality
    session.commit()
    session.refresh(author)
    return author

def delete_author(session: Session, author_id: int) -> bool:
    author = session.get(Author, author_id)
    if not author:
        return False
    session.delete(author)
    session.commit()
    return True

# ==================== Book CRUD (مع Relationships) ====================
def create_book(session: Session, book: Book) -> Book:
    session.add(book)
    session.commit()
    session.refresh(book)
    return book

def get_books(session: Session) -> List[Book]:
    return session.exec(select(Book)).all()

def get_book_with_details(session: Session, book_id: int) -> Optional[BookPublicWithDetails]:
    book = session.get(Book, book_id)
    if not book:
        return None
    
    # Load relationships manually
    session.refresh(book, attribute_names=["authors", "owner"])
    
    return BookPublicWithDetails(
        id=book.id,
        title=book.title,
        isbn=book.isbn,
        published_year=book.published_year,
        available=book.available,
        quantity=book.quantity,
        owner_id=book.owner_id,
        author_id=book.author_id,
        author=AuthorPublic(
            id=book.authors.id,
            name=book.authors.name,
            birth_year=book.authors.birth_year,
            nationality=book.authors.nationality
        ) if book.authors else None,
        owner=UserPublic(
            id=book.owner.id,
            email=book.owner.email,
            username=book.owner.username,
            full_name=book.owner.full_name,
            is_active=book.owner.is_active
        ) if book.owner else None
    )

def update_book(session: Session, book_id: int, book_data: Book) -> Optional[Book]:
    book = session.get(Book, book_id)
    if not book:
        return None
    book.title = book_data.title
    book.isbn = book_data.isbn
    book.published_year = book_data.published_year
    book.available = book_data.available
    book.quantity = book_data.quantity
    session.commit()
    session.refresh(book)
    return book

def delete_book(session: Session, book_id: int) -> bool:
    book = session.get(Book, book_id)
    if not book:
        return False
    session.delete(book)
    session.commit()
    return True