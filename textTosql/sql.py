import sqlite3

### connect to sqlite3
connection = sqlite3.connect("student.db")

### create a curson object to insert,record, create table, retrieve

cursor = connection.cursor()

### create a table

table_info = """
        create table student(name varchar(25),class varchar(25),
        section varchar(25),marks int);

"""

cursor.execute(table_info)

### insert some more records

cursor.execute('''Insert Into STUDENT values('Krish','Data Science','A',90)''')
cursor.execute('''Insert Into STUDENT values('Sudhanshu','Data Science','B',100)''')
cursor.execute('''Insert Into STUDENT values('Darius','Data Science','A',86)''')
cursor.execute('''Insert Into STUDENT values('Vikash','DEVOPS','A',50)''')
cursor.execute('''Insert Into STUDENT values('Dipesh','DEVOPS','A',35)''')


#### display all the records

print("the inserted records are ")

data = cursor.execute('''select * from student''')

for row in data:
    print(row)


### close the connection
connection.commit()
connection.close()


