from tkinter import *
from tkinter import messagebox
from sql_connection import get_sql_connection
import checkreservations
import bookabook

class WaitingList(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)
        self.geometry("600x750+550+200")
        self.title("Waiting List Interface")
        self.resizable(False, False)

        # Frames
        mainFrame = Frame(self)
        mainFrame.pack(fill=BOTH, expand=True)

        # Top frame
        self.topframe = Frame(mainFrame, height=150, bg='#87CEEB')
        self.topframe.pack(fill=X)

        # Center frame
        centerFrame = Frame(mainFrame, width=600, relief=RIDGE, bg='#e0f0f0', borderwidth=5)
        centerFrame.pack(side=TOP, fill=BOTH, expand=True)

        # Center left frame
        centerLeftFrame = Frame(centerFrame, width=200, height=700, bg='#e0f0f0', borderwidth=2, relief='sunken')
        centerLeftFrame.pack(side=LEFT, fill=Y)

        # Center right frame
        centerRightFrame = Frame(centerFrame, width=450, height=700, bg='#e0f0f0', borderwidth=2, relief='sunken')
        centerRightFrame.pack(side=RIGHT, fill=Y)

        # Heading
        self.top_image = PhotoImage(file='icons/time.png')
        top_image_lbl = Label(self.topframe, image=self.top_image, bg='#87CEEB')
        top_image_lbl.place(x=120, y=20)
        heading = Label(self.topframe, text='   Unavailable Books   ', font='arial 22 bold', fg='#003f8a', bg='#87CEEB')
        heading.place(x=290, y=60)

        # Listbox to display books with quantity = 0
        self.list_books = Listbox(centerLeftFrame, width=35, height=30, bd=5, font='times 12 bold')
        self.list_books.pack(padx=10, pady=10, fill=BOTH, expand=True)

        # Scrollbar for the listbox
        self.sb = Scrollbar(centerLeftFrame, orient=VERTICAL)
        self.sb.config(command=self.list_books.yview)
        self.list_books.config(yscrollcommand=self.sb.set)
        self.sb.pack(side=RIGHT, fill=Y)

        # Create a button for watching waiting list
        self.iconlist = PhotoImage(file='icons/watch.png')
        self.watch_list_button = Button(centerRightFrame, text='Reservations List',font='arial 12 bold',
                                         padx=10, command=self.display_waiting_lists)

        self.watch_list_button.configure(image=self.iconlist, compound=LEFT)
        self.watch_list_button.pack(side=TOP, pady=10)

        # Create a button for booking a book
        self.iconbook = PhotoImage(file='icons/loan.png')
        self.book_abook_button = Button(centerRightFrame, text='Book Unavailable Book', font='arial 12 bold',
                                         padx=10, command=self.bookABook)
        self.book_abook_button.configure(image=self.iconbook, compound=LEFT)
        self.book_abook_button.pack(side=TOP, pady=10)

        # Display books with quantity = 0
        self.display_zero_quantity_books()


    def display_waiting_lists(self):
        checkreservations.CheckReservations()

    def bookABook(self):  # Corrected method name
        bookabook.BookABook()  # Corrected method name

    def display_zero_quantity_books(self):
        connection = get_sql_connection()
        if not connection:
            messagebox.showerror("Error", "Could not connect to database.")
            return

        try:
            cursor = connection.cursor()
            query = "SELECT * FROM lib.books WHERE Quantity = 0"
            cursor.execute(query)
            books = cursor.fetchall()

            if not books:
                self.list_books.insert(END, "No books with quantity 0 found.")
            else:
                for book in books:
                    # Access dictionary values using integer indices instead of string keys
                    title = book[1]  # Assuming Title is the second column in your database table
                    book_id = book[0]  # Assuming BookID is the first column
                    self.list_books.insert(END, f"{title} (ID: {book_id})")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
