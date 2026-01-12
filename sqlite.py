import sqlite3

# Connect to SQLite database
connection = sqlite3.connect("student.db")
cursor = connection.cursor()

# Drop table if it already exists
cursor.execute("DROP TABLE IF EXISTS STUDENT")

# Create table
cursor.execute("""
CREATE TABLE STUDENT (
    NAME TEXT,
    CLASS TEXT,
    SECTION TEXT,
    MARKS INTEGER
)
""")

# Insert sample records
students = [
    ("Krish", "Data Science", "A", 90),
    ("Sudhanshu", "Data Science", "B", 100),
    ("Darius", "Data Science", "A", 86),
    ("Vikash", "DEVOPS", "A", 50),
    ("Dipesh", "DEVOPS", "A", 35)
]

cursor.executemany(
    "INSERT INTO STUDENT VALUES (?, ?, ?, ?)",
    students
)

connection.commit()
connection.close()

print("student.db created successfully with sample data.")
