import logging
import pickle
import os

# Set up logging configuration
logging.basicConfig(filename='library.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

class Book:
    def __init__(self, isbn, title, publisher, language, num_copies, availability):
        self.isbn = isbn
        self.title = title
        self.publisher = publisher
        self.language = language
        self.num_copies = num_copies
        self.availability = availability

    def __str__(self):
        return (f"ISBN: {self.isbn}, Title: {self.title}, Publisher: {self.publisher}, "
                f"Language: {self.language}, Number of Copies: {self.num_copies}, "
                f"Availability: {self.availability}")


BOOK_RECORDS_FILE = 'book_records.pkl'
BORROWED_BOOKS_FILE = 'borrowed_books.pkl'
USER_ACCOUNTS_FILE = 'user_accounts.pkl'


def load_data():
    if os.path.exists(BOOK_RECORDS_FILE):
        with open(BOOK_RECORDS_FILE, 'rb') as f:
            book_records = pickle.load(f)
    else:
        book_records = []

    if os.path.exists(BORROWED_BOOKS_FILE):
        with open(BORROWED_BOOKS_FILE, 'rb') as f:
            borrowed_books = pickle.load(f)
    else:
        borrowed_books = []

    if os.path.exists(USER_ACCOUNTS_FILE):
        with open(USER_ACCOUNTS_FILE, 'rb') as f:
            user_accounts = pickle.load(f)
    else:
        user_accounts = {'admin': 'password'}  # Initial admin account for testing

    return book_records, borrowed_books, user_accounts


def save_data():
    with open(BOOK_RECORDS_FILE, 'wb') as f:
        pickle.dump(book_records, f)

    with open(BORROWED_BOOKS_FILE, 'wb') as f:
        pickle.dump(borrowed_books, f)

    with open(USER_ACCOUNTS_FILE, 'wb') as f:
        pickle.dump(user_accounts, f)

# Load initial data
book_records, borrowed_books, user_accounts = load_data()

def log_action(action):
    logging.info(action)

def display_menu():
    print("\nLibrary Book Management System")
    print("1. Display all book records")
    print("2. Add new book record")
    print("3. Update book record")
    print("4. Delete book record")
    print("5. Borrow book")
    print("6. Return book")
    print("7. Sort books by Publisher (Bubble Sort)")
    print("8. Sort books by Number of Copies (Insertion Sort)")
    print("9. Exit and save")

def display_books(books):
    if not books:
        print("No books available.")
        log_action("Displayed books: No books available.")
    else:
        print('\nDisplaying all books records:\n')
        for book in books:
            print(book)
        log_action("Displayed all book records.")

def add_book():
    while True:
        try:
            isbn = int(input("Enter ISBN: "))
            if len(str(isbn)) == 13:
                break
            else:
                print("Invalid ISBN. Please enter a 13-digit number.")
        except ValueError:
            print("Invalid ISBN. Please enter a valid number.")

    title = input("Enter Title: ")
    while not title:
        print("Title cannot be empty. Please enter a valid title.")
        title = input("Enter Title: ")

    while True:
        publisher = input("Enter Publisher: ")
        if publisher.strip().replace(" ", "").isalpha():
            break
        else:
            print("Invalid publisher. Please enter a valid publisher with letters only.")

    while True:
        language = input("Enter Language: ")
        if language.isalpha():
            break
        else:
            print("Invalid language. Please enter a language with letters only.")

    while True:
        try:
            num_copies = int(input("Enter Number of Copies: "))
            if num_copies <= 0:
                print("Number of copies must be greater than zero.")
            else:
                break
        except ValueError:
            print("Invalid number of copies. Please enter a valid number.")

    while True:
        availability = input("Enter Availability (True/False): ").strip().lower()
        if availability == 'true' or availability == 'false':
            availability = availability == 'true'
            break
        else:
            print("Invalid availability. Please enter True or False.")

    book = Book(isbn, title, publisher, language, num_copies, availability)
    book_records.append(book)
    log_action(f"Book added: {book}")
    print("Book added successfully!")
    save_data()

def update_book():

    print("Existing Books:\n")
    for book in book_records:
        print(book)

    isbn = int(input("\nEnter ISBN of the book to update: "))

    # Print all books in book_records
    

    for book in book_records:
        if book.isbn == isbn:
            print(f"Updating book: {book}")
            
            # Validate and update ISBN
            new_isbn = input(f"Enter new ISBN (current: {book.isbn}): ")
            while True:
                try:
                    new_isbn = int(new_isbn)
                    if len(str(new_isbn)) == 13:
                        if new_isbn not in [b.isbn for b in book_records if b.isbn != isbn]:
                            break
                        else:
                            print("ISBN already exists in the database. Please enter a different ISBN.")
                    else:
                        print("Invalid ISBN. Please enter a 13-digit number.")
                except ValueError:
                    print("Invalid ISBN. Please enter a valid number.")
                new_isbn = input(f"Enter new ISBN (current: {book.isbn}): ")
            
            # Validate and update title
            title = input(f"Enter new Title (current: {book.title}): ")
            while not title:
                print("Title cannot be empty. Please enter a valid title.")
                title = input(f"Enter new Title (current: {book.title}): ")
            
            # Validate and update publisher
            publisher = input(f"Enter new Publisher (current: {book.publisher}): ")
            while not publisher.strip().replace(" ", "").isalnum():
                print("Invalid publisher. Please enter a valid publisher with letters and spaces only.")
                publisher = input(f"Enter new Publisher (current: {book.publisher}): ")

            
            # Validate and update language
            language = input(f"Enter new Language (current: {book.language}): ")
            while not language.isalpha():
                print("Invalid language. Please enter a language with letters only.")
                language = input(f"Enter new Language (current: {book.language}): ")
            
            # Validate and update number of copies
            num_copies = input(f"Enter new Number of Copies (current: {book.num_copies}): ")
            while True:
                try:
                    num_copies = int(num_copies) if num_copies else book.num_copies
                    if num_copies <= 0:
                        print("Number of copies must be greater than zero.")
                    else:
                        break
                except ValueError:
                    print("Invalid number of copies. Please enter a valid number.")
                num_copies = input(f"Enter new Number of Copies (current: {book.num_copies}): ")

            
            # Validate and update availability
            availability = input(f"Enter new Availability (True/False, current: {book.availability}): ").strip().lower()
            while availability not in ['true', 'false']:
                print("Invalid availability. Please enter True or False.")
                availability = input(f"Enter new Availability (True/False, current: {book.availability}): ").strip().lower()
            availability = availability == 'true'
            
            # Update book instance
            book.isbn = new_isbn
            book.title = title
            book.publisher = publisher
            book.language = language
            book.num_copies = num_copies
            book.availability = availability

            log_action(f"Book updated: {book}")
            print("Book updated successfully!")
            save_data()
            break
    else:
        print("Error: No book found with the provided ISBN.")
        log_action(f"Update failed: No book found with ISBN {isbn}.")



def delete_book():
    print("Existing Books:\n")
    for book in book_records:
        print(book)
    isbn = int(input("\nEnter ISBN of the book to delete: "))
    for b in book_records:
        if b.isbn == isbn:
            book_records.remove(b)
            log_action(f"Book deleted: {b}")
            print("Book deleted successfully!")
            save_data()
            break
    else:
        print("Error: No book found with the provided ISBN.")
        log_action(f"Delete failed: No book found with ISBN {isbn}.")

def list_available_books():
    available_books = [book for book in book_records if book.num_copies > 0 and book.availability]
    if available_books:
        print("Available books for borrowing:")
        for book in available_books:
            print(book)
    else:
        print("No available books for borrowing.")

def borrow_book():
    list_available_books()  # Display available books first

    isbn = int(input("Enter ISBN of the book to borrow: "))
    for book in book_records:
        if book.isbn == isbn:
            if book.num_copies > 0 and book.availability:
                book.num_copies -= 1
                borrowed_books.append(book)
                log_action(f"Book borrowed: {book}")
                print("Book borrowed successfully!")
                save_data()
            else:
                print("Error: The selected book is not available for borrowing.")
                log_action(f"Borrow failed: Book not available for ISBN {isbn}.")
            break
    else:
        print("Error: No book found with the provided ISBN.")
        log_action(f"Borrow failed: No book found with ISBN {isbn}.")


def return_book():
    print("Books borrowed:")
    for book in borrowed_books:
        print(book)
    isbn = int(input("Enter ISBN of the book to return: "))
    for book in borrowed_books:
        if book.isbn == isbn:
            book_records[book_records.index(book)].num_copies += 1
            borrowed_books.remove(book)
            log_action(f"Book returned: {book}")
            print("Book returned successfully!")
            save_data()
            break
    else:
        print("Error: No book found with the provided ISBN or not borrowed.")
        log_action(f"Return failed: No book found with ISBN {isbn} or not borrowed.")

def bubble_sort_books_by_publisher(books):
    n = len(books)
    for i in range(n):
        for j in range(0, n-i-1):
            if books[j].publisher > books[j+1].publisher:
                books[j], books[j+1] = books[j+1], books[j]
    log_action("Sorted books by publisher (ascending order).")
    print("Books sorted by publisher (ascending order).")

def insertion_sort_books_by_copies(books):
    for i in range(1, len(books)):
        key = books[i]
        j = i-1
        while j >= 0 and key.num_copies > books[j].num_copies:
            books[j + 1] = books[j]
            j -= 1
        books[j + 1] = key
    log_action("Sorted books by number of copies (descending order).")
    print("Books sorted by number of copies (descending order).")

def create_account():
    print("Creating a new account.")
    while True:
        username = input("Enter a new username: ")
        if username in user_accounts:
            print("Username already exists. Please choose a different username.")
        else:
            break
    password = input("Enter a new password: ")
    user_accounts[username] = password
    print("Account created successfully!")
    save_data()

def login():
    while True:
        print("1. Log in")
        print("2. Create a new account")
        print("3. Exit")
        choice = input("Do you already have an account? (1 for Yes, 2 for No, 3 to Exit): ")
        if choice == '2':
            create_account()
        elif choice == '3':
            log_action("User chose to exit.")
            return None
        elif choice == '1':
            username = input("Enter username: ")
            password = input("Enter password: ")
            if username in user_accounts and user_accounts[username] == password:
                log_action(f"User {username} logged in successfully.")
                return username
            else:
                print("Invalid username or password. Please try again.")
                log_action("Failed login attempt.")
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

def main():
    username = login()
    if username is None:
        print("Access Denied or User Exited.")
        return

    while True:
        display_menu()
        choice = input("Enter your choice: ")
        if choice == '1':
            display_books(book_records)

        elif choice == '2' or choice == '3' or choice == '4':
            if choice == '2' and username == 'admin':
                add_book()
            elif choice == '3' and username == 'admin':
                update_book()
            elif choice == '4' and username == 'admin':
                delete_book()
            else:
                print("Access Denied. Only admin can perform this operation.")
        elif choice == '5':
            borrow_book()
        elif choice == '6':
            return_book()
        elif choice == '7':
            bubble_sort_books_by_publisher(book_records)
            display_books(book_records)
        elif choice == '8':
            insertion_sort_books_by_copies(book_records)
            display_books(book_records)
        elif choice == '9':
            print("Exiting the program.")
            log_action(f"User {username} logged out.")
            save_data()  # Save data before exiting
            break
        else:
            print("\nInvalid choice. Please try again.")
            log_action(f"Invalid menu choice: {choice}")


if __name__ == "__main__":
    main()
