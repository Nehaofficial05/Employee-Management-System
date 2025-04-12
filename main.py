### db_config.py
import mysql.connector

def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="your_username",
        password="your_password",
        database="employee_database"
    )


### main.py
import tkinter as tk
from employee_page import open_employee_window
from department_page import open_department_window
from salary_page import open_salary_window
from performance_page import open_performance_window

root = tk.Tk()
root.title("Employee Management System")
root.geometry("400x400")

tk.Label(root, text="Welcome to Employee Management System", font=("Arial", 14)).pack(pady=20)

tk.Button(root, text="Manage Employees", width=30, command=open_employee_window).pack(pady=10)
tk.Button(root, text="Manage Departments", width=30, command=open_department_window).pack(pady=10)
tk.Button(root, text="Manage Salaries", width=30, command=open_salary_window).pack(pady=10)
tk.Button(root, text="Manage Performance", width=30, command=open_performance_window).pack(pady=10)

root.mainloop()


### employee_page.py
import tkinter as tk
from tkinter import ttk, messagebox
from db_config import connect_db

def open_employee_window():
    win = tk.Toplevel()
    win.title("Employee Records")
    win.geometry("900x500")

    table = ttk.Treeview(win, columns=("ID", "First", "Last", "Email"), show='headings')
    for col in ("ID", "First", "Last", "Email"):
        table.heading(col, text=col)
        table.column(col, width=200)
    table.pack(expand=True, fill='both', padx=10, pady=10)

    def fetch_employees():
        try:
            db = connect_db()
            cursor = db.cursor()
            cursor.execute("SELECT employee_id, first_name, last_name, email FROM employees")
            rows = cursor.fetchall()
            for row in table.get_children():
                table.delete(row)
            for row in rows:
                table.insert("", tk.END, values=row)
        except Exception as e:
            messagebox.showerror("DB Error", str(e))
        finally:
            cursor.close()
            db.close()

    fetch_employees()


### department_page.py
import tkinter as tk
from tkinter import ttk, messagebox
from db_config import connect_db

def open_department_window():
    win = tk.Toplevel()
    win.title("Department Records")
    win.geometry("700x400")

    table = ttk.Treeview(win, columns=("ID", "Name", "Location", "Email"), show='headings')
    for col in ("ID", "Name", "Location", "Email"):
        table.heading(col, text=col)
        table.column(col, width=150)
    table.pack(expand=True, fill='both', padx=10, pady=10)

    def fetch_departments():
        try:
            db = connect_db()
            cursor = db.cursor()
            cursor.execute("SELECT department_id, department_name, department_location, department_email FROM departments")
            rows = cursor.fetchall()
            for row in table.get_children():
                table.delete(row)
            for row in rows:
                table.insert("", tk.END, values=row)
        except Exception as e:
            messagebox.showerror("DB Error", str(e))
        finally:
            cursor.close()
            db.close()

    fetch_departments()


### salary_page.py
import tkinter as tk
from tkinter import ttk, messagebox
from db_config import connect_db

def open_salary_window():
    win = tk.Toplevel()
    win.title("Salary Records")
    win.geometry("700x400")

    table = ttk.Treeview(win, columns=("ID", "Employee ID", "Amount", "Payment Date"), show='headings')
    for col in ("ID", "Employee ID", "Amount", "Payment Date"):
        table.heading(col, text=col)
        table.column(col, width=150)
    table.pack(expand=True, fill='both', padx=10, pady=10)

    def fetch_salaries():
        try:
            db = connect_db()
            cursor = db.cursor()
            cursor.execute("SELECT salary_id, employee_id, salary_amount, payment_date FROM salaries")
            rows = cursor.fetchall()
            for row in table.get_children():
                table.delete(row)
            for row in rows:
                table.insert("", tk.END, values=row)
        except Exception as e:
            messagebox.showerror("DB Error", str(e))
        finally:
            cursor.close()
            db.close()

    fetch_salaries()


### performance_page.py
import tkinter as tk
from tkinter import ttk, messagebox
from db_config import connect_db

def open_performance_window():
    win = tk.Toplevel()
    win.title("Performance Records")
    win.geometry("800x400")

    table = ttk.Treeview(win, columns=("ID", "Employee ID", "Review Date", "Rating", "Comments"), show='headings')
    for col in ("ID", "Employee ID", "Review Date", "Rating", "Comments"):
        table.heading(col, text=col)
        table.column(col, width=150)
    table.pack(expand=True, fill='both', padx=10, pady=10)

    def fetch_performance():
        try:
            db = connect_db()
            cursor = db.cursor()
            cursor.execute("SELECT performance_id, employee_id, review_date, rating, comments FROM performance")
            rows = cursor.fetchall()
            for row in table.get_children():
                table.delete(row)
            for row in rows:
                table.insert("", tk.END, values=row)
        except Exception as e:
            messagebox.showerror("DB Error", str(e))
        finally:
            cursor.close()
            db.close()

    fetch_performance()
