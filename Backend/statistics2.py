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
        self.button = Button(self.bottomFrame, text='Open Stats', command=self.loans_return)
        self.button.grid(row=0, column=2, padx=20, pady=20)

        # Label to display count of loans
        self.result_label = Label(self.bottomFrame, text='', font='arial 14 bold', fg='#003f8a', bg='#87CEEB')
        self.result_label.grid(row=1, column=0, columnspan=3, padx=20, pady=20)
    
    def loans_return(self):
        connection = get_sql_connection()
        if not connection:
            messagebox.showerror("Error", "Could not connect to database.")
            return
        
        cursor = connection.cursor()
        query = "SELECT * FROM lib.loans WHERE ReturnDate IS NOT NULL" 
        cursor.execute(query)
        returned_loans = cursor.fetchall()

        if not returned_loans:
            self.result_label.config(text="No returned loans found.")
        else:
            total_returned_loans = len(returned_loans)
            self.result_label.config(text=f"Total returned loans: {total_returned_loans}")

            # Display detailed information about returned loans
            detailed_info = ""
            for loan in returned_loans:
                loan_id = loan[0]
                member_id = loan[1]
                book_id = loan[2]
                loan_date = loan[3]
                return_date = loan[4]
                detailed_info += f"Loan ID: {loan_id}, Member ID: {member_id}, Book ID: {book_id}, Loan Date: {loan_date}, Return Date: {return_date}\n"

            # Create a text widget to display detailed loan information
            self.detailed_text = Text(self.bottomFrame, width=60, height=10, font='arial 12')
            self.detailed_text.grid(row=2, column=0, columnspan=3, padx=20, pady=20)
            self.detailed_text.insert(END, detailed_info)

        connection.close()



        