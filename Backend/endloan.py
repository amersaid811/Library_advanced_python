from tkinter import *
from tkinter import messagebox
from sql_connection import get_sql_connection




class EndLoan(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)
        self.geometry("650x750+550+200")
        self.title("End Loan")
        self.resizable(False,False)

######################################FRAMES######################################################
        #top frame
        self.topframe= Frame(self,height=150,bg='white')
        self.topframe.pack(fill=X)
        #bottom frame
        self.bottomFrame= Frame(self,height=600,bg='#87CEEB')
        self.bottomFrame.pack(fill=X)
        
        #heading
        self.top_image= PhotoImage(file='icons/borrow.png')
        top_image_lbl=Label(self.topframe,image=self.top_image,bg='white')
        top_image_lbl.place(x=120,y=20)
        heading=Label(self.topframe, text ='   End Loan   ',font='arial 22 bold',fg='#003f8a',bg='white')
        heading.place(x=290,y=60)

######################################LABELS######################################################
        
        #LoanID
        self.loanID=Label(self.bottomFrame,text='LoanID: ',font='arial 15 bold',fg='white',bg='#87CEEB')
        self.loanID.place(x=40,y=40)
        self.ent_loanID=Entry(self.bottomFrame,width=30,bd=4)
        self.ent_loanID.insert(0,'Please enter the LoanID')
        self.ent_loanID.place(x=300,y=45)

        #button
        button=Button(self.bottomFrame,text='End Loan',command=self.endLoan)
        button.place(x=550,y=300)

    def endLoan(self):
        loanid = self.ent_loanID.get()

        connection = get_sql_connection()
        if not connection:
                messagebox.showerror("Error", "Could not connect to database.")
                return

        cursor = connection.cursor()

        # Retrieve the book ID associated with the loan
        query_loan = "SELECT BookID FROM lib.loans WHERE LoanID = %s"
        cursor.execute(query_loan, (loanid,))
        result = cursor.fetchone()

        if not result:
                messagebox.showerror("Error", f"Loan with ID {loanid} does not exist in the database.")
                connection.close()
                return

        book_id = result[0]

        # Delete the loan entry
        query_delete_loan = "DELETE FROM lib.loans WHERE LoanID = %s"
        try:
                cursor.execute(query_delete_loan, (loanid,))
                connection.commit()
                messagebox.showinfo("Success", "Loan is deleted successfully.")
        except Exception as e:
                connection.rollback()
                messagebox.showerror("Error", f"Failed to delete loan: {str(e)}")
                connection.close()
                return

        # Update book quantity and status
        try:
                # Increase the quantity by 1
                query_update_quantity = "UPDATE lib.books SET Quantity = Quantity + 1 WHERE BookID = %s"
                cursor.execute(query_update_quantity, (book_id,))
                
                # Retrieve the updated quantity
                query_get_quantity = "SELECT Quantity FROM lib.books WHERE BookID = %s"
                cursor.execute(query_get_quantity, (book_id,))
                quantity = cursor.fetchone()[0]

                # Update status based on quantity
                if quantity > 0:
                        query_update_status = "UPDATE lib.books SET Status = 'Available' WHERE BookID = %s"
                else:
                        query_update_status = "UPDATE lib.books SET Status = 'Checked Out' WHERE BookID = %s"
                
                cursor.execute(query_update_status, (book_id,))
                
                connection.commit()
                messagebox.showinfo("Success", "Quantity and status updated successfully.")
        except Exception as e:
                connection.rollback()
                messagebox.showerror("Error", f"Failed to update quantity and status: {str(e)}")
        finally:
                connection.close()
