import tkinter as tk
from tkinter import ttk, messagebox
from db_config import connect_db

def open_salary_window():
    win = tk.Toplevel()
    win.title("Salary Records")
    win.geometry("900x500")

    # Table
    table = ttk.Treeview(win, columns=("ID", "Employee ID", "Salary Amount", "Payment Date"), show='headings')
    for col in ("ID", "Employee ID", "Salary Amount", "Payment Date"):
        table.heading(col, text=col)
        table.column(col, width=150)
    table.pack(expand=True, fill='both', padx=10, pady=10)

    # Input fields
    frame = tk.Frame(win)
    frame.pack(pady=10)
    tk.Label(frame, text="Employee ID").grid(row=0, column=0)
    emp_id_entry = tk.Entry(frame)
    emp_id_entry.grid(row=0, column=1)

    tk.Label(frame, text="Salary Amount").grid(row=0, column=2)
    salary_amount_entry = tk.Entry(frame)
    salary_amount_entry.grid(row=0, column=3)

    tk.Label(frame, text="Payment Date (YYYY-MM-DD)").grid(row=0, column=4)
    payment_date_entry = tk.Entry(frame)
    payment_date_entry.grid(row=0, column=5)

    def fetch_salaries():
        try:
            db = connect_db()
            cursor = db.cursor()
            cursor.execute("SELECT * FROM salaries")
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

    def add_salary():
        emp_id = emp_id_entry.get()
        salary_amount = salary_amount_entry.get()
        payment_date = payment_date_entry.get()
        if not (emp_id and salary_amount and payment_date):
            messagebox.showwarning("Input Error", "All fields required")
            return
        try:
            db = connect_db()
            cursor = db.cursor()
            cursor.execute("INSERT INTO salaries (employee_id, salary_amount, payment_date) VALUES (%s, %s, %s)", 
                           (emp_id, salary_amount, payment_date))
            db.commit()
            fetch_salaries()
            messagebox.showinfo("Success", "Salary record added")
        except Exception as e:
            messagebox.showerror("Insert Error", str(e))
        finally:
            cursor.close()
            db.close()

    def delete_salary():
        selected = table.selection()
        if not selected:
            messagebox.showwarning("Select Row", "Please select a row to delete")
            return
        sal_id = table.item(selected[0])['values'][0]
        try:
            db = connect_db()
            cursor = db.cursor()
            cursor.execute("DELETE FROM salaries WHERE salary_id = %s", (sal_id,))
            db.commit()
            fetch_salaries()
            messagebox.showinfo("Deleted", "Salary record deleted")
        except Exception as e:
            messagebox.showerror("Delete Error", str(e))
        finally:
            cursor.close()
            db.close()

    tk.Button(win, text="Add Salary", command=add_salary).pack(pady=5)
    tk.Button(win, text="Delete Selected", command=delete_salary).pack(pady=5)

    fetch_salaries()
