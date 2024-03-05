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

print("1. Get all students")
print("2. Add a student")
print("3. Update a student's email")
print("4. Delete a student")
num = int(input())
if(num == 1):
    db.execute('select * from Students')
    for result in db:
        print(result)

elif(num == 2):
    fname = input("Please type in the student's first name: ")
    lname = input("Please type in the student's last name: ")
    email = input("Please type in the students email: ")
    day = datetime.date(int(input("Please type in the year of enrollment: ")),int(input("Please type in the month (1-12) of enrollment: ")),int(input("Please type in the day(1-31) of enrollment:")))  
    day = day.strftime('%Y-%m-%d')
    db.execute(f"insert into Students (first_name, last_name, email, enrollment_date) values ('{fname}', '{lname}', '{email}', '{day}')")
    conn.commit()
    print("Succesfully added student")

elif(num == 3):
    id = int(input("Please type in the id of the student you would like to change the email of:"))
    db.execute('select student_id from Students')
    if(id not in db):
        print("There is no student with this id")
    else:
        

  




