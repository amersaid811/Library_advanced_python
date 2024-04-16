from tkinter import *
from tkinter import messagebox
from sql_connection import get_sql_connection

class Statistics(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)
        self.geometry("650x750+550+200")
        self.title("Statistics -> Loans End Stats")
        self.resizable(False, False)

        # Frames
        self.topframe = Frame(self, height=150, bg='white')
        self.topframe.pack(fill=X)
        self.bottomFrame = Frame(self, height=600, bg='#87CEEB')
        self.bottomFrame.pack(fill=BOTH, expand=True)

        # Heading
        self.top_image = PhotoImage(file='icons/stats.png')
        top_image_lbl = Label(self.topframe, image=self.top_image, bg='white')
        top_image_lbl.place(x=120, y=20)
        heading = Label(self.topframe, text='   Loans per Month   ', font='arial 22 bold', fg='#003f8a', bg='white')
        heading.place(x=290, y=60)


        # Button to open stats
        self.button = Button(self.bottomFrame, text='Open Stats', command=self.top_5_loaned_books)
        self.button.grid(row=0, column=2, padx=20, pady=20)

        # Label to display count of loans
        self.result_label = Label(self.bottomFrame, text='', font='arial 14 bold', fg='#003f8a', bg='#87CEEB')
        self.result_label.grid(row=1, column=0, columnspan=3, padx=20, pady=20)

    def top_5_loaned_books(self):
        connection = get_sql_connection()
        if not connection:
            messagebox.showerror("Error", "Could not connect to database.")
            return

        cursor = connection.cursor()
        query = """
                SELECT BookID, COUNT(*) AS LoanCount
                FROM lib.loans
                GROUP BY BookID
                ORDER BY LoanCount DESC
                LIMIT 5
                """
        cursor.execute(query)
        top_books = cursor.fetchall()

        connection.close()

        if not top_books:
            self.result_label.config(text="No books found.")
        else:
            result_text = "Top 5 Loaned Books:\n"
            for book in top_books:
                result_text += f"Book ID: {book[0]}, Loan Count: {book[1]}\n"
            self.result_label.config(text=result_text)
