from tkinter import *
from tkinter import messagebox
from sql_connection import get_sql_connection




class AddBook(Toplevel):
    def __init__(self):
        Toplevel.__init__(self)
        self.geometry("650x750+550+200")
        self.title("Add Book")
        self.resizable(False,False)

######################################FRAMES######################################################
        #top frame
        self.topframe= Frame(self,height=150,bg='white')
        self.topframe.pack(fill=X)
        #bottom frame
        self.bottomFrame= Frame(self,height=600,bg='#87CEEB')
        self.bottomFrame.pack(fill=X)
        #heading
        self.top_image= PhotoImage(file='icons/addbook.png')
        top_image_lbl=Label(self.topframe,image=self.top_image,bg='white')
        top_image_lbl.place(x=120,y=20)
        heading=Label(self.topframe, text ='   Add Book   ',font='arial 22 bold',fg='#003f8a',bg='white')
        heading.place(x=290,y=60)

######################################LABELS######################################################
        
        #Title
        self.title=Label(self.bottomFrame,text='Title: ',font='arial 15 bold',fg='white',bg='#87CEEB')
        self.title.place(x=40,y=40)
        self.ent_title=Entry(self.bottomFrame,width=30,bd=4)
        self.ent_title.insert(0,'Please enter the book title')
        self.ent_title.place(x=300,y=45)
        #Author
        self.author=Label(self.bottomFrame,text='Author: ',font='arial 15 bold',fg='white',bg='#87CEEB')
        self.author.place(x=40,y=80)
        self.ent_author=Entry(self.bottomFrame,width=30,bd=4)
        self.ent_author.insert(0,'Please enter the book author')
        self.ent_author.place(x=300,y=85)
        #ISBN
        self.isbn = Label(self.bottomFrame, text='ISBN: ', font='arial 15 bold', fg='white', bg='#87CEEB')
        self.isbn.place(x=40, y=120)
        self.ent_isbn = Entry(self.bottomFrame, width=30, bd=4)
        self.ent_isbn.insert(0, 'Please enter the book ISBN')
        self.ent_isbn.place(x=300, y=125)
        #Genre
        self.genre = Label(self.bottomFrame, text='Genre: ', font='arial 15 bold', fg='white', bg='#87CEEB')
        self.genre.place(x=40, y=160)
        self.ent_genre = Entry(self.bottomFrame, width=30, bd=4)
        self.ent_genre.insert(0, 'Please enter the book Genre')
        self.ent_genre.place(x=300, y=165)
        #Quantity
        self.quantity_label = Label(self.bottomFrame, text='Quantity: ', font='arial 15 bold', fg='white', bg='#87CEEB')
        self.quantity_label.place(x=40, y=200)
        self.ent_quantity = Entry(self.bottomFrame, width=30, bd=4)
        self.ent_quantity.insert(0, 'Please enter the book Quantity')
        self.ent_quantity.place(x=300, y=205)
        #ShelfLocation
        self.shelf_location_label = Label(self.bottomFrame, text='Location: ', font='arial 15 bold', fg='white', bg='#87CEEB')
        self.shelf_location_label.place(x=40, y=240)
        self.ent_shelf_location = Entry(self.bottomFrame, width=30, bd=4)
        self.ent_shelf_location.insert(0, 'Please enter the Shelf Location')
        self.ent_shelf_location.place(x=300, y=245)
        #button
        button=Button(self.bottomFrame,text='Add Book',command=self.addBook)
        button.place(x=550,y=300)




    def addBook(self):
        book = {
            'Title': self.ent_title.get(),
            'Author': self.ent_author.get(),
            'ISBN': self.ent_isbn.get(),
            'Genre': self.ent_genre.get(),
            'ShelfLocation': self.ent_shelf_location.get(),
            'Quantity': self.ent_quantity.get()
        }

        connection = get_sql_connection()
        if not connection:
            messagebox.showerror("Error", "Could not connect to database.")
            return

        isbn = book['ISBN']

        cursor = connection.cursor()
        query = "SELECT * FROM lib.books WHERE ISBN = %s"
        cursor.execute(query, (isbn,))
        result = cursor.fetchone()

        if result:
            messagebox.showerror("Error", f"Book with ISBN {isbn} already exists in the database.")
            connection.close()
            return

        query = "INSERT INTO lib.books (Title, Author, ISBN, Genre, ShelfLocation, Quantity, Status) VALUES (%s, %s, %s, %s, %s, %s, 'Available')"
        data = (book['Title'], book['Author'], book['ISBN'], book['Genre'], book['ShelfLocation'], book['Quantity'])

        try:
            cursor.execute(query, data)
            connection.commit()
            messagebox.showinfo("Success", "Book added successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
        finally:
            connection.close()
