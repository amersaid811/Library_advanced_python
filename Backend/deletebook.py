from tkinter import *
from tkinter import messagebox
from sql_connection import get_sql_connection




class DeleteBook(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)
        self.geometry("650x750+550+200")
        self.title("Delete Book")
        self.resizable(False,False)

######################################FRAMES######################################################
        #top frame
        self.topframe= Frame(self,height=150,bg='white')
        self.topframe.pack(fill=X)
        #bottom frame
        self.bottomFrame= Frame(self,height=600,bg='#87CEEB')
        self.bottomFrame.pack(fill=X)
        #heading
        self.top_image= PhotoImage(file='icons/deletebook.png')
        top_image_lbl=Label(self.topframe,image=self.top_image,bg='white')
        top_image_lbl.place(x=120,y=20)
        heading=Label(self.topframe, text ='   Delete Book   ',font='arial 22 bold',fg='#003f8a',bg='white')
        heading.place(x=290,y=60)

######################################LABELS######################################################
        
        #BookID
        self.bookid=Label(self.bottomFrame,text='BookID: ',font='arial 15 bold',fg='white',bg='#87CEEB')
        self.bookid.place(x=40,y=40)
        self.ent_bookid=Entry(self.bottomFrame,width=30,bd=4)
        self.ent_bookid.insert(0,'Please enter the BookID')
        self.ent_bookid.place(x=300,y=45)
        #button
        button=Button(self.bottomFrame,text='Delete Book',command=self.deleteBook)
        button.place(x=550,y=300)
    
    def deleteBook(self):
        bookid = self.ent_bookid.get()

        connection = get_sql_connection()
        if not connection:
            messagebox.showerror("Error", "Could not connect to database.")
            return

        cursor = connection.cursor()
        query = "SELECT * FROM lib.books WHERE BookID = %s"
        cursor.execute(query, (bookid,))
        result = cursor.fetchone()

        if not result:
            messagebox.showerror("Error", f"Book with ID {bookid} does not exist in the database.")
            connection.close()
            return
        
        query = "DELETE FROM lib.books WHERE BookID = %s"
        
        try:
            cursor.execute(query, (bookid,))
            connection.commit()
            messagebox.showinfo("Success", "Book deleted successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
        finally:
            connection.close()


    
