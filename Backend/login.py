from tkinter import *
from tkinter import messagebox
from sql_connection import get_sql_connection
import deleteemployee,addemployee

class Login():
    def __init__(self):
        self.login_window = Toplevel()
        self.login_window.title("Login")
        self.login_window.geometry("300x150")
        
        self.label_username = Label(self.login_window, text="Username:")
        self.label_password = Label(self.login_window, text="Password:")
        self.entry_username = Entry(self.login_window)
        self.entry_password = Entry(self.login_window, show="*")
        
        self.label_username.grid(row=0, sticky=E)
        self.label_password.grid(row=1, sticky=E)
        self.entry_username.grid(row=0, column=1)
        self.entry_password.grid(row=1, column=1)
        
        self.login_button = Button(self.login_window, text="Login", command=self.login)
        self.login_button.grid(row=2, columnspan=2, pady=5)

    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        connection = get_sql_connection()
        if not connection:
            messagebox.showerror("Error", "Could not connect to database.")
            return

        cursor = connection.cursor()
        
        # Query to check user credentials
        cursor.execute("SELECT * FROM employees WHERE EmployeeID = %s AND Password = %s AND EmployeeType = 'Manager'", (username, password))
        user = cursor.fetchone()
        
        if user:
            messagebox.showinfo("Success", "Login successful")
            self.login_window.destroy()
            # Grant access to management functionalities
            self.display_management_interface()
        else:
            messagebox.showerror("Error", "Invalid username or password")


    def display_management_interface(self):
        top = Toplevel()
        top.geometry("650x750+550+200")
        top.title("Management Interface")
        top.resizable(False, False)

        # Top Frame
        top_frame = Frame(top, height=150, bg='#87CEEB')
        top_frame.pack(fill=X)

        # Bottom Frame
        bottom_frame = Frame(top, height=600, bg='#87CEEB')
        bottom_frame.pack(fill=X)

        # Heading
        heading = Label(top_frame, text='   HELLO BOSS!   ', font='arial 22 bold', fg='#003f8a', bg='white')
        heading.place(x=290, y=60)

        # Add Employee Button
        self.icon_add_employee = PhotoImage(file='icons/add-user.png')
        btn_add_employee = Button(bottom_frame, text='Add Employee', image=self.icon_add_employee, compound=LEFT,
                                font='arial 12 bold', command=self.addEmployee)
        btn_add_employee.pack(side=LEFT, padx=10)

        # Delete Employee Button
        self.icon_delete_employee = PhotoImage(file='icons/delete-user.png')
        btn_delete_employee = Button(bottom_frame, text='Delete Employee', image=self.icon_delete_employee, compound=LEFT,
                                    font='arial 12 bold', command=self.deleteEmployee)
        btn_delete_employee.pack(side=LEFT, padx=10)

    def addEmployee(self):
        add = addemployee.AddEmployee()
        # Optionally close any connections here if needed
    
    def deleteEmployee(self):
        delete = deleteemployee.deleteEmployee()
        # Optionally close any connections here if needed
