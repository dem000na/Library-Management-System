import json
from dotenv import load_dotenv
import os


class Book:
    is_avalaible = True

    def __init__(self, id, author, title):
        self.id = id
        self.author = author
        self.title = title
        self.is_avaliable = Book.is_avalaible
        self.quantity = 1

    def to_dictionary(self):
        return {"id": self.id, "author": self.author, "title": self.title, "is_avaliable": self.is_avalaible}

    @staticmethod
    def to_object(data):
        book =  Book(data["id"], data["author"], data["title"])
        book.is_avalaible = data["is_avaliable"]
        return book

    def display_books(self):
        print(f"ID: {self.id}\n"
              f"Title: {self.title}\n"
              f"Author: {self.author}")
        
        if self.is_avalaible:
            print("Available: Yes")
        else:
            print("Available: No")

    def borrow_book(self):
        if self.is_avalaible:
            self.quantity -= 1
            if self.quantity == 0:
                self.is_avalaible = False

            print(f"You borrowed '{self.title}' successfully!")

        else:
            print("Book is out of stock!")

    def return_book(self):
        self.quantity += 1
        if not self.is_avalaible:
            self.is_avalaible = True

        print(f"You retuned '{self.title}' successfully!")    

    def delete_book(self):
        print(f"You deleted '{self.title}' successfully!")

def save_books_to_file(file_path, books):
    with open(file_path, "w") as file:
        json.dump({id: book.to_dictionary() for id, book in books.items()}, file, indent=4)

def load_books_from_file(file_path):
    try:
        with open(file_path, "r") as file:
            data = json.load(file)
            return {int(id): Book.to_object(data=book_values) for id, book_values in data.items()}
    
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def main():
    load_dotenv()
    file_books = os.getenv("file_books") # Your file path
    books = load_books_from_file(file_books)
    is_running = True

    while is_running:
        print("1. Add book\n"
              "2. Display books\n"
              "3. Borrow book\n"
              "4. Return book\n"
              "5. Delete book \n"
              "6. Exit")
        
        print("----------------------")

        choice = get_choice(1, 6)
        print("----------------------")

        match choice:
            case 1:
                add_book(file_books, books)
                print("----------------------")

            case 2:
                display_books(books)

            case 3:
                borrow_book(file_books, books)
                print("----------------------")

            case 4:
                return_book(file_books, books)
                print("----------------------")

            case 5:
                delete_book(file_books, books)
                print("----------------------")

            case 6:
                break
        


def get_choice(start, end):
    while True:
        try:
            user_choice = int(input("Enter your choice: "))

            if not start <= user_choice <= end:
                raise Exception("Invalid choice!")

            return user_choice
        
        except ValueError:
            print("Invalid character!")

        except Exception as e:
            print(e)

def add_book(file_path, books):
    author = input("Enter an author: ")
    title = input("Enter a title: ")
    id = max(books.keys(), default=0) + 1

    books[id] = Book(id, author, title)
    save_books_to_file(file_path, books)
    
    print("You added book successfully!")

def display_books(books):
    if not books:
        print("No books found!")

    else:
        for book in books.values():
            book.display_books()
            print("----------------------")


def borrow_book(file_path, books):
    start = list(books)[0]
    end = list(books)[-1]

    display_books(books)
    choice = get_choice(start, end)

    books[choice].borrow_book()
    save_books_to_file(file_path, books)

def return_book(file_path, books):
    start = list(books)[0]
    end = list(books)[-1]

    display_books(books)
    choice = get_choice(start, end)

    books[choice].return_book()
    save_books_to_file(file_path, books)

def delete_book(file_path, books):
    start = list(books)[0]
    end = list(books)[-1]

    display_books(books)
    choice = get_choice(start, end)

    books[choice].delete_book()
    books.pop(choice)
    save_books_to_file(file_path, books)

main()