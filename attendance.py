import tkinter as tk
from tkinter import ttk, messagebox
from db_config import connect_db

def open_attendance_window():
    win = tk.Toplevel()
    win.title("Attendance Records")
    win.geometry("900x500")
    win.config(bg='#FFFFFF')  # White background

    # Table styling with Starbucks Green color
    style = ttk.Style()
    style.configure("Treeview",
                    background="#FFFFFF",  # White rows
                    foreground="black",
                    fieldbackground="#FFFFFF")
    style.configure("Treeview.Heading", font=('Arial', 12, 'bold'), background="#006747", foreground="white")  # Header style

    table = ttk.Treeview(win, columns=("ID", "Employee ID", "Date", "Status"), show='headings')
    for col in ("ID", "Employee ID", "Date", "Status"):
        table.heading(col, text=col)
        table.column(col, width=150)
    table.pack(expand=True, fill='both', padx=10, pady=10)

    # Input fields frame
    frame = tk.Frame(win, bg='#FFFFFF')
    frame.pack(pady=10)
    tk.Label(frame, text="Employee ID", bg='#FFFFFF').grid(row=0, column=0)
    emp_id_entry = tk.Entry(frame)
    emp_id_entry.grid(row=0, column=1)

    tk.Label(frame, text="Date (YYYY-MM-DD)", bg='#FFFFFF').grid(row=0, column=2)
    date_entry = tk.Entry(frame)
    date_entry.grid(row=0, column=3)

    tk.Label(frame, text="Status (Present/Absent)", bg='#FFFFFF').grid(row=0, column=4)
    status_entry = tk.Entry(frame)
    status_entry.grid(row=0, column=5)

    def fetch_attendance():
        try:
            db = connect_db()
            cursor = db.cursor()
            cursor.execute("SELECT * FROM attendance")
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

    def add_attendance():
        emp_id = emp_id_entry.get()
        date = date_entry.get()
        status = status_entry.get()
        if not (emp_id and date and status):
            messagebox.showwarning("Input Error", "All fields required")
            return
        try:
            db = connect_db()
            cursor = db.cursor()
            cursor.execute("INSERT INTO attendance (employee_id, attendance_date, status) VALUES (%s, %s, %s)", 
                           (emp_id, date, status))
            db.commit()
            fetch_attendance()
            messagebox.showinfo("Success", "Attendance added")
        except Exception as e:
            messagebox.showerror("Insert Error", str(e))
        finally:
            cursor.close()
            db.close()

    def delete_attendance():
        selected = table.selection()
        if not selected:
            messagebox.showwarning("Select Row", "Please select a row to delete")
            return
        att_id = table.item(selected[0])['values'][0]
        try:
            db = connect_db()
            cursor = db.cursor()
            cursor.execute("DELETE FROM attendance WHERE attendance_id = %s", (att_id,))
            db.commit()
            fetch_attendance()
            messagebox.showinfo("Deleted", "Attendance deleted")
        except Exception as e:
            messagebox.showerror("Delete Error", str(e))
        finally:
            cursor.close()
            db.close()

    tk.Button(win, text="Add Attendance", bg="#006747", fg="white", command=add_attendance).pack(pady=5)
    tk.Button(win, text="Delete Selected", bg="#006747", fg="white", command=delete_attendance).pack(pady=5)

    fetch_attendance()
