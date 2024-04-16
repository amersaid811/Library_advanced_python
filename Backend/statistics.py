from tkinter import *
from tkinter import messagebox
from sql_connection import get_sql_connection

class Statistics(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)
        self.geometry("650x750+550+200")
        self.title("Statistics -> Loans per Month")
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

        # Month Label and Entry
        self.month_label = Label(self.bottomFrame, text='Choose Month:', font='arial 15 bold', fg='white', bg='#87CEEB')
        self.month_label.grid(row=0, column=0, padx=20, pady=20)
        self.ent_month = Entry(self.bottomFrame, width=30, bd=4)
        self.ent_month.insert(0, 'Enter month (1-12)')
        self.ent_month.grid(row=0, column=1, padx=20, pady=20)

        # Button to open stats
        self.button = Button(self.bottomFrame, text='Open Stats', command=self.loans_by_month)
        self.button.grid(row=0, column=2, padx=20, pady=20)

        # Label to display count of loans
        self.result_label = Label(self.bottomFrame, text='', font='arial 14 bold', fg='#003f8a', bg='#87CEEB')
        self.result_label.grid(row=1, column=0, columnspan=3, padx=20, pady=20)

    # Method to fetch and display count of loans by month
    def loans_by_month(self):
        month = self.ent_month.get()

        try:
            month = int(month)
            if month < 1 or month > 12:
                messagebox.showerror("Error", "Please enter a valid month (1-12).")
                return
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid month (1-12).")
            return

        connection = get_sql_connection()
        if not connection:
            messagebox.showerror("Error", "Could not connect to database.")
            return

        cursor = connection.cursor()
        query = "SELECT COUNT(*) FROM lib.loans WHERE EXTRACT(MONTH FROM LoanDate) = %s"
        cursor.execute(query, (month,))
        result = cursor.fetchone()

        if not result:
            self.result_label.config(text="No loans found for the selected month.")
        else:
            count = result[0]
            self.result_label.config(text=f"Total loans for month {month} is : {count} Loans")

        connection.close()