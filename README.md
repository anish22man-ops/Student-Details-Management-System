### Student Details Management System ###

A Python-based desktop application developed using Tkinter and SQLite for managing student information through a simple and user-friendly graphical interface.

The application allows users to add, view, search, update, and delete student records. Student information is stored in an SQLite database, allowing the data to remain available when the application is closed and reopened.

## Features

- Add new student records
- View student records in a table
- Update existing student information
- Delete student records
- Search student records
- SQLite database integration
- CRUD operations
- Input validation
- Email validation
- Phone number validation
- Interactive graphical user interface

## Technologies Used

- Python
- Tkinter
- SQLite
- SQL

## Student Information

The application stores the following information:

- Student ID
- Student Name
- Roll Number
- Course
- Semester
- Email
- Phone Number

## Database ##

This project uses SQLite as the database.

The database file is automatically created when the application is run for the first time.

The database file is named:

`students.db`

The database file is not included in this GitHub repository because it may contain student information. It is also included in `.gitignore` so it will not be uploaded accidentally.

## CRUD Operations

This project demonstrates the four basic CRUD operations:

### Create

Users can add new student records to the database.

### Read

The application displays stored student records in a table.

### Update

Users can select an existing student and update their information.

### Delete

Users can select and delete unwanted student records.

## Search Functionality

The application provides a search feature that allows users to find student records using information such as:

- Student name
- Roll number
- Course
- Email

## Input Validation

The application includes basic input validation to improve data accuracy.

It checks that:

- Required fields are completed
- Phone numbers contain 10 digits
- Email addresses follow a basic valid format

## How It Works ##

The application provides a graphical interface where users can enter student information.

When a student is added, the information is inserted into the SQLite database. The stored records are then displayed in a table using the Tkinter Treeview widget.

Users can select a record from the table to update or delete it. The search functionality allows users to find specific records quickly.

## How to Run

### 1. Download or Clone the Repository

***You can download the repository or clone it using Git:
git clone https://github.com/anish22man-ops/student-details-management-system.git