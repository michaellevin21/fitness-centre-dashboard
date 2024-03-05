import psycopg2
from config import load_config

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
    db = connect(config).cursor()

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
    fname = input("Please type in the student's first name")
    lname = input("Please type in the student's last name")
    email = input("Please type in the students email")
    db.execute(f"insert into Students values({input("")})")



