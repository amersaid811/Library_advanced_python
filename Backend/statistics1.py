from tkinter import *
from tkinter import messagebox
from sql_connection import get_sql_connection

class Statistics(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)
        self.geometry("650x750+550+200")
        self.title("Statistics -> Loans per Periods")
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
        heading = Label(self.topframe, text='   Loans per Periods   ', font='arial 22 bold', fg='#003f8a', bg='white')
        heading.place(x=290, y=60)

        # Month Label and Entry
        self.start_month_label = Label(self.bottomFrame, text='Start Month:', font='arial 15 bold', fg='white', bg='#87CEEB')
        self.start_month_label.grid(row=0, column=0, padx=20, pady=20)
        self.ent_month1 = Entry(self.bottomFrame, width=10, bd=4)
        self.ent_month1.insert(0, 'Month')
        self.ent_month1.grid(row=0, column=1, padx=10, pady=20)

        self.end_month_label = Label(self.bottomFrame, text='End Month:', font='arial 15 bold', fg='white', bg='#87CEEB')
        self.end_month_label.grid(row=1, column=0, padx=20, pady=20)
        self.ent_month2 = Entry(self.bottomFrame, width=10, bd=4)
        self.ent_month2.insert(0, 'Month')
        self.ent_month2.grid(row=1, column=1, padx=10, pady=20)

        # Button to open stats
        self.button = Button(self.bottomFrame, text='Show Stats', command=self.show_loan_count)
        self.button.grid(row=2, column=0, columnspan=2, padx=20, pady=20)

        # Label to display count of loans
        self.result_text = Text(self.bottomFrame, width=60, height=20)
        self.result_text.grid(row=3, column=0, columnspan=2, padx=20, pady=20)

    def show_loan_count(self):
        start_month = self.ent_month1.get()
        end_month = self.ent_month2.get()

        try:
            start_month = int(start_month)
            end_month = int(end_month)
            if start_month < 1 or start_month > 12 or end_month < 1 or end_month > 12:
                messagebox.showerror("Error", "Please enter valid months (1-12).")
                return
        except ValueError:
            messagebox.showerror("Error", "Please enter valid months (1-12).")
            return

        connection = get_sql_connection()
        if not connection:
            messagebox.showerror("Error", "Could not connect to database.")
            return

        results = self.loans_between_2months(connection, start_month, end_month)

        if results is None:
            messagebox.showinfo("Info", "No loans found for the selected period.")
        else:
            self.result_text.delete(1.0, END)  # Clear previous results
            self.result_text.insert(END, f"Number of loans between months {start_month} and {end_month}: {len(results)}")

        connection.close()

    # Method to fetch loans between two specified months
    def loans_between_2months(self, connection, start_month, end_month):
        cursor = connection.cursor()
        query = "SELECT * FROM lib.loans WHERE MONTH(LoanDate) BETWEEN %s AND %s"
        cursor.execute(query, (start_month, end_month))

        # Fetch the results
        results = cursor.fetchall()

        # Return the fetched results
        return results

