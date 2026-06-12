import sqlite3

## Connectt to SQlite
connection=sqlite3.connect("student.db")

# Create a cursor object to insert record,create table

cursor=connection.cursor()

## Drop the table if it already exists
cursor.execute("DROP TABLE IF EXISTS STUDENT")

## create the table
table_info="""
Create table STUDENT(NAME VARCHAR(25), SUBJECT VARCHAR(25),
DIVISON VARCHAR(25), MARKS INT);
"""
cursor.execute(table_info)

## Insert Some more records

cursor.execute('''Insert Into STUDENT values('Krish','Data Science','A',90)''')
cursor.execute('''Insert Into STUDENT values('Sudhanshu','Data Science','B',100)''')
cursor.execute('''Insert Into STUDENT values('Darius','Data Science','A',86)''')
cursor.execute('''Insert Into STUDENT values('Vikash','DEVOPS','A',50)''')
cursor.execute('''Insert Into STUDENT values('Dipesh','DEVOPS','A',35)''')

# 50 Additional Records
records = [
    ("Alice", "Data Science", "C", 78),
    ("Bob", "DEVOPS", "B", 82),
    ("Charlie", "Cyber Security", "A", 95),
    ("David", "Cloud Computing", "A", 67),
    ("Eva", "AI", "B", 88),
    ("Frank", "Machine Learning", "C", 73),
    ("Grace", "Full Stack", "A", 91),
    ("Hannah", "Data Science", "B", 84),
    ("Ian", "DEVOPS", "A", 59),
    ("Jack", "Cyber Security", "C", 76),
    ("Karen", "Cloud Computing", "B", 92),
    ("Liam", "AI", "A", 81),
    ("Mia", "Machine Learning", "A", 90),
    ("Noah", "Full Stack", "C", 68),
    ("Olivia", "Data Science", "A", 85),
    ("Paul", "DEVOPS", "B", 72),
    ("Quinn", "Cyber Security", "B", 89),
    ("Rachel", "Cloud Computing", "C", 65),
    ("Sam", "AI", "C", 77),
    ("Tom", "Machine Learning", "B", 83),
    ("Uma", "Full Stack", "A", 94),
    ("Victor", "Data Science", "C", 71),
    ("Wendy", "DEVOPS", "A", 87),
    ("Xander", "Cyber Security", "C", 63),
    ("Yara", "Cloud Computing", "A", 96),
    ("Zack", "AI", "B", 79),
    ("Abby", "Machine Learning", "A", 86),
    ("Ben", "Full Stack", "B", 75),
    ("Cara", "Data Science", "A", 93),
    ("Dan", "DEVOPS", "C", 62),
    ("Emma", "Cyber Security", "A", 80),
    ("Finn", "Cloud Computing", "B", 74),
    ("Gina", "AI", "C", 69),
    ("Harry", "Machine Learning", "C", 97),
    ("Ivy", "Full Stack", "A", 88),
    ("Jake", "Data Science", "B", 70),
    ("Kate", "DEVOPS", "B", 91),
    ("Leo", "Cyber Security", "A", 84),
    ("Maya", "Cloud Computing", "C", 78),
    ("Nate", "AI", "A", 82),
    ("Owen", "Machine Learning", "B", 76),
    ("Piper", "Full Stack", "C", 85),
    ("Quincy", "Data Science", "A", 90),
    ("Rose", "DEVOPS", "A", 66),
    ("Sean", "Cyber Security", "B", 92),
    ("Tara", "Cloud Computing", "A", 87),
    ("Uri", "AI", "B", 73),
    ("Vera", "Machine Learning", "C", 81),
    ("Will", "Full Stack", "B", 89),
    ("Zoe", "Data Science", "C", 95)
]

for record in records:
    cursor.execute(f"Insert Into STUDENT values('{record[0]}', '{record[1]}', '{record[2]}', {record[3]})")

## Disspaly ALl the records

print("The isnerted records are")
data=cursor.execute('''Select * from STUDENT''')
for row in data:
    print(row)

## Commit your changes int he databse
connection.commit()
connection.close()
