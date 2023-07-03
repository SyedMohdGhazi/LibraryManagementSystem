from abc import ABC, abstractmethod

class BookDisplayStrategy(ABC):
    @abstractmethod
    def display(self, book):
        pass

class DefaultBookDisplayStrategy(BookDisplayStrategy):
    def display(self, book):
        print(" *-- " + book)

class FancyBookDisplayStrategy(BookDisplayStrategy):
    def display(self, book):
        print("╔═════════════════════════╗")
        print("║        BOOK INFO        ║")
        print("╠═════════════════════════╣")
        print("---> " + book)

class BookIterator(ABC):
    @abstractmethod
    def has_next(self):
        pass

    @abstractmethod
    def next(self):
        pass

class LibraryCatalogIterator(BookIterator):
    def __init__(self, books):
        self.books = books
        self.index = 0

    def has_next(self):
        return self.index < len(self.books)

    def next(self):
        if self.has_next():
            book = self.books[self.index]
            self.index += 1
            return book
        else:
            raise StopIteration()

class LibraryCatalog:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        self.books = []

    def addBook(self, book):
        self.books.append(book)

    def removeBook(self, book):
        if book in self.books:
            self.books.remove(book)
            print(f"Book '{book}' has been removed from the library.")
        else:
            print(f"Book '{book}' is not in the library.")

    def displayCatalog(self):
        print("Library Catalog:")
        for book in self.books:
            print(book)
        print()

    def get_iterator(self):
        return LibraryCatalogIterator(self.books)

class Observer(ABC):
    @abstractmethod
    def update(self):
        pass

class Student(Observer):
    def __init__(self, name):
        self.name = name

    def update(self):
        print(f"{self.name}, a new book has been added to the library.")

class BookDisplayStrategyFactory:
    @staticmethod
    def create_strategy(strategy_type):
        if strategy_type == "default":
            return DefaultBookDisplayStrategy()
        elif strategy_type == "fancy":
            return FancyBookDisplayStrategy()
        else:
            raise ValueError("Invalid strategy type")

class Library:
    def __init__(self):
        self.books = []
        self.displayStrategy = DefaultBookDisplayStrategy()
        self.catalog = LibraryCatalog()
        self.observers = []

    def registerObserver(self, observer):
        self.observers.append(observer)

    def removeObserver(self, observer):
        self.observers.remove(observer)

    def notifyObservers(self):
        for observer in self.observers:
            observer.update()

    def addBook(self, book):
        self.books.append(book)
        self.catalog.addBook(book)
        self.notifyObservers()

    def removeBook(self, book):
        if book in self.books:
            self.books.remove(book)
            self.catalog.removeBook(book)
            return True
        else:
            print(f"Book '{book}' is not in the library.")
            return False

    def displayAvailableBooks(self):
        print(f"\n{len(self.books)} AVAILABLE BOOKS ARE:")
        iterator = self.catalog.get_iterator()
        while iterator.has_next():
            book = iterator.next()
            self.displayStrategy.display(book)
        print()

    def setDisplayStrategy(self, strategy_type):
        strategy = BookDisplayStrategyFactory.create_strategy(strategy_type)
        self.displayStrategy = strategy

    def donateBook(self, book):
        self.addBook(book)
        print(f"Book '{book}' has been donated to the library.")

if __name__ == "__main__":
    library = Library()

    while True:
        print("\nLibrary Management System")
        print("1. Add User")
        print("2. Add Book")
        print("3. Issue Book")
        print("4. Remove Book")
        print("5. Display Available Books")
        print("6. Donate Book")
        print("7. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            name = input("Enter the user name: ")
            student = Student(name)
            library.registerObserver(student)
            print(f"User '{name}' has been added.")
        elif choice == "2":
            book = input("Enter the book name: ")
            library.addBook(book)
            print(f"Book '{book}' has been added to the library.")
        elif choice == "3":
            book = input("Enter the book name to be issued: ")
            if library.removeBook(book):
                print(f"Book '{book}' has been issued.")
        elif choice == "4":
            book = input("Enter the book name to be removed: ")
            library.removeBook(book)
        elif choice == "5":
            print("Select Display Strategy:")
            print("1. Default Book Display Strategy")
            print("2. Fancy Book Display Strategy")
            display_strategy_choice = input("Enter your choice: ")
            
            if display_strategy_choice == "1":
                library.setDisplayStrategy("default")
            elif display_strategy_choice == "2":
                library.setDisplayStrategy("fancy")
            else:
                print("Invalid display strategy choice.")
            library.displayAvailableBooks()
        elif choice == "6":
            book = input("Enter the book name to be donated: ")
            library.donateBook(book)
        elif choice == "7":
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please try again.")
