from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime

# ==================== Users Microservice ====================
class UserBase(SQLModel):
    email: str = Field(index=True, unique=True)
    username: str = Field(index=True, unique=True)
    password_hash: str
    full_name: Optional[str] = None
    is_active: bool = True

class User(UserBase, table=True):
    __tablename__ = "users"
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Relationship: User → Books (One-to-Many)
    books: List["Book"] = Relationship(back_populates="owner")
    
    # Relationship: User → Authors (One-to-Many)
    authors: List["Author"] = Relationship(back_populates="user")

class UserPublic(UserBase):
    id: int
    is_active: bool

# ==================== Authors Microservice ====================
class AuthorBase(SQLModel):
    name: str = Field(index=True)
    birth_year: Optional[int] = None
    nationality: Optional[str] = None
    bio: Optional[str] = None

class Author(AuthorBase, table=True):
    __tablename__ = "authors"
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Foreign Key: User owns this Author
    user_id: Optional[int] = Field(default=None, foreign_key="users.id")
    
    # Relationship: Author → User (Many-to-One)
    user: Optional[User] = Relationship(back_populates="authors")
    
    # Relationship: Author → Books (One-to-Many)
    books: List["Book"] = Relationship(back_populates="authors")

class AuthorPublic(AuthorBase):
    id: int

# ==================== Books Microservice ====================
class BookBase(SQLModel):
    title: str = Field(index=True)
    isbn: str = Field(unique=True)
    published_year: Optional[int] = None
    available: bool = True
    quantity: int = 1

class Book(BookBase, table=True):
    __tablename__ = "books"
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Foreign Keys
    owner_id: Optional[int] = Field(default=None, foreign_key="users.id")
    author_id: Optional[int] = Field(default=None, foreign_key="authors.id")
    
    # Relationship: Book → User (Many-to-One)
    owner: Optional[User] = Relationship(back_populates="books")
    
    # Relationship: Book → Authors (Many-to-One)
    authors: Optional[Author] = Relationship(back_populates="books")

class BookPublic(BookBase):
    id: int
    owner_id: Optional[int]
    author_id: Optional[int]

# Book dengan Author + User data (for single read)
class BookPublicWithDetails(BookPublic):
    author: Optional[AuthorPublic] = None
    owner: Optional[UserPublic] = None
