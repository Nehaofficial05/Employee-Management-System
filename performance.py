import tkinter as tk
from tkinter import ttk, messagebox
from db_config import connect_db

def open_performance_window():
    win = tk.Toplevel()
    win.title("Performance Records")
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
    table = ttk.Treeview(win, columns=("ID", "Employee ID", "Date", "Rating", "Comments"), show='headings', height=10)
    table.heading("ID", text="Performance ID")
    table.heading("Employee ID", text="Employee ID")
    table.heading("Date", text="Review Date")
    table.heading("Rating", text="Rating (1-5)")
    table.heading("Comments", text="Comments")
    
    # Set column widths and padding
    table.column("ID", width=100, anchor='center')
    table.column("Employee ID", width=150, anchor='center')
    table.column("Date", width=150, anchor='center')
    table.column("Rating", width=100, anchor='center')
    table.column("Comments", width=300, anchor='w')

    table.pack(expand=True, fill='both', padx=10, pady=10)

    def fetch_performance():
        try:
            db = connect_db()
            cursor = db.cursor()
            cursor.execute("SELECT * FROM performance")
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
