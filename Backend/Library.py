from tkinter import *
from tkinter import ttk
from tkinter import PhotoImage
from tkinter import messagebox
import datetime
import mysql.connector
import Books
import login,addbook,addmember,deletebook,deletemember,editbook,editmember,newloan,endloan,statistics,statistics1,statistics2,statistics3,addemployee,deleteemployee,waitinglist
import os

connection = mysql.connector.connect(user='root', password='amersaid95', database='lib')
cur = connection.cursor()



class Main():
    def __init__(self,master):

        self.master = master


        def displayLoans(self):
            self.list_loans.delete(0, END)

            cur.execute("SELECT * FROM lib.loans")
            loans = cur.fetchall()
            count = 0
            for loan in loans:
                print(loan)
                loan_id = str(loan[0])  # Convert loan ID to string
                book_id = str(loan[1]) 
                member_id = str(loan[2])
                loan_date = str(loan[3])
                loan_return = str(loan[4])

                # Concatenate loan details into a single string
                loan_info = f'LoanID: {loan_id} - BookID: {book_id} - MemberID: {member_id} - Loan Date: {loan_date} - Return Date: {loan_return}'

                # Insert loan details into the listbox
                self.list_loans.insert(count, loan_info)
        
        def displayBooks(self):
            self.list_loans.delete(0, END)

            self.cur.execute("SELECT * FROM lib.books")
            books = self.cur.fetchall()
            for book in books:
                book_info = f"BookID: {book[0]}\nTitle: {book[1]}\nISBN: {book[2]}\nAuthor: {book[3]}\nGenre: {book[4]}\nShelf Location: {book[5]}\nQuantity: {book[6]}\nStatus: {book[7]}"
                for line in book_info.split('\n'):
                    self.list_loans.insert(END, line)
                self.list_loans.insert(END, '')


               

        #frames
        mainFrame=Frame(self.master)
        mainFrame.pack()
        #top frames
        topFrame= Frame(mainFrame,width=1350,height=70,bg='#f8f8f8',padx=20,relief=SUNKEN,borderwidth=2)
        topFrame.pack(side=TOP,fill=X)
        #top 2 frames
        top2Frame= Frame(mainFrame,width=1350,height=70,bg='#f8f8f8',padx=20,relief=SUNKEN,borderwidth=2)
        top2Frame.pack(side=TOP,fill=X)
        #center frame
        centerFrame= Frame(mainFrame,width=1350,relief=RIDGE,bg='#e0f0f0',height=680,borderwidth=5)
        centerFrame.pack(side=TOP)
        #center left frame
        centerLeftFrame=Frame(centerFrame,width=900,height=700,bg='#e0f0f0',borderwidth=2,relief='sunken')
        centerLeftFrame.pack(side=LEFT)
        #center right frame
        centerRightFrame=Frame(centerFrame,width=450,height=700,bg='#e0f0f0',borderwidth=2,relief='sunken')
        centerRightFrame.pack(side=RIGHT)

###################################################################################################        

        # Add Book
        self.iconbook=PhotoImage(file='icons/addbook.png')
        self.btnbook = Button(topFrame,text='Add Book   ',image=self.iconbook,compound=LEFT,
                              font='arial 12 bold',command=self.addBook)
        self.btnbook.pack(side=LEFT,padx=10)

        # Delete Book
        self.icondbook=PhotoImage(file='icons/deletebook.png')
        self.btndbook = Button(topFrame,text='Delete Book',image=self.iconbook,compound=LEFT,
                              font='arial 12 bold',command=self.deleteBook)
        self.btndbook.configure(image=self.icondbook,compound=LEFT)
        self.btndbook.pack(side=LEFT,padx=10)

        # Edit Book
        self.iconebook=PhotoImage(file='icons/editbook.png')
        self.btnebook = Button(topFrame,text='Edit Book',image=self.iconbook,compound=LEFT,
                              font='arial 12 bold',command=self.editBook)
        self.btnebook.configure(image=self.iconebook,compound=LEFT)
        self.btnebook.pack(side=LEFT,padx=10)

###################################################################################################
        
        # Add Member
        self.iconmember=PhotoImage(file='icons/add-user.png')
        self.btnmember = Button(topFrame,text='Add Member',font='arial 12 bold',padx=10,command=self.addMember)
        self.btnmember.configure(image=self.iconmember,compound=LEFT)
        self.btnmember.pack(side=LEFT)

        # Delete Member
        self.icondmember=PhotoImage(file='icons/delete-user.png')
        self.btndmember = Button(topFrame,text='Delete Member',image=self.icondmember,compound=LEFT,
                              font='arial 12 bold',command=self.deleteMember)
        self.btndmember.configure(image=self.icondmember,compound=LEFT)
        self.btndmember.pack(side=LEFT,padx=10)

        # Edit Member
        self.iconemember=PhotoImage(file='icons/edit-user.png')
        self.btnemember = Button(topFrame,text='Edit Member',image=self.iconmember,compound=LEFT,
                              font='arial 12 bold',command=self.editMember)
        self.btnemember.configure(image=self.iconemember,compound=LEFT)
        self.btnemember.pack(side=LEFT,padx=10)

        # New Loan
        self.iconloan=PhotoImage(file='icons/loan.png')
        self.btnloan = Button(top2Frame,text='New Loan',font='arial 12 bold',image=self.iconloan,command=self.newLoan)
        self.btnloan.configure(image=self.iconloan,compound=LEFT)
        self.btnloan.pack(side=LEFT,padx=10) 

         # End Loan
        self.iconeloan=PhotoImage(file='icons/borrow.png')
        self.btneloan = Button(top2Frame,text='End Loan',font='arial 12 bold',image=self.iconloan,command=self.endLoan)
        self.btneloan.configure(image=self.iconeloan,compound=LEFT)
        self.btneloan.pack(side=LEFT,padx=10) 

         # Waiting List
        self.iconlist=PhotoImage(file='icons/time.png')
        self.btnlist = Button(top2Frame,text='Waiting List',font='arial 12 bold',image=self.iconloan,command=self.display_books_with_zero_quantity)
        self.btnlist.configure(image=self.iconlist,compound=LEFT)
        self.btnlist.pack(side=LEFT,padx=10) 

    #############################################################################################################
        # Search Book
        search_bar = LabelFrame(centerRightFrame,width=440,height=100,text='Search Book', bg='#87CEEB')
        search_bar.pack(fill=BOTH)
        self.lbl_search=Label(search_bar,text='Enter BookID',bg='#87CEEB',fg='white')
        self.lbl_search.grid(row=0,column=0,padx=20,pady=10)
        self.ent_search=Entry(search_bar,width=25,bd=5)
        self.ent_search.grid(row=0,column=1,columnspan=3,padx=10,pady=10)
        self.btn_search=Button(search_bar,text='Search',font='arial 12',bg='#87CEEB',fg='white',command=self.searchBook)
        self.btn_search.grid(row=0,column=4,padx=20,pady=10)


        # Search Member
        search_bar1 = LabelFrame(centerRightFrame,width=440,height=175,text='Search Member', bg='#87CEEB')
        search_bar1.pack(fill=BOTH)
        self.lbl_search1=Label(search_bar1,text='Enter MemberID',bg='#87CEEB',fg='white')
        self.lbl_search1.grid(row=0,column=0,padx=20,pady=10)
        self.ent_search1=Entry(search_bar1,width=25,bd=5)
        self.ent_search1.grid(row=0,column=1,columnspan=3,padx=10,pady=10)
        self.btn_search1=Button(search_bar1,text='Search',font='arial 12',bg='#87CEEB',fg='white',command=self.searchMember)
        self.btn_search1.grid(row=0,column=4,padx=20,pady=10)

    

        # image
        image=Frame(centerRightFrame,width=440,height=370)
        image.pack(fill=BOTH)
        self.title_right=Label(image,text='Welcome to YVC Library',font='arial 16 bold')
        self.title_right.grid(row=0)
        self.img_library=PhotoImage(file='icons/lib.png')
        self.lblImg=Label(image,image=self.img_library)
        self.lblImg.grid(row=1)

    #############################################################################################################
        # Tabs

        #home page display (loans details)
        
        self.tabs = ttk.Notebook(centerLeftFrame,width=900,height=660)
        self.tabs.pack()
        self.tab1_icon=PhotoImage(file='icons/home.png')
        self.tab2_icon=PhotoImage(file='icons/stats.png')
        self.tab3_icon=PhotoImage(file='icons/manager.png')
        self.tab1=ttk.Frame(self.tabs)
        self.tab2=ttk.Frame(self.tabs)
        self.tab3=ttk.Frame(self.tabs)
        self.tabs.add(self.tab1,text='Home',image=self.tab1_icon,compound=LEFT)
        self.tabs.bind("<Button-1>", lambda event: self.displayloan())
        self.tabs.add(self.tab2,text='Statistics',image=self.tab2_icon,compound=LEFT)
        self.tabs.add(self.tab3,text='Library Management',image=self.tab3_icon,compound=LEFT)
        self.tabs.bind("<<NotebookTabChanged>>", self.on_tab_change)

#######################################################################################################
      
        
        
        #loans list
        self.list_loans= Listbox(self.tab1,width=110,height=30,bd=5,font='times 12 bold')
        self.sb=Scrollbar(self.tab1,orient=VERTICAL)
        self.list_loans.grid(row=0,column=0,padx=(10,0),pady=10,sticky=N)
        self.sb.config(command=self.list_loans.yview)
        self.list_loans.config(yscrollcommand=self.sb.set)
        self.sb.grid(row=0,column=0,sticky=N+S+E)


        self.list_details=Listbox(self.tab1,width=80,height=30,bd=5,font='times 12 bold')
        self.list_details.grid(row=0,column=1,padx=(10,0),pady=10,sticky=N)


        displayLoans(self)
        


    def on_tab_change(self, event):
        current_tab = self.tabs.index("current")
        if current_tab == 0:  
            self.displayLoans()  
        elif current_tab == 1:  
            self.display_buttons()
            self.tabs.unbind("<<NotebookTabChanged>>")
        elif current_tab == 2:
            self.login()



        

    # Define a method to display the buttons for statistics and LM
    def display_buttons(self):
        # Create and pack the buttons for statistics
        button1 = Button(self.tab2, text="Loans per Month", font='arial 12 bold',command=self.statistics)
        button1.pack(side=TOP, pady=10)
        button2 = Button(self.tab2, text="Loans per Periods", font='arial 12 bold',command=self.statistics1)
        button2.pack(side=TOP, pady=10)
        button3 = Button(self.tab2, text="Loans End Stats", font='arial 12 bold',command=self.statistics2)
        button3.pack(side=TOP, pady=10)
        button4 = Button(self.tab2, text="Most Popular Books", font='arial 12 bold',command=self.statistics3)
        button4.pack(side=TOP, pady=10)
        button4 = Button(self.tab3, text=" Login ", font='arial 12 bold',command=self.login)
        button4.pack(side=TOP, pady=10)









    def login(self):
        log=login.Login()
        self.close_connection()

    

    def addBook(self):
        add=addbook.AddBook()
        self.dislayBooks()
        self.close_connection()


    def deleteBook(self):
        delete=deletebook.DeleteBook()
        self.close_connection()

    def editBook(self):
        edit=editbook.EditBook()
        self.close_connection()

 

    def addMember(self):
        add=addmember.AddMember()
        self.close_connection()
    
    def deleteMember(self):
        delete=deletemember.DeleteMember()
        self.close_connection()

    def editMember(self):
        edit=editmember.EditMember()
        self.close_connection()

    def newLoan(self):
        new=newloan.NewLoan()
        self.close_connection()

    def endLoan(self):
        end=endloan.EndLoan()
        self.close_connection()

    def display_books_with_zero_quantity(self):
        dis = waitinglist.WaitingList()
        self.close_connection()

    ##############################################################################################
    # Stats

    def statistics(self):
        stats=statistics.Statistics()
        self.close_connection()

    def statistics1(self):
        stats=statistics1.Statistics()
        self.close_connection()

    def statistics2(self):
        stats=statistics2.Statistics()
        self.close_connection()

    def statistics3(self):
        stats=statistics3.Statistics()
        self.close_connection()


    ##############################################################################################
    # Search Engines

    def searchBook(self):

        # Clear the list box
        self.list_loans.delete(0, END)

        value = self.ent_search.get()
        try:
            cur.execute("SELECT * FROM Books WHERE BookID = %s", (value,))
            search = cur.fetchall()
            for book in search:
                # Construct book details with each detail on a new line
                book_info = f"BookID: {book[0]}\nTitle: {book[1]}\nISBN: {book[2]}\nAuthor: {book[3]}\nGenre: {book[4]}\nShelf Location: {book[5]}\nQuantity: {book[6]}\nStatus: {book[7]}"
                # Split book_info into lines and insert each line separately
                for line in book_info.split('\n'):
                    self.list_loans.insert(END, line)
                # Insert an empty line between books
                self.list_loans.insert(END, '')  
        except Exception as e:
            print("An error occurred:", e)

    def searchMember(self):
        # Clear the list box
        self.list_loans.delete(0, END)

        value = self.ent_search1.get()
        try:
            cur.execute("SELECT * FROM lib.member WHERE MemberID = %s", (value,))
            search = cur.fetchall()
            for member in search:
                # Construct member details with each detail on a new line
                member_info = f"MemberID: {member[0]}\nName: {member[1]}\nEmail: {member[2]}\nPhone: {member[3]}\nMembership Type: {member[4]}\nMembership Start Date: {member[5]}"
                # Split member_info into lines and insert each line separately
                for line in member_info.split('\n'):
                    self.list_loans.insert(END, line)
                # Insert an empty line between members
                self.list_loans.insert(END, '')  
        except Exception as e:
            print("An error occurred:", e)








def main():
    root = Tk()
    app = Main(root)
    root.title("Library Management System")
    root.geometry("1350x750+350+200")
    root.iconbitmap('icons/icon.ico')
    root.mainloop()

if __name__== '__main__':
    main()

    