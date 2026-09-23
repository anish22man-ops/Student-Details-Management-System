import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# Database Setup

connection = sqlite3.connect("students.db")
cursor = connection.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        roll_no TEXT NOT NULL,
        course TEXT NOT NULL,
        semester TEXT NOT NULL,
        email TEXT NOT NULL,
        phone TEXT NOT NULL
    )
""")

connection.commit()

# Functions

def clear_fields():
    name_entry.delete(0, tk.END)
    roll_entry.delete(0, tk.END)
    course_entry.delete(0, tk.END)
    semester_combo.set("")
    email_entry.delete(0, tk.END)
    phone_entry.delete(0, tk.END)


def add_student():
    name = name_entry.get().strip()
    roll_no = roll_entry.get().strip()
    course = course_entry.get().strip()
    semester = semester_combo.get().strip()
    email = email_entry.get().strip()
    phone = phone_entry.get().strip()

    if not name or not roll_no or not course or not semester or not email or not phone:
        messagebox.showwarning(
            "Missing Information",
            "Please fill in all fields."
        )
        return

    if not phone.isdigit() or len(phone) != 10:
        messagebox.showwarning(
            "Invalid Phone Number",
            "Please enter a valid 10-digit phone number."
        )
        return

    if "@" not in email or "." not in email:
        messagebox.showwarning(
            "Invalid Email",
            "Please enter a valid email address."
        )
        return

    try:
        cursor.execute("""
            INSERT INTO students
            (name, roll_no, course, semester, email, phone)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (name, roll_no, course, semester, email, phone))

        connection.commit()

        messagebox.showinfo(
            "Success",
            "Student details added successfully."
        )

        clear_fields()
        display_students()

    except sqlite3.Error as error:
        messagebox.showerror(
            "Database Error",
            f"An error occurred:\n{error}"
        )


def display_students():
    # Remove existing rows
    for item in student_table.get_children():
        student_table.delete(item)

    cursor.execute("""
        SELECT id, name, roll_no, course, semester, email, phone
        FROM students
        ORDER BY id DESC
    """)

    records = cursor.fetchall()

    for record in records:
        student_table.insert("", tk.END, values=record)


def delete_student():
    selected_item = student_table.selection()

    if not selected_item:
        messagebox.showwarning(
            "No Selection",
            "Please select a student to delete."
        )
        return

    selected_data = student_table.item(selected_item[0])
    student_id = selected_data["values"][0]

    confirm = messagebox.askyesno(
        "Confirm Delete",
        "Are you sure you want to delete this student?"
    )

    if confirm:
        cursor.execute(
            "DELETE FROM students WHERE id = ?",
            (student_id,)
        )

        connection.commit()

        messagebox.showinfo(
            "Deleted",
            "Student details deleted successfully."
        )

        display_students()


def search_student():
    search_text = search_entry.get().strip()

    if not search_text:
        display_students()
        return

    for item in student_table.get_children():
        student_table.delete(item)

    cursor.execute("""
        SELECT id, name, roll_no, course, semester, email, phone
        FROM students
        WHERE name LIKE ?
           OR roll_no LIKE ?
           OR course LIKE ?
           OR email LIKE ?
    """, (
        "%" + search_text + "%",
        "%" + search_text + "%",
        "%" + search_text + "%",
        "%" + search_text + "%"
    ))

    records = cursor.fetchall()

    for record in records:
        student_table.insert("", tk.END, values=record)


def select_student(event):
    selected_item = student_table.selection()

    if not selected_item:
        return

    selected_data = student_table.item(selected_item[0])
    values = selected_data["values"]

    if values:
        name_entry.delete(0, tk.END)
        name_entry.insert(0, values[1])

        roll_entry.delete(0, tk.END)
        roll_entry.insert(0, values[2])

        course_entry.delete(0, tk.END)
        course_entry.insert(0, values[3])

        semester_combo.set(values[4])

        email_entry.delete(0, tk.END)
        email_entry.insert(0, values[5])

        phone_entry.delete(0, tk.END)
        phone_entry.insert(0, values[6])


def update_student():
    selected_item = student_table.selection()

    if not selected_item:
        messagebox.showwarning(
            "No Selection",
            "Please select a student from the table."
        )
        return

    selected_data = student_table.item(selected_item[0])
    student_id = selected_data["values"][0]

    name = name_entry.get().strip()
    roll_no = roll_entry.get().strip()
    course = course_entry.get().strip()
    semester = semester_combo.get().strip()
    email = email_entry.get().strip()
    phone = phone_entry.get().strip()

    if not name or not roll_no or not course or not semester or not email or not phone:
        messagebox.showwarning(
            "Missing Information",
            "Please fill in all fields."
        )
        return

    if not phone.isdigit() or len(phone) != 10:
        messagebox.showwarning(
            "Invalid Phone Number",
            "Please enter a valid 10-digit phone number."
        )
        return

    if "@" not in email or "." not in email:
        messagebox.showwarning(
            "Invalid Email",
            "Please enter a valid email address."
        )
        return

    cursor.execute("""
        UPDATE students
        SET name = ?,
            roll_no = ?,
            course = ?,
            semester = ?,
            email = ?,
            phone = ?
        WHERE id = ?
    """, (
        name,
        roll_no,
        course,
        semester,
        email,
        phone,
        student_id
    ))

    connection.commit()

    messagebox.showinfo(
        "Updated",
        "Student details updated successfully."
    )

    clear_fields()
    display_students()


def close_application():
    connection.close()
    root.destroy()

# Main Window
root = tk.Tk()

root.title("Student Details Management System")
root.geometry("1050x650")
root.configure(bg="#f2f2f2")
root.resizable(True, True)

# Heading
title_label = tk.Label(
    root,
    text="Student Details Management System",
    font=("Arial", 24, "bold"),
    bg="#f2f2f2",
    fg="#222222"
)

title_label.pack(pady=20)

# Form Frame
form_frame = tk.Frame(
    root,
    bg="white",
    bd=1,
    relief=tk.SOLID
)

form_frame.pack(
    padx=30,
    pady=5,
    fill=tk.X
)


# Name
tk.Label(
    form_frame,
    text="Student Name",
    font=("Arial", 11, "bold"),
    bg="white"
).grid(row=0, column=0, padx=15, pady=12, sticky="w")

name_entry = tk.Entry(
    form_frame,
    font=("Arial", 11),
    width=25
)

name_entry.grid(row=0, column=1, padx=10, pady=12)


# Roll Number
tk.Label(
    form_frame,
    text="Roll Number",
    font=("Arial", 11, "bold"),
    bg="white"
).grid(row=0, column=2, padx=15, pady=12, sticky="w")

roll_entry = tk.Entry(
    form_frame,
    font=("Arial", 11),
    width=25
)

roll_entry.grid(row=0, column=3, padx=10, pady=12)


# Course
tk.Label(
    form_frame,
    text="Course",
    font=("Arial", 11, "bold"),
    bg="white"
).grid(row=1, column=0, padx=15, pady=12, sticky="w")

course_entry = tk.Entry(
    form_frame,
    font=("Arial", 11),
    width=25
)

course_entry.grid(row=1, column=1, padx=10, pady=12)


# Semester
tk.Label(
    form_frame,
    text="Semester",
    font=("Arial", 11, "bold"),
    bg="white"
).grid(row=1, column=2, padx=15, pady=12, sticky="w")

semester_combo = ttk.Combobox(
    form_frame,
    values=[
        "Semester 1",
        "Semester 2",
        "Semester 3",
        "Semester 4",
        "Semester 5",
        "Semester 6"
    ],
    font=("Arial", 11),
    width=23,
    state="readonly"
)

semester_combo.grid(row=1, column=3, padx=10, pady=12)


# Email
tk.Label(
    form_frame,
    text="Email",
    font=("Arial", 11, "bold"),
    bg="white"
).grid(row=2, column=0, padx=15, pady=12, sticky="w")

email_entry = tk.Entry(
    form_frame,
    font=("Arial", 11),
    width=25
)

email_entry.grid(row=2, column=1, padx=10, pady=12)


# Phone
tk.Label(
    form_frame,
    text="Phone",
    font=("Arial", 11, "bold"),
    bg="white"
).grid(row=2, column=2, padx=15, pady=12, sticky="w")

phone_entry = tk.Entry(
    form_frame,
    font=("Arial", 11),
    width=25
)

phone_entry.grid(row=2, column=3, padx=10, pady=12)

# Buttons
button_frame = tk.Frame(
    root,
    bg="#f2f2f2"
)

button_frame.pack(pady=15)


add_button = tk.Button(
    button_frame,
    text="Add Student",
    command=add_student,
    font=("Arial", 11, "bold"),
    padx=15,
    pady=8
)

add_button.grid(row=0, column=0, padx=5)


update_button = tk.Button(
    button_frame,
    text="Update",
    command=update_student,
    font=("Arial", 11, "bold"),
    padx=15,
    pady=8
)

update_button.grid(row=0, column=1, padx=5)


delete_button = tk.Button(
    button_frame,
    text="Delete",
    command=delete_student,
    font=("Arial", 11, "bold"),
    padx=15,
    pady=8
)

delete_button.grid(row=0, column=2, padx=5)


clear_button = tk.Button(
    button_frame,
    text="Clear",
    command=clear_fields,
    font=("Arial", 11, "bold"),
    padx=15,
    pady=8
)

clear_button.grid(row=0, column=3, padx=5)

# Search

search_frame = tk.Frame(
    root,
    bg="#f2f2f2"
)

search_frame.pack(pady=5)


tk.Label(
    search_frame,
    text="Search:",
    font=("Arial", 11, "bold"),
    bg="#f2f2f2"
).pack(side=tk.LEFT, padx=5)


search_entry = tk.Entry(
    search_frame,
    font=("Arial", 11),
    width=35
)

search_entry.pack(side=tk.LEFT, padx=5)


search_button = tk.Button(
    search_frame,
    text="Search",
    command=search_student,
    font=("Arial", 10, "bold"),
    padx=12
)

search_button.pack(side=tk.LEFT, padx=5)


show_all_button = tk.Button(
    search_frame,
    text="Show All",
    command=display_students,
    font=("Arial", 10, "bold"),
    padx=12
)

show_all_button.pack(side=tk.LEFT, padx=5)

# Student Table
table_frame = tk.Frame(root)

table_frame.pack(
    padx=30,
    pady=15,
    fill=tk.BOTH,
    expand=True
)


columns = (
    "ID",
    "Name",
    "Roll No",
    "Course",
    "Semester",
    "Email",
    "Phone"
)


student_table = ttk.Treeview(
    table_frame,
    columns=columns,
    show="headings"
)


for column in columns:
    student_table.heading(
        column,
        text=column
    )


student_table.column("ID", width=50, anchor="center")
student_table.column("Name", width=150)
student_table.column("Roll No", width=100)
student_table.column("Course", width=120)
student_table.column("Semester", width=100)
student_table.column("Email", width=200)
student_table.column("Phone", width=120)


scrollbar = ttk.Scrollbar(
    table_frame,
    orient=tk.VERTICAL,
    command=student_table.yview
)

student_table.configure(
    yscrollcommand=scrollbar.set
)


student_table.pack(
    side=tk.LEFT,
    fill=tk.BOTH,
    expand=True
)

scrollbar.pack(
    side=tk.RIGHT,
    fill=tk.Y
)


# Select table row
student_table.bind(
    "<ButtonRelease-1>",
    select_student
)



# Load Existing Students
display_students()



# Close Event
root.protocol(
    "WM_DELETE_WINDOW",
    close_application
)



root.mainloop()
