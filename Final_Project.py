#Пытаемся импортировать модули для работы с базой данных SQLite и для создания графического интерфейса с помощью библиотеки Tkinter.
import sqlite3
from tkinter import *
from tkinter import messagebox
from tkinter import ttk

#Эта функция создает таблицу employee, после создания таблицы, функция сохраняет изменения и закрывает соединение с базой данных.

def create_table():
    conn = sqlite3.connect('employees.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS employees
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT,
                  phone REAL,
                  email TEXT,
                  salary REAL)''')
    
    conn.commit()
    conn.close()

#добавляет нового сотрудника в базу данных 

def add_employee():
    name = name_entry.get()
    phone = phone_entry.get()
    email = email_entry.get()
    salary = salary_entry.get()

    if not name or not phone or not email or not salary:
        messagebox.showerror('Ошибка', 'Заполните все поля')
        return

    conn = sqlite3.connect('employees.db')
    c = conn.cursor()
    c.execute('INSERT INTO employees (name, phone, email, salary) VALUES (?, ?, ?, ?)',
              (name, phone, email, salary))
    conn.commit()
    conn.close()

    load_employees()


#обновляет данные сотрудника в базе данных, проверяет наличие выбранного сотрудника и заполнение всех полей, выводит сообщения об ошибках при их отсутствии


def update_employee():
    selected_item = tree.selection()

    if not selected_item:
        messagebox.showerror('Ошибка', 'Выберите сотрудника')
        return

    name = name_entry.get()
    phone = phone_entry.get()
    email = email_entry.get()
    salary = salary_entry.get()

    if not name or not phone or not email or not salary:
        messagebox.showerror('Ошибка', 'Заполните все поля')
        return

    conn = sqlite3.connect('employees.db')
    c = conn.cursor()
    employee_id = tree.item(selected_item)['values'][0]
    c.execute('UPDATE employees SET name=?, phone=?, email=?, salary=? WHERE id=?', (name, phone, email, salary, employee_id))
    conn.commit()
    conn.close()

    load_employees()

#Этот код реализует функцию которая удаляет выбранных сотрудников

def delete_employee():
    selected_item = tree.selection()

    if not selected_item:
        messagebox.showerror('Ошибка', 'Выберите сотрудника')
        return

    result = messagebox.askyesno('Подтверждение', 'Вы уверены, что хотите удалить сотрудника?')

    if result:
        conn = sqlite3.connect('employees.db')
        c = conn.cursor()
        employee_id = tree.item(selected_item)['values'][0]
        c.execute('DELETE FROM employees WHERE id=?', (employee_id,))
        conn.commit()
        conn.close()

        load_employees()

#общий смысл кода - создание приложения для управления списком сотрудников компании.

def search_employee():
    search_query = search_entry.get()

    conn = sqlite3.connect('employees.db')
    c = conn.cursor()
    c.execute('SELECT * FROM employees WHERE name LIKE ?', ('%{}%'.format(search_query),))
    rows = c.fetchall()
    conn.close()

    tree.delete(*tree.get_children())

    for row in rows:
        tree.insert('', 'end', values=row)

def load_employees():
    conn = sqlite3.connect('employees.db')
    c = conn.cursor()
    c.execute('SELECT * FROM employees')
    rows = c.fetchall()
    conn.close()

    tree.delete(*tree.get_children())

    for row in rows:
        tree.insert('', 'end', values=row)

root = Tk()
root.title('Список сотрудников компании')

frame = Frame(root)
frame.pack(pady=20)

name_label = Label(frame, text='ФИО:')
name_label.grid(row=0, column=0)
name_entry = Entry(frame)
name_entry.grid(row=0, column=1)

phone_label = Label(frame, text='Номер телефона:')
phone_label.grid(row=1, column=0)
phone_entry = Entry(frame)
phone_entry.grid(row=1, column=1)

email_label = Label(frame, text='Адрес электронной почты:')
email_label.grid(row=2, column=0)
email_entry = Entry(frame)
email_entry.grid(row=2, column=1)

salary_label = Label(frame, text='Заработная плата:')
salary_label.grid(row=3, column=0)
salary_entry = Entry(frame)
salary_entry.grid(row=3, column=1)

button_frame = Frame(root)
button_frame.pack(pady=20)

add_button = Button(button_frame, text='Добавить', command=add_employee)
add_button.grid(row=0, column=0)

update_button = Button(button_frame, text='Изменить', command=update_employee)
update_button.grid(row=0, column=1)

delete_button = Button(button_frame, text='Удалить', command=delete_employee)
delete_button.grid(row=0, column=2)

search_entry = Entry(root)
search_entry.pack(pady=10)
search_button = Button(root, text="Поиск", command=search_employee)
search_button.pack()

tree = ttk.Treeview(root, columns=('ID', 'ФИО', 'Телефон', 'Email', 'Зарплата'), show='headings', height=10)
tree.column('ID', width=30, anchor=CENTER)
tree.column('ФИО', width=150, anchor=CENTER)
tree.column('Телефон', width=100, anchor=CENTER)
tree.column('Email', width=150, anchor=CENTER)
tree.column('Зарплата', width=80, anchor=CENTER)

tree.heading('ID', text='ID')
tree.heading('ФИО', text='ФИО')
tree.heading('Телефон', text='Телефон')
tree.heading('Email', text='Email')
tree.heading('Зарплата', text='Зарплата')

tree.pack()

create_table()
load_employees()

root.mainloop()

#Теперь пользователь может изменять, добавлять и удалять сотрудников. Также можно выполнять поиск по имени.
