from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from sql_connection import get_sql_connection
from datetime import datetime


class BookABook(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)
        self.geometry("650x750+550+200")
        self.title("Book Unavailable Book")
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

        # Heading
        self.top_image = PhotoImage(file='icons/time.png')
        top_image_lbl = Label(self.topframe, image=self.top_image, bg='#87CEEB')
        top_image_lbl.place(x=120, y=20)
        heading = Label(self.topframe, text=' Books Reservations', font='arial 22 bold', fg='#003f8a',
                        bg='#87CEEB')
        heading.place(x=290, y=60)

        ########################################LABELS############################################

        # Label and Combobox for book selection
        self.book_label = Label(centerFrame, text="Select Book:")
        self.book_label.grid(row=0, column=0, padx=10, pady=10, sticky='w')

        # Fetch book titles from the database
        self.book_id = self.get_book_id()

        # Create a Combobox to display book titles
        self.book_combobox = ttk.Combobox(centerFrame, values=self.book_id, state='readonly')
        self.book_combobox.grid(row=0, column=1, padx=10, pady=10, sticky='w')
        self.book_combobox.bind("<<ComboboxSelected>>")

        # MemberID
        self.memberID = Label(centerFrame, text='MemberID: ', font='arial 15 bold', fg='white', bg='#87CEEB')
        self.memberID.place(x=10, y=80)
        self.ent_memberID = Entry(centerFrame, width=30, bd=4)
        self.ent_memberID.insert(0, 'Please enter the MemberID')
        self.ent_memberID.place(x=200, y=85)

        # button
        button = Button(centerFrame, text='Add Reservation', command=self.bookABook)
        button.place(x=400, y=300)

    def get_book_id(self):
        try:
            sql_conn = get_sql_connection()
            cursor = sql_conn.cursor()
            cursor.execute("SELECT BookID FROM lib.books WHERE Quantity = 0")
            books = cursor.fetchall()
            return [book[0] for book in books]
        except Exception as e:
            messagebox.showerror("Error", f"Error: {str(e)}")
            return []


    def bookABook(self):
        BookID = self.book_combobox.get()
        member_id = self.ent_memberID.get()
        if not BookID or not member_id:
            messagebox.showwarning("Missing Information", "Please select a book and enter member ID.")
            return
        try:
            sql_conn = get_sql_connection()
            cursor = sql_conn.cursor()
            # Count the number of loans for the member
            cursor.execute("SELECT COUNT(*) FROM lib.loans WHERE MemberID = %s", (member_id,))
            loan_count = cursor.fetchone()[0]
            # Insert reservation with loan count and reservation time
            cursor.execute("INSERT INTO lib.reservations (BookID, MemberID, LoanCount, ReservationTime) VALUES (%s, %s, %s, %s)",
                           (BookID, member_id, loan_count, datetime.now()))
            sql_conn.commit()
            messagebox.showinfo("Success", "Reservation added successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Error: {str(e)}")
