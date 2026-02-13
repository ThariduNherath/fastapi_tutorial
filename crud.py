from fastapi import FastAPI
from pydantic import BaseModel


books = [

    {"id": 1, "title": "1984", "author": "George Orwell","publish_date":"1949"},
    {"id": 2, "title": "To Kill a Mockingbird", "author": "Harper Lee","publish_date":"1960"},
    {"id": 3, "title": "The Great Gatsby", "author": "F. Scott Fitzgerald","publish_date":"1925"},
    {"id": 4, "title": "Pride and Prejudice", "author": "Jane Austen","publish_date":"1813"},



]

app = FastAPI()

@app.get("/books")
def get_books():
    return books


class Book(BaseModel):
    id: int
    title: str
    author: str
    publish_date: str


@app.post("/book")
def create_book(book: Book):
    new_book = book.model_dump()
    books.append(new_book)
    return new_book 