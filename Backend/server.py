import tkinter as tk

root = tk.Tk()

root.geometry("500x500")
root.title("THE LIBRARY OF THE PEOPLE")

label = tk.Label(root, text="Hello Readers", font=('Arial,18'))
label.pack()

root.mainloop()