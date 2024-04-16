from tkinter import *
from tkinter import messagebox
from sql_connection import get_sql_connection




class NewLoan(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)
        self.geometry("650x750+550+200")
        self.title("New Loan")
        self.resizable(False,False)

######################################FRAMES######################################################
        #top frame
        self.topframe= Frame(self,height=150,bg='white')
        self.topframe.pack(fill=X)
        #bottom frame
        self.bottomFrame= Frame(self,height=600,bg='#87CEEB')
        self.bottomFrame.pack(fill=X)
        
        #heading
        self.top_image= PhotoImage(file='icons/loan.png')
        top_image_lbl=Label(self.topframe,image=self.top_image,bg='white')
        top_image_lbl.place(x=120,y=20)
        heading=Label(self.topframe, text ='   New Loan   ',font='arial 22 bold',fg='#003f8a',bg='white')
        heading.place(x=290,y=60)

######################################LABELS######################################################
        
        #BookID
        self.bookID=Label(self.bottomFrame,text='BookID: ',font='arial 15 bold',fg='white',bg='#87CEEB')
        self.bookID.place(x=40,y=40)
        self.ent_bookID=Entry(self.bottomFrame,width=30,bd=4)
        self.ent_bookID.insert(0,'Please enter the BookID')
        self.ent_bookID.place(x=300,y=45)
        #MemberID
        self.memberID=Label(self.bottomFrame,text='MemberID: ',font='arial 15 bold',fg='white',bg='#87CEEB')
        self.memberID.place(x=40,y=80)
        self.ent_memberID=Entry(self.bottomFrame,width=30,bd=4)
        self.ent_memberID.insert(0,'Please enter the MemberID')
        self.ent_memberID.place(x=300,y=85)
        #LoanDate
        self.loanDate = Label(self.bottomFrame, text='Loan Date: ', font='arial 15 bold', fg='white', bg='#87CEEB')
        self.loanDate.place(x=40, y=120)
        self.ent_loanDate = Entry(self.bottomFrame, width=30, bd=4)
        self.ent_loanDate.insert(0, 'Please enter Loan Date')
        self.ent_loanDate.place(x=300, y=125)
        #ReturnDate
        self.returnDate = Label(self.bottomFrame, text='Return Date: ', font='arial 15 bold', fg='white', bg='#87CEEB')
        self.returnDate.place(x=40, y=160)
        self.ent_returnDate = Entry(self.bottomFrame, width=30, bd=4)
        self.ent_returnDate.insert(0, 'Please enter the Return Date')
        self.ent_returnDate.place(x=300, y=165)

        #button
        button=Button(self.bottomFrame,text='Add Loan',command=self.newLoan)
        button.place(x=550,y=300)

    def newLoan(self):
        book_id = self.ent_bookID.get()
        member_id = self.ent_memberID.get()
        loan_date = self.ent_loanDate.get()
        return_date = self.ent_returnDate.get()

        if not book_id or not member_id or not loan_date or not return_date:
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        connection = get_sql_connection()
        if not connection:
            messagebox.showerror("Error", "Could not tetstest to database.")
            return

        try:
            # Start a transaction
            connection.start_transaction()

            # Check if the book is available
            cursor = connection.cursor()
            availability_query = "SELECT Quantity FROM lib.books WHERE BookID = %s"
            cursor.execute(availability_query, (book_id,))
            result = cursor.fetchone()

            if not result:
                messagebox.showerror("Error", f"Book with ID {book_id} does not exist.")
                return

            quantity = result[0]
            if quantity <= 0:
                messagebox.showerror("Error", f"Book with ID {book_id} is out of stock.")
                return

            # Insert new loan record into the database
            loan_query = "INSERT INTO loans (BookID, MemberID, LoanDate, ReturnDate) VALUES (%s, %s, %s, %s)"
            cursor.execute(loan_query, (book_id, member_id, loan_date, return_date))

            # Update the book quantity by -1
            decrease_quantity_query = "UPDATE books SET Quantity = Quantity - 1 WHERE BookID = %s"
            cursor.execute(decrease_quantity_query, (book_id,))

            # If quantity drops to 0, update status to 'Checked Out'
            if quantity == 1:
                update_status_query = "UPDATE books SET Status = 'Checked Out' WHERE BookID = %s"
                cursor.execute(update_status_query, (book_id,))

            # Commit the transaction
            connection.commit()

            messagebox.showinfo("Success", "New loan added successfully.")
        except Exception as e:
            # Rollback the transaction in case of any error
            connection.rollback()
            messagebox.showerror("Error", f"Failed to add loan: {str(e)}")
        finally:
            connection.close()  # Close the database connection
