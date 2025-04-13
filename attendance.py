import tkinter as tk
from tkinter import ttk, messagebox
from db_config import connect_db

def open_attendance_window():
    win = tk.Toplevel()
    win.title("Attendance Records")
    win.geometry("800x400")
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

    table = ttk.Treeview(win, columns=("ID", "Employee ID", "Date", "Status"), show='headings')
    table.heading("ID", text="Attendance ID")
    table.heading("Employee ID", text="Employee ID")
    table.heading("Date", text="Date")
    table.heading("Status", text="Status")

    table.column("ID", width=100, anchor='center')
    table.column("Employee ID", width=150, anchor='center')
    table.column("Date", width=150, anchor='center')
    table.column("Status", width=150, anchor='center')

    table.pack(expand=True, fill='both', padx=10, pady=10)

    def fetch_attendance():
        try:
            db = connect_db()
            cursor = db.cursor()
            cursor.execute("SELECT attendance_id, employee_id, date, status FROM attendance")
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

    fetch_attendance()
