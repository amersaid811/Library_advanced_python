from tkinter import *
from tkinter import messagebox
from sql_connection import get_sql_connection




class DeleteMember(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)
        self.geometry("650x750+550+200")
        self.title("Delete Member")
        self.resizable(False,False)

######################################FRAMES######################################################
        #top frame
        self.topframe= Frame(self,height=150,bg='white')
        self.topframe.pack(fill=X)
        #bottom frame
        self.bottomFrame= Frame(self,height=600,bg='#87CEEB')
        self.bottomFrame.pack(fill=X)
        #heading
        self.top_image= PhotoImage(file='icons/delete-user.png')
        top_image_lbl=Label(self.topframe,image=self.top_image,bg='white')
        top_image_lbl.place(x=120,y=20)
        heading=Label(self.topframe, text ='   Delete Member   ',font='arial 22 bold',fg='#003f8a',bg='white')
        heading.place(x=290,y=60)

######################################LABELS######################################################
        
        #MemberID
        self.memberid=Label(self.bottomFrame,text=' MemberID: ',font='arial 15 bold',fg='white',bg='#87CEEB')
        self.memberid.place(x=40,y=40)
        self.ent_memberid=Entry(self.bottomFrame,width=30,bd=4)
        self.ent_memberid.insert(0,'Please enter the MemberID')
        self.ent_memberid.place(x=300,y=45)
        #button
        button=Button(self.bottomFrame,text='Delete Member',command=self.deleteMember)
        button.place(x=550,y=300)
    
    def deleteMember(self):
        memberid = self.ent_memberid.get()

        connection = get_sql_connection()
        if not connection:
            messagebox.showerror("Error", "Could not connect to database.")
            return

        cursor = connection.cursor()
        query = "SELECT * FROM lib.member WHERE MemberID = %s"
        cursor.execute(query, (memberid,))
        result = cursor.fetchone()

        if not result:
            messagebox.showerror("Error", f"Member with ID {memberid} does not exist in the database.")
            connection.close()
            return
        
        query = "DELETE FROM lib.member WHERE MemberID = %s"
        
        try:
            cursor.execute(query, (memberid,))
            connection.commit()
            messagebox.showinfo("Success", "Member deleted successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
        finally:
            connection.close()


    
