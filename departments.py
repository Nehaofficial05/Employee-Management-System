import tkinter as tk
from tkinter import ttk, messagebox
from db_config import connect_db

def open_department_window():
    win = tk.Toplevel()
    win.title("Department Records")
    win.geometry("900x500")
    win.config(bg='#F5F5F5')  # Light gray background for the window

    # Treeview Styling
    style = ttk.Style()
    style.configure("Treeview",
                    background="#FFFFFF",  # White background for rows
                    foreground="black",
                    fieldbackground="#FFFFFF")
    
    # Header Styling
    style.configure("Treeview.Heading",
                    font=('Arial', 12, 'bold'),
                    background="#006747",  # Starbucks Green header
                    foreground="white", 
                    padding=(10, 5))  # Padding for better spacing in the header
    
    # Treeview Row Styling
    style.map("Treeview",
              background=[('selected', '#006747')])  # Selected row background

    # Create Treeview Table
    table = ttk.Treeview(win, columns=("ID", "Name", "Location", "Email"), show='headings', height=10)
    table.heading("ID", text="Department ID")
    table.heading("Name", text="Department Name")
    table.heading("Location", text="Location")
    table.heading("Email", text="Email")
    
    # Set column widths and padding
    table.column("ID", width=100, anchor='center')
    table.column("Name", width=200, anchor='w')
    table.column("Location", width=200, anchor='w')
    table.column("Email", width=300, anchor='w')

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
