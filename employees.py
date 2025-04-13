import tkinter as tk
from tkinter import ttk, messagebox
from db_config import connect_db

def open_employee_window():
    win = tk.Toplevel()
    win.title("Employee Records")
    win.geometry("950x600")
    win.config(bg='#FFE4E1')  # Light pink background

    # ====== Styles ======
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Treeview",
                    background="#FFFFFF",
                    foreground="black",
                    rowheight=25,
                    fieldbackground="#FFFFFF")
    style.configure("Treeview.Heading",
                    font=('Arial', 12, 'bold'),
                    background="#FFB6C1",
                    foreground="black")
    style.map("Treeview",
              background=[('selected', '#FF69B4')],
              foreground=[('selected', 'white')])

    # ====== Entry Form ======
    tk.Label(win, text="First Name:", bg='#FFE4E1').place(x=30, y=20)
    first_name_entry = tk.Entry(win, width=30)
    first_name_entry.place(x=130, y=20)

    tk.Label(win, text="Last Name:", bg='#FFE4E1').place(x=30, y=60)
    last_name_entry = tk.Entry(win, width=30)
    last_name_entry.place(x=130, y=60)

    tk.Label(win, text="Email:", bg='#FFE4E1').place(x=30, y=100)
    email_entry = tk.Entry(win, width=30)
    email_entry.place(x=130, y=100)

    # ====== Treeview Table ======
    table = ttk.Treeview(win, columns=("ID", "First Name", "Last Name", "Email"), show='headings', height=10)
    table.heading("ID", text="Employee ID")
    table.heading("First Name", text="First Name")
    table.heading("Last Name", text="Last Name")
    table.heading("Email", text="Email")
    table.column("ID", width=100, anchor='center')
    table.column("First Name", width=200, anchor='w')
    table.column("Last Name", width=200, anchor='w')
    table.column("Email", width=300, anchor='w')
    table.place(x=30, y=150, width=880)

    # ====== CRUD Functions ======
    def fetch_employees():
        try:
            db = connect_db()
            cursor = db.cursor()
            cursor.execute("SELECT employee_id, first_name, last_name, email FROM employees")
            rows = cursor.fetchall()
            table.delete(*table.get_children())
            for row in rows:
                table.insert("", tk.END, values=row)
        except Exception as e:
            messagebox.showerror("Fetch Error", str(e))
        finally:
            cursor.close()
            db.close()


    def insert_employee():
        fname = first_name_entry.get()
        lname = last_name_entry.get()
        email = email_entry.get()
        if fname and lname and email:
            try:
                db = connect_db()
                cursor = db.cursor()
                cursor.execute("INSERT INTO employees (first_name, last_name, email) VALUES (%s, %s, %s)", 
                               (fname, lname, email))
                db.commit()
                messagebox.showinfo("Success", "Employee added!")
                fetch_employees()
                clear_form()
            except Exception as e:
                messagebox.showerror("Insert Error", str(e))
            finally:
                cursor.close()
                db.close()
        else:
            messagebox.showwarning("Input Error", "Please fill in all fields.")

    def update_employee():
        selected = table.focus()
        if not selected:
            messagebox.showwarning("Select Record", "Please select a record to update.")
            return
        employee_id = table.item(selected)['values'][0]
        fname = first_name_entry.get()
        lname = last_name_entry.get()
        email = email_entry.get()
        if fname and lname and email:
            try:
                db = connect_db()
                cursor = db.cursor()
                cursor.execute(
                    "UPDATE employees SET first_name=%s, last_name=%s, email=%s WHERE employee_id=%s",
                    (fname, lname, email, employee_id)
                )
                db.commit()
                messagebox.showinfo("Success", "Record updated.")
                fetch_employees()
                clear_form()
            except Exception as e:
                messagebox.showerror("Update Error", str(e))
            finally:
                cursor.close()
                db.close()
        else:
            messagebox.showwarning("Input Error", "All fields required for update.")

    def delete_employee():
        selected = table.focus()
        if not selected:
            messagebox.showwarning("Select Record", "Please select a record to delete.")
            return
        employee_id = table.item(selected)['values'][0]
        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this employee?")
        if confirm:
            try:
                db = connect_db()
                cursor = db.cursor()
                cursor.execute("DELETE FROM employees WHERE employee_id=%s", (employee_id,))
                db.commit()
                messagebox.showinfo("Deleted", "Employee deleted successfully.")
                fetch_employees()
                clear_form()
            except Exception as e:
                messagebox.showerror("Delete Error", str(e))
            finally:
                cursor.close()
                db.close()

    def select_record(event):
        selected = table.focus()
        if selected:
            values = table.item(selected, 'values')
            first_name_entry.delete(0, tk.END)
            last_name_entry.delete(0, tk.END)
            email_entry.delete(0, tk.END)
            first_name_entry.insert(0, values[1])
            last_name_entry.insert(0, values[2])
            email_entry.insert(0, values[3])

    def clear_form():
        first_name_entry.delete(0, tk.END)
        last_name_entry.delete(0, tk.END)
        email_entry.delete(0, tk.END)

    # ====== Buttons ======
    tk.Button(win, text="Add", bg="#FFB6C1", width=12, command=insert_employee).place(x=450, y=20)
    tk.Button(win, text="Update", bg="#FFB6C1", width=12, command=update_employee).place(x=450, y=60)
    tk.Button(win, text="Delete", bg="#FFB6C1", width=12, command=delete_employee).place(x=450, y=100)
    tk.Button(win, text="Clear", bg="#FFDDEE", width=12, command=clear_form).place(x=580, y=60)

    # ====== Bind Events ======
    table.bind("<ButtonRelease-1>", select_record)

    # Initial Data Load
    fetch_employees()
