import psycopg2
from config import load_config
import datetime

def connect(config):
    """ Connect to the PostgreSQL database server """
    try:
        # connecting to the PostgreSQL server
        with psycopg2.connect(**config) as conn:
            print('Connected to the PostgreSQL server.')
            return conn
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)


if __name__ == '__main__':
    config = load_config()
    conn = connect(config)
    db = conn.cursor()

db.execute("DROP TABLE IF EXISTS Students")
db.execute("CREATE TABLE students (student_id SERIAL PRIMARY KEY,first_name TEXT NOT NULL,last_name TEXT NOT NULL,email TEXT NOT NULL UNIQUE,enrollment_date DATE)")
db.execute("INSERT INTO students (first_name, last_name, email, enrollment_date) VALUES('John', 'Doe', 'john.doe@example.com', '2023-09-01'),('Jane', 'Smith', 'jane.smith@example.com', '2023-09-01'),('Jim', 'Beam', 'jim.beam@example.com', '2023-09-02');")
conn.commit()
print("Succesfully created and filled database")

def getAllStudents():
    db.execute('select * from Students')
    for result in db:
        print(result)

def addStudent(first_name, last_name, email, enrollment_date):
    db.execute(f"insert into Students (first_name, last_name, email, enrollment_date) values ('{first_name}', '{last_name}', '{email}', '{enrollment_date}')")
    conn.commit()
    print("Succesfully added student")


def updateStudentEmail(student_id, new_email):
    db.execute(f"update Students set email = '{new_email}' where student_id = '{student_id}'")
    conn.commit()
    print("Succesfully changed email")

def deleteStudent(student_id):
    db.execute(f"delete from Students where student_id = '{student_id}'")
    conn.commit()
    print("Succesfully deleted student")

while(True):
    print("0. Exit")
    print("1. Get all students")
    print("2. Add a student")
    print("3. Update a student's email")
    print("4. Delete a student")
    num = int(input())
    if(num == 0):
        break
    
    elif(num == 1):
        getAllStudents()

    elif(num == 2):
        fname = input("Please type in the student's first name: ")
        lname = input("Please type in the student's last name: ")
        email = input("Please type in the students email: ")
        day = datetime.date(int(input("Please type in the year of enrollment: ")),int(input("Please type in the month (1-12) of enrollment: ")),int(input("Please type in the day(1-31) of enrollment:")))  
        day = day.strftime('%Y-%m-%d')
        addStudent(fname,lname,email,day)
    
    elif(num == 3):
        id = int(input("Please type in the id of the student you would like to change the email of: "))
        email = input("Please type in the new email you want this student to have: ")
        updateStudentEmail(id,email)

    elif(num == 4):
        deleteStudent(int(input("Please type in the id of the student you would like to delete: ")))
    

  




