import tkinter as tk
from employees import open_employee_window
from departments import open_department_window
from salaries import open_salary_window
from performance import open_performance_window
from salaries import open_salary_window
from attendance import open_attendance_window  # Already added earlier

root = tk.Tk()
root.title("Employee Management System")
root.geometry("400x500")  # Increased height to accommodate more buttons
root.config(bg='#FFE4E1')  # Light pink background for the main window

# Welcome label with consistent pink theme
tk.Label(root, text="Welcome to Employee Management System", font=("Arial", 14), bg='#FFE4E1').pack(pady=20)

# Buttons with a consistent pink theme
button_style = {'width': 30, 'bg': '#FFB6C1', 'fg': 'black', 'font': ('Arial', 12, 'bold')}

tk.Button(root, text="Manage Employees", command=open_employee_window, **button_style).pack(pady=10)
tk.Button(root, text="Manage Departments", command=open_department_window, **button_style).pack(pady=10)
tk.Button(root, text="Manage Salaries", command=open_salary_window, **button_style).pack(pady=10)
tk.Button(root, text="Manage Performance", command=open_performance_window, **button_style).pack(pady=10)
tk.Button(root, text="Manage Attendance", command=open_attendance_window, **button_style).pack(pady=10)  # Added Attendance Button

root.mainloop()
