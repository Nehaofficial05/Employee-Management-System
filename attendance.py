import tkinter as tk
from tkinter import ttk, messagebox
from db_config import connect_db

def open_attendance_window():
    win = tk.Toplevel()
    win.title("Attendance Records")
    win.geometry("800x500")  # Increased height for better layout
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

    # Add input fields for creating/updating attendance records
    input_frame = tk.Frame(win, bg='#FFE4E1')  # Frame to organize input fields
    input_frame.pack(pady=10, padx=10, fill='x')

    tk.Label(input_frame, text="Employee ID:", bg='#FFE4E1').pack(pady=5)
    emp_id_entry = tk.Entry(input_frame)
    emp_id_entry.pack(pady=5)

    tk.Label(input_frame, text="Date (YYYY-MM-DD):", bg='#FFE4E1').pack(pady=5)
    date_entry = tk.Entry(input_frame)
    date_entry.pack(pady=5)

    tk.Label(input_frame, text="Status (Present/Absent):", bg='#FFE4E1').pack(pady=5)
    status_entry = tk.Entry(input_frame)
    status_entry.pack(pady=5)

    # Button style configuration
    button_style = {
        'width': 20,
        'height': 2,
        'bg': '#FFB6C1',  # Light pink button color
        'font': ('Arial', 10, 'bold')
    }

    def fetch_attendance():
        try:
            db = connect_db()
            cursor = db.cursor()
            cursor.execute("SELECT attendance_id, employee_id, attendance_date, status FROM attendance")
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
        if not emp_id or not date or not status:
            messagebox.showerror("Input Error", "All fields are required.")
            return
        try:
            db = connect_db()
            cursor = db.cursor()
            cursor.execute("INSERT INTO attendance (employee_id, attendance_date, status) VALUES (%s, %s, %s)",
                           (emp_id, date, status))
            db.commit()
            messagebox.showinfo("Success", "Attendance record added.")
            fetch_attendance()  # Refresh the table after adding
        except Exception as e:
            messagebox.showerror("DB Error", str(e))
        finally:
            cursor.close()
            db.close()

    def update_attendance():
        selected_item = table.selection()
        if not selected_item:
            messagebox.showerror("Selection Error", "Please select a record to update.")
            return
        attendance_id = table.item(selected_item[0])['values'][0]
        emp_id = emp_id_entry.get()
        date = date_entry.get()
        status = status_entry.get()
        if not emp_id or not date or not status:
            messagebox.showerror("Input Error", "All fields are required.")
            return
        try:
            db = connect_db()
            cursor = db.cursor()
            cursor.execute("UPDATE attendance SET employee_id = %s, attendance_date = %s, status = %s WHERE attendance_id = %s",
                           (emp_id, date, status, attendance_id))
            db.commit()
            messagebox.showinfo("Success", "Attendance record updated.")
            fetch_attendance()  # Refresh the table after updating
        except Exception as e:
            messagebox.showerror("DB Error", str(e))
        finally:
            cursor.close()
            db.close()

    def delete_attendance():
        selected_item = table.selection()
        if not selected_item:
            messagebox.showerror("Selection Error", "Please select a record to delete.")
            return
        attendance_id = table.item(selected_item[0])['values'][0]
        try:
            db = connect_db()
            cursor = db.cursor()
            cursor.execute("DELETE FROM attendance WHERE attendance_id = %s", (attendance_id,))
            db.commit()
            messagebox.showinfo("Success", "Attendance record deleted.")
            fetch_attendance()  # Refresh the table after deleting
        except Exception as e:
            messagebox.showerror("DB Error", str(e))
        finally:
            cursor.close()
            db.close()

    # CRUD Operation buttons
    button_frame = tk.Frame(win, bg='#FFE4E1')  # Frame to organize buttons
    button_frame.pack(pady=10, padx=10)

    tk.Button(button_frame, text="Add Attendance", command=add_attendance, **button_style).pack(pady=5)
    tk.Button(button_frame, text="Update Attendance", command=update_attendance, **button_style).pack(pady=5)
    tk.Button(button_frame, text="Delete Attendance", command=delete_attendance, **button_style).pack(pady=5)

    fetch_attendance()  # Fetch and display attendance records on window open
