"""Create database models to represent tables."""
from books_app import db
from sqlalchemy.orm import backref
import enum


class Audience(enum.Enum):
    CHILDREN = 1
    YOUNG_ADULT = 2
    ADULT = 3
    ALL = 4


class Book(db.Model):
    """Book model."""

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    publish_date = db.Column(db.Date)

    # The author - Who wrote it?
    author_id = db.Column(db.Integer, db.ForeignKey("author.id"), nullable=False)

    # .relationship is sugar!
    author = db.relationship("Author", back_populates="books")

    # The audience - Who is this book written for?
    audience = db.Column(db.Enum(Audience), default=Audience.ALL)

    # The genres, e.g. fiction, sci-fi, fantasy
    genres = db.relationship("Genre", secondary="book_genre", back_populates="books")
    users = db.relationship(
        "User", secondary="book_user", back_populates="favorite_books"
    )

    def __str__(self):
        return f"<Book: {self.title}>"

    def __repr__(self):
        return f"<Book: {self.title}><Author: {self.author}>"


class Author(db.Model):
    """Author model."""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

    # .relationship is sugar!
    books = db.relationship("Book", back_populates="author")

    # what's the difference between __str__ and __repr__?
    def __str__(self):
        return f"<Author: {self.name}>"

    def __repr__(self):
        return f"<Author: {self.name}>"


class Genre(db.Model):
    """Genre model."""

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)

    # .relationship is sugar!
    books = db.relationship("Book", secondary="book_genre", back_populates="genres")

    def __str__(self):
        return f"<Genre: {self.name}>"

    def __repr__(self):
        return f"<Genre: {self.name}>"


class User(db.Model):
    """User model."""

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)

    favorite_books = db.relationship(
        "Book", secondary="book_user", back_populates="users"
    )

    def __str__(self):
        return f"<User: {self.username}>"

    def __repr__(self):
        return f"<User: {self.username}>"


# this is a bridge table which maps a many-to-many relationship
book_genre_table = db.Table(
    "book_genre",
    db.Column("book_id", db.Integer, db.ForeignKey("book.id")),
    db.Column("genre_id", db.Integer, db.ForeignKey("genre.id")),
)

favorite_book_table = db.Table(
    "book_user",
    db.Column("book_id", db.Integer, db.ForeignKey("book.id")),
    db.Column("user_id", db.Integer, db.ForeignKey("user.id")),
)
