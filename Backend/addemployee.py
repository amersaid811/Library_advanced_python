from tkinter import *
from tkinter import messagebox
from sql_connection import get_sql_connection

class AddEmployee(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)
        self.geometry("650x750+550+200")
        self.title("Add Employee")
        self.resizable(False,False)

        #top frame
        self.topframe = Frame(self, height=150, bg='white')
        self.topframe.pack(fill=X)
        #bottom frame
        self.bottomFrame = Frame(self, height=600, bg='#87CEEB')
        self.bottomFrame.pack(fill=X)
        
        #heading
        self.top_image= PhotoImage(file='icons/add-user.png')
        top_image_lbl=Label(self.topframe,image=self.top_image,bg='white')
        top_image_lbl.place(x=120,y=20)
        heading=Label(self.topframe, text ='   Add Employee   ',font='arial 22 bold',fg='#003f8a',bg='white')
        heading.place(x=290,y=60)

        #EmployeeID
        self.memberID=Label(self.bottomFrame,text='MemberID: ',font='arial 15 bold',fg='white',bg='#87CEEB')
        self.memberID.place(x=40,y=40)
        self.employeeID=Entry(self.bottomFrame,width=30,bd=4)
        self.employeeID.insert(0,'Please enter the MemberID')
        self.employeeID.place(x=300,y=45)

        #Name
        self.name=Label(self.bottomFrame,text='Name: ',font='arial 15 bold',fg='white',bg='#87CEEB')
        self.name.place(x=40,y=80)
        self.ent_name=Entry(self.bottomFrame,width=30,bd=4)
        self.ent_name.insert(0,'Please enter the member name')
        self.ent_name.place(x=300,y=85)

        #Email
        self.email = Label(self.bottomFrame, text='Email: ', font='arial 15 bold', fg='white', bg='#87CEEB')
        self.email.place(x=40, y=120)
        self.ent_email = Entry(self.bottomFrame, width=30, bd=4)
        self.ent_email.insert(0, 'Please enter the Email')
        self.ent_email.place(x=300, y=125)

        #EmployeeType
        self.type_label = Label(self.bottomFrame, text='Employee Type: ', font='arial 15 bold', fg='white', bg='#87CEEB')
        self.type_label.place(x=40, y=160)
        self.ent_type = Entry(self.bottomFrame, width=30, bd=4)
        self.ent_type.insert(0, 'Manager or Worker ?')
        self.ent_type.place(x=300, y=165)

        #Password
        self.password_label = Label(self.bottomFrame, text='Create Password: ', font='arial 15 bold', fg='white', bg='#87CEEB')
        self.password_label.place(x=40, y=200)
        self.ent_password = Entry(self.bottomFrame, width=30, bd=4)
        self.ent_password.insert(0, 'Please enter the password')
        self.ent_password.place(x=300, y=205)

        #button
        button=Button(self.bottomFrame,text='Add Employee',command=self.addEmployee)
        button.place(x=550,y=300)

    def addEmployee(self):
        employee = {
            'EmployeeID': self.employeeID.get(),
            'Name': self.ent_name.get(),
            'Email': self.ent_email.get(),
            'EmployeeType': self.ent_type.get(),
            'Password': self.ent_password.get()
        }

        connection = get_sql_connection()
        if not connection:
            messagebox.showerror("Error", "Could not connect to database.")
            return

        employee_id = employee['EmployeeID']

        cursor = connection.cursor()
        query = "SELECT * FROM employees WHERE EmployeeID = %s"
        cursor.execute(query, (employee_id,))
        result = cursor.fetchone()

        if result:
            messagebox.showerror("Error", f"Member with ID {employee_id} already exists in the database.")
            connection.close()
            return

        query = "INSERT INTO employees (EmployeeID, Name, Email, EmployeeType, Password) VALUES (%s, %s, %s, %s, %s)"
        data = (employee['EmployeeID'], employee['Name'], employee['Email'], employee['EmployeeType'], employee['Password'])

        try:
            cursor.execute(query, data)
            connection.commit()
            messagebox.showinfo("Success", "Employee added successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
        finally:
            connection.close()
