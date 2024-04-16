from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from sql_connection import get_sql_connection

class CheckReservations(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)
        self.geometry("900x750+550+200")
        self.title("Reservation List")
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
        heading = Label(self.topframe, text='   Reservations List   ', font='arial 22 bold', fg='#003f8a', bg='#87CEEB')
        heading.place(x=290, y=60)
#####################################################LABELS###########################################################
        
        # Label and Combobox for book selection
        self.book_label = Label(centerFrame, text="Select Book:")
        self.book_label.grid(row=0, column=0, padx=10, pady=10, sticky='w')

        # Fetch book titles from the database
        self.BookIDs = self.get_BookIDs()

        # Create a Combobox to display book titles
        self.book_combobox = ttk.Combobox(centerFrame, values=self.BookIDs, state='readonly')
        self.book_combobox.grid(row=0, column=1, padx=10, pady=10, sticky='w')
        self.book_combobox.bind("<<ComboboxSelected>>", self.display_selected_book_reservations)

        # Treeview to display waiting lists
        self.tree = ttk.Treeview(centerFrame, columns=('ReservationsID','MemberID', 'ReservationTime'))
        
        self.tree.heading('#0', text='BookID')
        self.tree.heading('ReservationsID', text='ReservationID')
        self.tree.heading('MemberID', text='MemberID')
        self.tree.heading('ReservationTime', text='Reservation Time')
        self.tree.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky='nsew')

        # Display waiting lists
        self.display_waiting_lists()

        # Make the window visible
        self.wait_visibility()
        self.grab_set()
        self.focus_set()
        self.wait_window()

    def get_BookIDs(self):
        connection = get_sql_connection()
        if not connection:
            messagebox.showerror("Error", "Could not not not connect to database.")
            return []

        try:
            cursor = connection.cursor()
            cursor.execute("SELECT Title FROM lib.books WHERE Quantity = 0")
            books = cursor.fetchall()
            BookIDs = [book[0] for book in books]
            return BookIDs
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            return []
        finally:
            connection.close()

    def display_selected_book_reservations(self, event):
        selected_book = self.book_combobox.get()
        if not selected_book:
            return

        connection = get_sql_connection()
        if not connection:
            messagebox.showerror("Error", "Could not connect to database.")
            return

        try:
            cursor = connection.cursor()
            cursor.execute("SELECT BookID FROM lib.books WHERE Title = %s", (selected_book,))
            book_id = cursor.fetchone()[0]

            self.tree.delete(*self.tree.get_children())  # Clear previous reservations
            
            # Retrieve reservations sorted by priority conditions
            cursor.execute("SELECT ReservationsID, MemberID, ReservationTime FROM lib.reservations WHERE BookID = %s ORDER BY "
                        "CASE WHEN MemberID IN (SELECT MemberID FROM lib.loans GROUP BY MemberID ORDER BY COUNT(*) DESC) "
                        "THEN 0 ELSE 1 END, ReservationTime", (book_id,))
            reservations = cursor.fetchall()

            for reservation in reservations:
                self.tree.insert('', 'end', values=reservation)

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
        finally:
            connection.close()

