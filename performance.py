import tkinter as tk
from tkinter import ttk, messagebox
from db_config import connect_db

def open_performance_window():
    win = tk.Toplevel()
    win.title("Employee Performance")
    win.geometry("900x500")
    win.config(bg='#FFE4E1')

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Treeview", background="#FFFFFF", foreground="black", rowheight=25, fieldbackground="#FFFFFF")
    style.configure("Treeview.Heading", font=('Arial', 12, 'bold'), background="#FFB6C1", foreground="black")
    style.map("Treeview", background=[('selected', '#FF69B4')], foreground=[('selected', 'white')])

    tk.Label(win, text="Employee ID:", bg='#FFE4E1').place(x=30, y=20)
    emp_entry = tk.Entry(win, width=20)
    emp_entry.place(x=150, y=20)

    tk.Label(win, text="Review Date (YYYY-MM-DD):", bg='#FFE4E1').place(x=30, y=60)
    date_entry = tk.Entry(win, width=20)
    date_entry.place(x=230, y=60)

    tk.Label(win, text="Rating (1-5):", bg='#FFE4E1').place(x=30, y=100)
    rating_entry = tk.Entry(win, width=20)
    rating_entry.place(x=150, y=100)

    table = ttk.Treeview(win, columns=("ID", "Emp ID", "Review Date", "Rating"), show='headings', height=10)
    table.heading("ID", text="ID")
    table.heading("Emp ID", text="Employee ID")
    table.heading("Review Date", text="Review Date")
    table.heading("Rating", text="Rating")
    table.column("ID", width=60, anchor='center')
    table.column("Emp ID", width=150, anchor='center')
    table.column("Review Date", width=200, anchor='center')
    table.column("Rating", width=100, anchor='center')
    table.place(x=30, y=150, width=820)

    def fetch_performances():
        try:
            db = connect_db()
            cursor = db.cursor()
            cursor.execute("SELECT performance_id, employee_id, review_date, rating FROM performance")
            rows = cursor.fetchall()
            table.delete(*table.get_children())
            for row in rows:
                table.insert("", tk.END, values=row)
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            cursor.close()
            db.close()

    def insert_performance():
        emp = emp_entry.get()
        date = date_entry.get()
        rating = rating_entry.get()
        if emp and date and rating:
            try:
                db = connect_db()
                cursor = db.cursor()
                cursor.execute("INSERT INTO performance (employee_id, review_date, rating) VALUES (%s, %s, %s)", (emp, date, rating))
                db.commit()
                fetch_performances()
                emp_entry.delete(0, tk.END)
                date_entry.delete(0, tk.END)
                rating_entry.delete(0, tk.END)
            except Exception as e:
                messagebox.showerror("Insert Error", str(e))
            finally:
                cursor.close()
                db.close()

    def update_performance():
        selected = table.focus()
        if selected:
            perf_id = table.item(selected)['values'][0]
            emp = emp_entry.get()
            date = date_entry.get()
            rating = rating_entry.get()
            try:
                db = connect_db()
                cursor = db.cursor()
                cursor.execute("UPDATE performance SET employee_id=%s, review_date=%s, rating=%s WHERE performance_id=%s", (emp, date, rating, perf_id))
                db.commit()
                fetch_performances()
                emp_entry.delete(0, tk.END)
                date_entry.delete(0, tk.END)
                rating_entry.delete(0, tk.END)
            except Exception as e:
                messagebox.showerror("Update Error", str(e))
            finally:
                cursor.close()
                db.close()

    def delete_performance():
        selected = table.focus()
        if selected:
            perf_id = table.item(selected)['values'][0]
            confirm = messagebox.askyesno("Confirm", "Delete this performance record?")
            if confirm:
                try:
                    db = connect_db()
                    cursor = db.cursor()
                    cursor.execute("DELETE FROM performance WHERE performance_id=%s", (perf_id,))
                    db.commit()
                    fetch_performances()
                    emp_entry.delete(0, tk.END)
                    date_entry.delete(0, tk.END)
                    rating_entry.delete(0, tk.END)
                except Exception as e:
                    messagebox.showerror("Delete Error", str(e))
                finally:
                    cursor.close()
                    db.close()

    def select_row(event):
        selected = table.focus()
        if selected:
            values = table.item(selected)['values']
            emp_entry.delete(0, tk.END)
            emp_entry.insert(0, values[1])
            date_entry.delete(0, tk.END)
            date_entry.insert(0, values[2])
            rating_entry.delete(0, tk.END)
            rating_entry.insert(0, values[3])

    table.bind("<ButtonRelease-1>", select_row)

    tk.Button(win, text="Add", bg="#FFB6C1", width=12, command=insert_performance).place(x=500, y=20)
    tk.Button(win, text="Update", bg="#FFB6C1", width=12, command=update_performance).place(x=630, y=20)
    tk.Button(win, text="Delete", bg="#FFB6C1", width=12, command=delete_performance).place(x=500, y=60)
    tk.Button(win, text="Clear", bg="#FFDDEE", width=12, command=lambda: [emp_entry.delete(0, tk.END), date_entry.delete(0, tk.END), rating_entry.delete(0, tk.END)]).place(x=630, y=60)

    fetch_performances()
