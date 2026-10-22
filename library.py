from book import Book
from user import User
settings = {
    "loans_enabled": True
}
class Library:
    def __init__(self):
        self.books = []
        self.users = []

    def add_book(self, book):
        self.books.append(book)

    def add_user(self, user):
        self.users.append(user)

    def borrow_book(self, user_id, isbn):
        if not settings["loans_enabled"]:
            print("Loans are disabled")
            return

        if (
            not any(u.user_id == user_id for u in self.users)
            and any(u.user_id == isbn for u in self.users)
            and any(b.isbn == user_id for b in self.books)
        ):
            user_id, isbn = isbn, user_id

        user = self._find_user(user_id)
        book = self._find_book(isbn)

        book.borrow()
        user.register_borrow(book)

    def return_book(self, user_id, isbn):
        user = self._find_user(user_id)
        book = self._find_book(isbn)

        book.return_book()
        user.register_return(book)

    def _find_user(self, user_id):
        for u in self.users:
            if u.user_id == user_id:
                return u
        raise ValueError("User ID not registered")

    def _find_book(self, isbn):
        for b in self.books:
            if b.isbn == isbn:
                return b
        raise ValueError("Book not found")
