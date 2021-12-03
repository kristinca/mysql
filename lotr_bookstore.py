import mysql.connector
import tkinter as tk
from tkinter import ttk
from calendartime import DTP


# class based gui

class MyApp(tk.Tk):
    """The app"""

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.title('LOTR bookstore')
        self.iconbitmap('')
        self.geometry('800x600')
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.resizable(False, False)

        container = tk.Frame(self)
        container.pack(side='top', fill='both', expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        container.config(bg='#FFAB49')

        frame = tk.Frame(self)
        frame.pack()

        frame1 = FrameOne(parent=container, controller=self)
        frame1.pack()


class FrameOne(tk.Frame):
    """The only frame this app has"""

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.controller = controller

        self.config(bg='#FFAB49')

        self.rent1 = ' '
        self.return1 = ' '

        # entry widgets + labels

        first_name_label = tk.Label(self, text='First Name', font='bold, 15', bg='#FFAB49')
        first_name_label.grid(row=0, column=0, pady=10)

        self.enter_first_name = tk.Entry(self, width=20, borderwidth=5)
        self.enter_first_name.grid(row=1, column=0, padx=50)

        last_name_label = tk.Label(self, text='Last Name', font='bold, 15', bg='#FFAB49')
        last_name_label.grid(row=0, column=1, pady=10)

        self.enter_last_name = tk.Entry(self, width=20, borderwidth=5)
        self.enter_last_name.grid(row=1, column=1, padx=50)

        book_name_label = tk.Label(self, text='Book', font='bold, 15', bg='#FFAB49')
        book_name_label.grid(row=0, column=2, pady=10)

        self.enter_book_name = tk.Entry(self, width=20, borderwidth=5)
        self.enter_book_name.grid(row=1, column=2, padx=50)

        # buttons

        button_enter = tk.Button(self, text='ENTER', font='bold, 18', command=lambda: self.insert_values(),
                                 bg='#FBDB48', borderwidth=8, relief="raised")
        button_enter.grid(row=2, column=1, padx=60, pady=40)

        button_update = tk.Button(self, text='UPDATE', font='bold, 18', command=lambda: self.update_return_date(),
                                  bg='#FBDB48', borderwidth=8, relief="raised")
        button_update.grid(row=2, column=2, padx=60, pady=40)

        button_delete = tk.Button(self, text='DELETE', font='bold, 18', command=lambda: self.delete_values(),
                                  bg='#FBDB48', borderwidth=8, relief="raised")
        button_delete.grid(row=2, column=3, padx=60, pady=40)

        # date time picker

        self.enter_rent_date_btn = tk.Button(self, text='Rent Date', font='bold, 12', bg='#FBDB48',
                                             command=lambda: self.get_rent_date(),
                                             borderwidth=8, relief="raised")
        self.enter_rent_date_btn.grid(row=1, column=3, padx=50)

        self.enter_return_date_btn = tk.Button(self, text='Return Date', font='bold, 12', bg='#FBDB48',
                                             command=lambda: self.get_return_date(),
                                             borderwidth=8, relief="raised")
        self.enter_return_date_btn.grid(row=1, column=4, padx=50)

        # database

        # setup treeview
        columns = ('First Name', 'Last Name', 'Book', 'Rent Date', 'Return Date')
        self.tree = ttk.Treeview(self, columns=columns, show='headings')
        self.tree.grid(row=3, column=1, columnspan=3, pady=30, sticky='news')

        # setup columns attributes
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150, anchor=tk.CENTER)
        style = ttk.Style()
        style.configure("Treeview.Heading", font=(None, 14))
        style.configure("Treeview.Column", font=(None, 14))

        # fetch data
        self.my_cursor.execute('SELECT * FROM users LEFT JOIN books ON users.book_name=books.book_name '
                               'UNION SELECT * FROM users RIGHT JOIN books ON users.book_name=books.book_name '
                               'GROUP BY users.book_name, books.book_name')

        for r in tuple(set(self.my_cursor.fetchall())):
            r1 = list(r)
            del r1[2]
            self.tree.insert('', 'end', value=tuple(r1))

    def rent_date(self):

        self.rent1 = self.dtp.app_data["dt"]

    def return1_date(self):

        self.return1 = self.dtp.app_data["dt"]

    def get_rent_date(self):
        self.dtp = DTP('Rented')
        self.dtp.grid()

    def get_return_date(self):
        self.dtp = DTP('Returned')
        self.dtp.grid()

    def update_table(self):
        self.my_cursor.execute('SELECT * FROM users LEFT JOIN books ON users.book_name=books.book_name '
                               'UNION SELECT * FROM users RIGHT JOIN books ON users.book_name=books.book_name '
                               'GROUP BY users.book_name, books.book_name')
        self.cfall = list(tuple(set(self.my_cursor.fetchall()))).copy()
        self.my_cursor.fetchall().clear()
        self.tree.destroy()
        # setup treeview
        columns = ('First Name', 'Last Name', 'Book', 'Rent Date', 'Return Date')
        self.tree = ttk.Treeview(self, columns=columns, show='headings')
        self.tree.grid(row=3, column=1, columnspan=3, pady=30, sticky='news')

        # setup columns attributes
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150, anchor=tk.CENTER)
        style = ttk.Style()
        style.configure("Treeview.Heading", font=(None, 14))
        style.configure("Treeview.Column", font=(None, 14))
        for r in self.cfall:
            r1 = list(r)
            del r1[2]
            self.tree.insert('', 'end', value=tuple(r1))
        # self.after(1000, self.update_table)

    def insert_values(self):
        self.rent_date()
        self.return1_date()
        print(self.return1)
        print(self.rent1)
        self.my_cursor.execute(f"SELECT * FROM books WHERE book_name='{self.enter_book_name.get()}'")

        try:
            # the book is already in the db table

            self.my_cursor.execute("SET foreign_key_checks=0")

            self.my_cursor.execute(f"UPDATE books SET rent_datetime='{self.rent1}', "
                                   f"return_datetime='{self.return1}' "
                                   f"WHERE book_name='{self.book_name}' ")

            self.my_cursor.execute(f"UPDATE users SET first_name='{self.enter_first_name.get()}', "
                                   f"last_name='{self.enter_last_name.get()}', "
                                   f"WHERE book_name='{self.my_cursor.fetchone()[0]}'")

            self.my_cursor.execute("SET foreign_key_checks=1")

        except TypeError:
            # the book is not in the db table
            self.my_cursor.execute(f"INSERT INTO books VALUES('{self.enter_book_name.get()}',"
                                   f"'{self.rent1}', '{self.return1}') ")
            self.my_cursor.execute(f"INSERT INTO users VALUES('{self.enter_first_name.get()}',"
                                   f"'{self.enter_last_name.get()}', '{self.enter_book_name.get()}')")

        self.mydb.commit()
        self.update_table()

    def delete_values(self):
        self.my_cursor.execute("SET foreign_key_checks=0")
        self.my_cursor.execute(f"SELECT book_name FROM users "
                               f"WHERE first_name='{self.enter_first_name.get()}'")
        self.book_name = self.my_cursor.fetchone()[0]
        # print(self.book_name[0])

        self.my_cursor.execute(f"DELETE FROM books WHERE book_name='{self.book_name}'")
        self.my_cursor.execute(f"DELETE FROM users WHERE first_name='{self.enter_first_name.get()}'")

        self.mydb.commit()
        self.update_table()

    def update_return_date(self):
        self.return1_date()
        self.my_cursor.execute(f"SELECT * FROM books WHERE book_name='{self.enter_book_name.get()}'")
        self.book_name = self.my_cursor.fetchone()[0]
        # print(self.book_name)

        self.my_cursor.execute(f"UPDATE books SET return_datetime='{self.return1}' "
                               f"WHERE book_name='{self.book_name}'")

        self.mydb.commit()
        self.update_table()


if __name__ == '__main__':
    app = MyApp()
    app.mainloop()
