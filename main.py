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


def displayUser(user):
    print(f"First name: {db.execute(f"select first_name from Members where Members.id = '{user}'")}")
    print(f"Last name: {db.execute(f"select last_name from Members where Members.id = '{user}'")}")
    choice = 0
    while(True):
        print("1. View exercises")
        print("2. View schedule")
        print("3. Update personal info")
        choice = int(input())
        if(choice >= 1 and choice <= 3):
            break
        print("Invalid input please try again")
    if(choice == 1):
        viewExercises(user)
    elif(choice == 2):
        userSchedule(user)
    else:
        while(True):
            print("1. Update your first name")
            print("2. Update your last name")
            choice = int(input())
            if(choice >= 1 and choice <= 2):
                break
            print("Invalid input please try again")
        if(choice == 1):
            db.execute(f"update Members set first_name = '{input("Type in your new first name: ")}' where id = '{user}'")
            conn.commit()
            print("Update succesful")
            displayUser(user)
        else:
            db.execute(f"update Members set last_name = '{input("Type in your new last name: ")}' where id = '{user}'")
            conn.commit()
            print("Update succesful")
            displayUser(user)

def viewExercises(user):
    print(db.execute(f"select type,goal,current,method from Exercises where Exercises.id = '{user}'"))
    choice = 0
    while(True):
        print("1. Add an exercise")
        print("2. Edit an exercise")
        choice = int(input())
        if(choice >= 1 and choice <= 2):
            break
        print("Invalid input please try again")
    if(choice == 1):
        type = input("Type in the name of the exercise: ")
        goal = input("Type in your goal for this exercise: ")
        current = input("Type in your current record for this exercise: ")
        method = input("Type in your planned routine for this exercise")
        db.execute(f"insert into Members(member,type,goal,current,method) values('{user}','{type}','{goal}','{current}','{method}')")
        conn.commit()
        print("Exercise added")
        displayUser(user)
    else:
        type = input("Type in the name of the exercise you would like to edit: ")
        while(True):
            print("1. Update the exercise name")
            print("2. Update the goal")
            print("3. Update the current record")
            print("4. Update your planned routine")


        
            
    

choice = 0
while(True):
    print("1. Sign in to an existing account")
    print("2. Create new member account") 
    choice = int(input())
    if(choice >= 1 and choice <= 2):
        break
    print("Invalid input please try again")

if(choice == 1):
    while(True):
        print("1. Sign into a member account")
        print("2. Sign into a trainer account")
        print("3. Sign into an admin account")
        choice = int(input())
        if(choice >= 1 and choice <= 3):
            break
        print("Invalid input please try again")
    if(choice == 1):
        while(True):
            print("Please type in your user ID: ")
            choice = int(input())
            if(db.execute(f"select exists(select 1 from Members where Members.id = '{choice}')")):
                break
            print("Invalid ID please try again")
        displayUser(choice)
    elif(choice == 2):
        while(True):
            print("Please type in your trainer ID: ")
            choice = int(input())
            if(db.execute(f"select exists(select 1 from Trainers where Trainers.id = '{choice}')")):
                break
            print("Invalid ID please try again")
        id = choice
        while(True):
            print("1. View your schedule")
            print("2. Search for a member")
            choice = int(input())
            if(choice >= 1 and choice <= 2):
                break
            print("Invalid input please try again")
        if(choice == 1):
            trainerSchedule()
        else:
            searchMembers()
    else:
        while(True):
            print("Please type in your admin ID: ")
            choice = int(input())
            if(db.execute(f"select exists(select 1 from Admins where Admins.id = '{choice}')")):
                break
            print("Invalid ID please try again")
        while(True):
            print("1. Manage room bookings")
            print("2. Manage equipment")
            print("3. Manage class schedule")
            print("4. Process payments")
            choice = int(input)
            if(choice >= 1 and choice <= 3):
                break
            print("Invalid input please try again")
        if(choice == 1):
            bookRooms()
        elif(choice == 2):
            manageEquipment()
        elif(choice == 3):
            updateClassSchedule()
        else:
            processPayment()

else:
    registerMember()







    

  




