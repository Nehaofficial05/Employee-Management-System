import tkinter as tk
from tkinter import ttk, messagebox
from db_config import connect_db

def open_salary_window():
    win = tk.Toplevel()
    win.title("Salary Records")
    win.geometry("800x500")
    win.config(bg='#FFE4E1')  # Light pink background

    style = ttk.Style()
    style.theme_use("clam")

    style.configure("Treeview",
                    background="#FFFFFF",  # White rows
                    foreground="black",
                    rowheight=25,
                    fieldbackground="#FFFFFF")

    style.configure("Treeview.Heading",
                    font=('Arial', 12, 'bold'),
                    background="#FFB6C1",  # Light pink header
                    foreground="black",
                    padding=(10, 5))

    style.map("Treeview",
              background=[('selected', '#FF69B4')],  # Hot pink selection
              foreground=[('selected', 'white')])

    table = ttk.Treeview(win, columns=("ID", "Employee ID", "Amount", "Payment Date"), show='headings')
    table.heading("ID", text="Salary ID")
    table.heading("Employee ID", text="Employee ID")
    table.heading("Amount", text="Amount")
    table.heading("Payment Date", text="Payment Date")

    table.column("ID", width=100, anchor='center')
    table.column("Employee ID", width=150, anchor='center')
    table.column("Amount", width=150, anchor='center')
    table.column("Payment Date", width=150, anchor='center')

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

    # Function for inserting a new salary record
    def insert_salary():
        def save_salary():
            try:
                employee_id = entry_employee_id.get()
                amount = entry_amount.get()
                payment_date = entry_payment_date.get()

                if not employee_id or not amount or not payment_date:
                    messagebox.showwarning("Input Error", "All fields are required")
                    return

                db = connect_db()
                cursor = db.cursor()
                cursor.execute("""
                    INSERT INTO salaries (employee_id, salary_amount, payment_date)
                    VALUES (%s, %s, %s)
                """, (employee_id, amount, payment_date))
                db.commit()
                messagebox.showinfo("Success", "Salary record added successfully")
                fetch_salaries()
                add_window.destroy()

            except Exception as e:
                messagebox.showerror("DB Error", str(e))
            finally:
                cursor.close()
                db.close()

        # Add Salary Window
        add_window = tk.Toplevel()
        add_window.title("Add New Salary Record")
        add_window.geometry("400x300")
        add_window.config(bg='#FFE4E1')

        tk.Label(add_window, text="Employee ID", bg='#FFE4E1').pack(pady=5)
        entry_employee_id = tk.Entry(add_window)
        entry_employee_id.pack(pady=5)

        tk.Label(add_window, text="Salary Amount", bg='#FFE4E1').pack(pady=5)
        entry_amount = tk.Entry(add_window)
        entry_amount.pack(pady=5)

        tk.Label(add_window, text="Payment Date", bg='#FFE4E1').pack(pady=5)
        entry_payment_date = tk.Entry(add_window)
        entry_payment_date.pack(pady=5)

        tk.Button(add_window, text="Save", command=save_salary).pack(pady=10)

    # Function for updating a salary record
    def update_salary():
        def save_update():
            try:
                selected_item = table.selection()
                if not selected_item:
                    messagebox.showwarning("Selection Error", "Please select a record to update")
                    return

                salary_id = table.item(selected_item)["values"][0]
                employee_id = entry_employee_id.get()
                amount = entry_amount.get()
                payment_date = entry_payment_date.get()

                if not employee_id or not amount or not payment_date:
                    messagebox.showwarning("Input Error", "All fields are required")
                    return

                db = connect_db()
                cursor = db.cursor()
                cursor.execute("""
                    UPDATE salaries
                    SET employee_id = %s, salary_amount = %s, payment_date = %s
                    WHERE salary_id = %s
                """, (employee_id, amount, payment_date, salary_id))
                db.commit()
                messagebox.showinfo("Success", "Salary record updated successfully")
                fetch_salaries()
                update_window.destroy()

            except Exception as e:
                messagebox.showerror("DB Error", str(e))
            finally:
                cursor.close()
                db.close()

        # Update Salary Window
        selected_item = table.selection()
        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select a record to update")
            return

        salary_id = table.item(selected_item)["values"][0]
        employee_id = table.item(selected_item)["values"][1]
        amount = table.item(selected_item)["values"][2]
        payment_date = table.item(selected_item)["values"][3]

        update_window = tk.Toplevel()
        update_window.title("Update Salary Record")
        update_window.geometry("400x300")
        update_window.config(bg='#FFE4E1')

        tk.Label(update_window, text="Employee ID", bg='#FFE4E1').pack(pady=5)
        entry_employee_id = tk.Entry(update_window)
        entry_employee_id.insert(0, employee_id)
        entry_employee_id.pack(pady=5)

        tk.Label(update_window, text="Salary Amount", bg='#FFE4E1').pack(pady=5)
        entry_amount = tk.Entry(update_window)
        entry_amount.insert(0, amount)
        entry_amount.pack(pady=5)

        tk.Label(update_window, text="Payment Date", bg='#FFE4E1').pack(pady=5)
        entry_payment_date = tk.Entry(update_window)
        entry_payment_date.insert(0, payment_date)
        entry_payment_date.pack(pady=5)

        tk.Button(update_window, text="Save Changes", command=save_update).pack(pady=10)

    # Function for deleting a salary record
    def delete_salary():
        selected_item = table.selection()
        if not selected_item:
            messagebox.showwarning("Selection Error", "Please select a record to delete")
            return

        salary_id = table.item(selected_item)["values"][0]

        try:
            db = connect_db()
            cursor = db.cursor()
            cursor.execute("DELETE FROM salaries WHERE salary_id = %s", (salary_id,))
            db.commit()
            messagebox.showinfo("Success", "Salary record deleted successfully")
            fetch_salaries()

        except Exception as e:
            messagebox.showerror("DB Error", str(e))
        finally:
            cursor.close()
            db.close()

    # CRUD Buttons
    tk.Button(win, text="Add Salary", width=20, command=insert_salary, bg="#FFB6C1").pack(pady=10)
    tk.Button(win, text="Update Salary", width=20, command=update_salary, bg="#FFB6C1").pack(pady=10)
    tk.Button(win, text="Delete Salary", width=20, command=delete_salary, bg="#FFB6C1").pack(pady=10)
