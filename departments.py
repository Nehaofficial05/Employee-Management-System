import tkinter as tk
from tkinter import ttk, messagebox
from db_config import connect_db

def open_department_window():
    win = tk.Toplevel()
    win.title("Department Records")
    win.geometry("800x500")
    win.config(bg='#FFE4E1')

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Treeview", background="#FFFFFF", foreground="black", rowheight=25, fieldbackground="#FFFFFF")
    style.configure("Treeview.Heading", font=('Arial', 12, 'bold'), background="#FFB6C1", foreground="black")
    style.map("Treeview", background=[('selected', '#FF69B4')], foreground=[('selected', 'white')])

    tk.Label(win, text="Department Name:", bg='#FFE4E1').place(x=30, y=20)
    dept_entry = tk.Entry(win, width=30)
    dept_entry.place(x=160, y=20)

    table = ttk.Treeview(win, columns=("ID", "Department"), show='headings', height=10)
    table.heading("ID", text="Department ID")
    table.heading("Department", text="Department Name")
    table.column("ID", width=100, anchor='center')
    table.column("Department", width=300, anchor='w')
    table.place(x=30, y=100, width=720)

    def fetch_departments():
        try:
            db = connect_db()
            cursor = db.cursor()
            cursor.execute("SELECT department_id, department_name FROM departments")
            rows = cursor.fetchall()
            table.delete(*table.get_children())
            for row in rows:
                table.insert("", tk.END, values=row)
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            cursor.close()
            db.close()




    def insert_department():
        name = dept_entry.get()
        if name:
            try:
                db = connect_db()
                cursor = db.cursor()
                cursor.execute("INSERT INTO departments (department_name) VALUES (%s)", (name,))
                db.commit()
                fetch_departments()
                dept_entry.delete(0, tk.END)
            except Exception as e:
                messagebox.showerror("Insert Error", str(e))
            finally:
                cursor.close()
                db.close()

    def update_department():
        selected = table.focus()
        if selected:
            dept_id = table.item(selected)['values'][0]
            name = dept_entry.get()
            if name:
                try:
                    db = connect_db()
                    cursor = db.cursor()
                    cursor.execute("UPDATE departments SET department_name=%s WHERE department_id=%s", (name, dept_id))
                    db.commit()
                    fetch_departments()
                    dept_entry.delete(0, tk.END)
                except Exception as e:
                    messagebox.showerror("Update Error", str(e))
                finally:
                    cursor.close()
                    db.close()

    def delete_department():
        selected = table.focus()
        if selected:
            dept_id = table.item(selected)['values'][0]
            confirm = messagebox.askyesno("Confirm", "Delete this department?")
            if confirm:
                try:
                    db = connect_db()
                    cursor = db.cursor()
                    cursor.execute("DELETE FROM departments WHERE department_id=%s", (dept_id,))
                    db.commit()
                    fetch_departments()
                    dept_entry.delete(0, tk.END)
                except Exception as e:
                    messagebox.showerror("Delete Error", str(e))
                finally:
                    cursor.close()
                    db.close()

    def select(event):
        selected = table.focus()
        if selected:
            values = table.item(selected)['values']
            dept_entry.delete(0, tk.END)
            dept_entry.insert(0, values[1])

    table.bind("<ButtonRelease-1>", select)

    tk.Button(win, text="Add", bg="#FFB6C1", width=12, command=insert_department).place(x=500, y=20)
    tk.Button(win, text="Update", bg="#FFB6C1", width=12, command=update_department).place(x=620, y=20)
    tk.Button(win, text="Delete", bg="#FFB6C1", width=12, command=delete_department).place(x=500, y=60)
    tk.Button(win, text="Clear", bg="#FFDDEE", width=12, command=lambda: dept_entry.delete(0, tk.END)).place(x=620, y=60)

    fetch_departments()
