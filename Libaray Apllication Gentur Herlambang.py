## Pembuatan Aplikasi Perpustakaan oleh : Gentur Herlambang 


import re
import datetime
import tkinter as tk
from tkinter import messagebox

# Membuat kelas Buku mewakili buku dengan nama, peminjam, dan tanggal peminjamannya.
class Book:
    def __init__(self, name, borrowed_by=None, borrowed_date=None):
        self.name = name
        self.borrowed_by = borrowed_by
        self.borrowed_date = borrowed_date

# Kelas Pengguna mewakili pengguna dengan email, kata sandi, dan buku pinjaman.
class User:
    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.borrowed_book = None

    # Hanya bisa menggunakan email yang sudah tervalidasi.
    def validate_email_domain(self):
        domain = re.search("@[\w.]+", self.email).group()
        if domain in ["@gmail.com", "@hotmail.com"]:
            return True
        else:
            return False

    # Membuat validasi jika kata sandi memenuhi persyaratan (setidaknya 8 karakter, setidaknya satu huruf besar, dan hanya karakter alfanumerik).
    def validate_password(self):
        if len(self.password) < 8:
            return False
        if not re.search("[A-Z]", self.password):
            return False
        if re.search("[^a-zA-Z0-9]", self.password):
            return False
        return True

    # 1 E-mail hanya bisa digunkan 1 pengguna.
    def register(self):
        if self.email in registered_emails:
            messagebox.showerror("Registration", "Email is already registered.")
            return

        if self.validate_email_domain() and self.validate_password():
            registered_emails.append(self.email)
            messagebox.showinfo("Registration", "User registered successfully.")
        else:
            messagebox.showerror("Registration", "Invalid email domain or password. Please check the requirements.")

    # Hanya bisa meminjam buku 1 , apabila ingin meminjam buku lagi harus mengembalikan yang sebelumnya
    def borrow_book(self, book_name):
        if self.borrowed_book is not None:
            messagebox.showerror("Borrow Book", "You already have a book borrowed. Please return it first.")
            return

        if self in late_returned_users:
            messagebox.showerror("Borrow Book", "You have returned a book late. Please return the late book first.")
            return

        book = None
        for b in available_books:
            if b.name == book_name:
                book = b
                break

        if book is None:
            messagebox.showerror("Borrow Book", "The requested book is not available for borrowing.")
            return

        book.borrowed_by = self
        book.borrowed_date = datetime.datetime.now()
        self.borrowed_book = book
        messagebox.showinfo("Borrow Book", "Book borrowed successfully.")

    # Mengembalikan Buku
    def return_book(self):
        if self.borrowed_book is None:
            messagebox.showerror("Return Book", "You don't have any books borrowed.")
            return

        borrowed_book = self.borrowed_book
        borrowed_book.borrowed_by = None
        borrowed_book.borrowed_date = None
        self.borrowed_book = None

        if borrowed_book in late_returned_books:
            late_returned_books.remove(borrowed_book)
            late_returned_users.remove(self)

        messagebox.showinfo("Return Book", "Book returned successfully.")

    # Melihat Ketersidiaan Buku
    def check_book_stock(self):
        stock = ""
        for book in available_books:
            if book.borrowed_by is None:
                stock += f"{book.name}: Available\n"
            else:
                stock += f"{book.name}: Borrowed by {book.borrowed_by.email}\n"

        messagebox.showinfo("Book Stock", stock)

# Daftar untuk melihat email yang di daftarkan , buku yang ada, buku yang di pinjam , dan buku yang telat di pinjam
registered_emails = []
available_books = [Book("Book1"), Book("Book2"), Book("Book3")]
late_returned_books = []
late_returned_users = []

# Function interkasi GUI

# Pendaftaran pengguna dengan mendapatkan email dan kata sandi dari  entri GUI.
def register_user():
    email = email_entry.get()
    password = password_entry.get()

    user = User(email, password)
    user.register()

# Peminjaman Buku dari GUI
def borrow_book():
    email = email_entry.get()

    if email not in registered_emails:
        messagebox.showerror("Borrow Book", "Email is not registered.")
        return

    user = User(email, None)
    book_name = book_entry.get()
    user.borrow_book(book_name)

# Pengembaian Buku dari GUI
def return_book():
    email = email_entry.get()

    if email not in registered_emails:
        messagebox.showerror("Return Book", "Email is not registered.")
        return

    user = User(email, None)
    user.return_book()

# Megecheck buku dengan email admin
def check_book_stock():
    admin_email = email_entry.get()

    if admin_email not in registered_emails:
        messagebox.showerror("Admin Access", "Email is not registered.")
        return

    user = User(admin_email, None)
    user.check_book_stock()

# Membuat GUI Window.
root = tk.Tk()
root.title("Library System")

# Membuat label,  entri, dan window GUI.
email_label = tk.Label(root, text="Email:")
email_label.pack()

email_entry = tk.Entry(root)
email_entry.pack()

password_label = tk.Label(root, text="Password:")
password_label.pack()

password_entry = tk.Entry(root, show="*")
password_entry.pack()

register_button = tk.Button(root, text="Register", command=register_user)
register_button.pack()

book_label = tk.Label(root, text="Book:")
book_label.pack()

book_entry = tk.Entry(root)
book_entry.pack()

borrow_button = tk.Button(root, text="Borrow Book", command=borrow_book)
borrow_button.pack()

return_button = tk.Button(root, text="Return Book", command=return_book)
return_button.pack()

admin_button = tk.Button(root, text="Check Book Stock", command=check_book_stock)
admin_button.pack()

# Run GUI loop.
root.mainloop()
