from fastapi import FastAPI ,status
from pydantic import BaseModel
from fastapi.exceptions import HTTPException


books = [

    {"id": 1, "title": "1984", "author": "George Orwell","publish_date":"1949"},
    {"id": 2, "title": "To Kill a Mockingbird", "author": "Harper Lee","publish_date":"1960"},
    {"id": 3, "title": "The Great Gatsby", "author": "F. Scott Fitzgerald","publish_date":"1925"},
    {"id": 4, "title": "Pride and Prejudice", "author": "Jane Austen","publish_date":"1813"},



]

app = FastAPI()

# Get all books

@app.get("/books")
def get_books():
    return books

@app.get("/books/{book_id}")
def get_book(book_id: int):
    for book in books:
        if book["id"] == book_id:
            return book
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found") 


class Book(BaseModel):
    id: int
    title: str
    author: str
    publish_date: str

# Create a new book

@app.post("/book")
def create_book(book: Book):
    new_book = book.model_dump()
    books.append(new_book)
    return new_book 

class BookUpdate(BaseModel):
    title: str
    author: str
    publish_date: str


# Update a book by ID
@app.put("/books/{book_id}")
def update_book(book_id: int, updated_book: BookUpdate):
    for i, book in enumerate(books):
        if book["id"] == book_id:
            book["title"] = updated_book.title 
            book["author"] = updated_book.author
            book["publish_date"] = updated_book.publish_date
            return book
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")    


@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    for i, book in enumerate(books):
        if book["id"] == book_id:
            books.remove(book)
            return {"message": "Book deleted successfully"}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")