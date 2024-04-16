from tkinter import *
from tkinter import messagebox
from sql_connection import get_sql_connection

class EditMember(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)
        self.geometry("650x750+550+200")
        self.title("Edit Member")
        self.resizable(False, False)

        # Frames
        self.topframe = Frame(self, height=150, bg='white')
        self.topframe.pack(fill=X)
        self.bottomFrame = Frame(self, height=600, bg='#87CEEB')
        self.bottomFrame.pack(fill=X)

        # Heading
        self.top_image = PhotoImage(file='icons/edit-user.png')
        top_image_lbl = Label(self.topframe, image=self.top_image, bg='white')
        top_image_lbl.place(x=120, y=20)
        heading = Label(self.topframe, text='   Edit Member   ', font='arial 22 bold', fg='#003f8a', bg='white')
        heading.place(x=290, y=60)

        # Labels and Entry Fields
        self.memberID_label = Label(self.bottomFrame, text='MemberID: ', font='arial 15 bold', fg='white', bg='#87CEEB')
        self.memberID_label.place(x=40, y=40)
        self.ent_memberID = Entry(self.bottomFrame, width=30, bd=4)
        self.ent_memberID.insert(0, 'Please enter the MemberID')
        self.ent_memberID.place(x=300, y=45)

        self.name_label = Label(self.bottomFrame, text='Name: ', font='arial 15 bold', fg='white', bg='#87CEEB')
        self.name_label.place(x=40, y=80)
        self.ent_name = Entry(self.bottomFrame, width=30, bd=4)
        self.ent_name.insert(0, 'Please enter the member name')
        self.ent_name.place(x=300, y=85)

        self.email_label = Label(self.bottomFrame, text='Email: ', font='arial 15 bold', fg='white', bg='#87CEEB')
        self.email_label.place(x=40, y=120)
        self.ent_email = Entry(self.bottomFrame, width=30, bd=4)
        self.ent_email.insert(0, 'Please enter the Email')
        self.ent_email.place(x=300, y=125)

        self.phone_label = Label(self.bottomFrame, text='Phone: ', font='arial 15 bold', fg='white', bg='#87CEEB')
        self.phone_label.place(x=40, y=160)
        self.ent_phone = Entry(self.bottomFrame, width=30, bd=4)
        self.ent_phone.insert(0, 'Please enter the Phone Number')
        self.ent_phone.place(x=300, y=165)

        self.type_label = Label(self.bottomFrame, text='Membership Type: ', font='arial 15 bold', fg='white', bg='#87CEEB')
        self.type_label.place(x=40, y=200)
        self.ent_type = Entry(self.bottomFrame, width=30, bd=4)
        self.ent_type.insert(0, 'Please enter the membership type')
        self.ent_type.place(x=300, y=205)

        self.date_label = Label(self.bottomFrame, text='Membership StartDate: ', font='arial 15 bold', fg='white', bg='#87CEEB')
        self.date_label.place(x=40, y=240)
        self.ent_date = Entry(self.bottomFrame, width=30, bd=4)
        self.ent_date.insert(0, 'Format: (2024-11-30)')
        self.ent_date.place(x=300, y=245)

        # Button
        button = Button(self.bottomFrame, text='Edit Member', command=self.editMember)
        button.place(x=550, y=300)

    def editMember(self):
        member = {
            'MemberID': self.ent_memberID.get(),
            'Name': self.ent_name.get(),
            'Email': self.ent_email.get(),
            'Phone': self.ent_phone.get(),
            'MembershipType': self.ent_type.get(),
            'MembershipStartDate': self.ent_date.get()
        }

        connection = get_sql_connection()
        if not connection:
            messagebox.showerror("Error", "Could not connect to database.")
            return

        member_id = member['MemberID']

        cursor = connection.cursor()
        query = "SELECT * FROM member WHERE MemberID = %s"
        cursor.execute(query, (member_id,))
        result = cursor.fetchone()

        if not result:
            messagebox.showerror("Error", f"Member with ID {member_id} does not exist in the database.")
            connection.close()
            return

        query = "UPDATE member SET Name = %s, Email = %s, Phone = %s, MembershipType = %s, MembershipStartDate = %s WHERE MemberID = %s"
        data = (member['Name'], member['Email'], member['Phone'], member['MembershipType'], member['MembershipStartDate'], member_id)

        try:
            cursor.execute(query, data)
            connection.commit()
            messagebox.showinfo("Success", "Member edited successfully.")
        except Exception as e:
            connection.rollback()
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
        finally:
            connection.close()

# Usage example
if __name__ == "__main__":
    root = Tk()
    app = EditMember()
    root.mainloop()
