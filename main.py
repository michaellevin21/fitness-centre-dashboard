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
    db.execute(f'select first_name from Members where Members.id = {user}')
    print(f"First name: {db.fetchone()[0]}")
    db.execute(f'select last_name from Members where Members.id = {user}')
    print(f"Last name: {db.fetchone()[0]}")
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
            name = input("Type in your new first name: ")
            db.execute(f"update Members set first_name = '{name}' where id = '{user}'")
            conn.commit()
            print("Update succesful")
            displayUser(user)
        else:
            name = input("Type in your new last name: ")
            db.execute(f"update Members set last_name = '{name}' where id = '{user}'")
            conn.commit()
            print("Update succesful")
            displayUser(user)

def viewExercises(user):
    print("Exercises:")
    db.execute(f"select type,goal,current,method from Exercises where Exercises.member = '{user}'")
    print("Name|Goal|Current Record|Routine")
    print(db.fetchall())
    choice = 0
    while(True):
        print("1. Add an exercise")
        print("2. Edit an exercise")
        choice = int(input())
        if(choice >= 1 and choice <= 2):
            break
        print("Invalid input please try again")
    if(choice == 1):
        type = ""
        while(True):
            type = input("Type in the name of the exercise: ")
            db.execute(f"select 1 from Exercises where Exercises.member = '{user}' and Exercises.type = '{type}'" )
            if(db.rowcount == 0):
                break
            print("You already have an exercise with this name please try again")
        goal = input("Type in your goal for this exercise: ")
        current = input("Type in your current record for this exercise: ")
        method = input("Type in your planned routine for this exercise: ")
        db.execute(f"insert into Exercises(member,type,goal,current,method) values('{user}','{type}','{goal}','{current}','{method}')")
        conn.commit()
        print("Exercise added")
        displayUser(user)
    else:
        type = ""
        while(True):
            type = input("Type in the name of the exercise you would like to edit: ")
            db.execute(f"select 1 from Exercises where Exercises.member = '{user}' and Exercises.type = '{type}'" )
            if(db.rowcount != 0):
                break
            print("You don't have an exercise with this name please try again")
        while(True):
            print("1. Update the exercise name")
            print("2. Update the goal")
            print("3. Update the current record")
            print("4. Update your planned routine")
            choice = int(input())
            if(choice >= 1 and choice <= 4):
                break
            print("Invalid input please try again")
        if(choice == 1):
            name = input("Type in the new name for the exercise: ")
            db.execute(f"update Exercises set type = '{name}' where member = '{user}' and type = '{type}'")
            conn.commit()
            print("Update succesful")
            displayUser(user)
        elif(choice == 2):
            goal = input("Type in the new goal for the exercise: ")
            db.execute(f"update Exercises set goal = '{goal}' where member = '{user}' and type = '{type}'")
            conn.commit()
            print("Update succesful")
            displayUser(user)
        elif(choice == 3):
            current = input("Type in the new record for the exercise: ")
            db.execute(f"update Exercises set current = '{current}' where member = '{user}' and type = '{type}'")
            conn.commit()
            print("Update succesful")
            displayUser(user)
        else:
            method = input("Type in the new routine for the exercise: ")
            db.execute(f"update Exercises set method = '{method}' where member = '{user}' and type = '{type}'")
            conn.commit()
            print("Update succesful")
            displayUser(user)

def userSchedule(user):
    print("Booked sessions:")
    print("ID|Trainer|Date|Time")
    db.execute(f"select Sessions.id,first_name || ' ' || last_name as trainer,date,time from Sessions join Trainers on Sessions.trainer = Trainers.id where member = '{user}'")
    print(db.fetchall())
    print("Registered classes:")
    print("Date|Time|Room")
    db.execute(f"select date,time,room from Classes join Takes on Classes.id = Takes.class where member = '{user}'")
    print(db.fetchall())
    choice = 0
    while(True):
        print("1. Manage your sessions")
        print("2. Register for a group class")
        choice = int(input())
        if(choice >= 1 and choice <= 2):
            break
        print("Invalid input please try again")
    if(choice == 1):
        while(True):
            print("1. Book a session with a trainer")
            print("2. Reschedule an existing session")
            print("3. Cancel a session")
            choice = int(input())
            if(choice >= 1 and choice <= 3):
                break
            print("Invalid input please try again")
        if(choice == 1):
            print("Trainers:")
            db.execute("select * from Trainers")
            print("ID|First|Last|Cost")
            print(db.fetchall())
            while(True):
                choice = int(input("Type the id of the trainer you want to book a session with: "))
                db.execute(f"select 1 from Trainers where Trainers.id = '{choice}'")
                if(db.rowcount != 0):
                    break
                print("There is no trainer with this id please try again")
            print("Trainer availabilities:")
            db.execute(f"select date,time from Availabilities where Availabilities.trainer = '{choice}' order by date,time")
            print(db.fetchall())
            trainer = choice
            while(True):
                choice = int(input("Type 1 to pick the first availability, 2 to pick the second one, etc: "))
                db.execute(f"select Count(date) from (select date,time from Availabilities where Availabilities.trainer = '{trainer}')")
                if(db.fetchone()[0] >= choice and choice >= 1):
                    break
                print("Invalid input please try again")
            db.execute(f"select date,time from Availabilities where Availabilities.trainer = '{trainer}' order by date,time offset '{choice-1}' limit 1")
            result = db.fetchone()
            db.execute(f"select 1 from Sessions where Sessions.member = '{user}' and Sessions.date = '{result[0]}' and Sessions.time = '{result[1]}'")
            if(db.rowcount != 0):
                print("You already have a session during this time")
                userSchedule(user)
            db.execute(f"select 1 from Classes join Takes on Classes.id = Takes.class where Takes.member = '{user}' and Classes.date = '{result[0]}' and Classes.time = '{result[1]}'")
            if(db.rowcount != 0):
                print("You are registered in a class during this time")
                userSchedule(user)
            else:
                db.execute(f"insert into Sessions(member,trainer,date,time,paid_for) values('{user}','{trainer}','{result[0]}','{result[1]}',FALSE)")
                conn.commit()
                db.execute(f"delete from Availabilities where Availabilities.trainer = '{trainer}' and Availabilities.date = '{result[0]}' and Availabilities.time = '{result[1]}'")
                conn.commit()
                print("Session added")
                displayUser(user)
        elif(choice == 2):
            while(True):
                choice = int(input("Type the id of the session you want to reschedule: "))
                db.execute(f"select 1 from Sessions where Sessions. id = '{choice}' and Sessions.member = '{user}'")
                if(db.rowcount != 0):
                    print("Trainer availabilities:")
                    db.execute(f"select * from Sessions where Sessions. id = '{choice}' and Sessions.member = '{user}'")
                    session = db.fetchone() 
                    db.execute(f"select date,time from Availabilities where Availabilities.trainer = '{session[2]}' order by date,time")
                    print(db.fetchall())
                    trainer = session[2]
                    while(True):
                        choice = int(input("Type 1 to pick the first availability, 2 to pick the second one, etc: "))
                        db.execute(f"select Count(date) from (select date,time from Availabilities where Availabilities.trainer = '{trainer}')")
                        if(db.fetchone()[0] >= choice and choice >= 1):
                            break
                        print("Invalid input please try again")
                    db.execute(f"select date,time from Availabilities where Availabilities.trainer = '{trainer}' order by date,time offset '{choice-1}' limit 1")
                    result = db.fetchone()
                    db.execute(f"select 1 from Sessions where Sessions.member = '{user}' and Sessions.date = '{result[0]}' and Sessions.time = '{result[1]}'")
                    if(db.rowcount != 0):
                        print("You already have a session during this time")
                        userSchedule(user)
                    db.execute(f"select 1 from Classes join Takes on Classes.id = Takes.class where Takes.member = '{user}' and Classes.date = '{result[0]}' and Classes.time = '{result[1]}'")
                    if(db.rowcount != 0):
                        print("You are registered in a class during this time")
                        userSchedule(user)
                    else:
                        db.execute(f"select date,time from Sessions where id = '{session[0]}'")
                        old = db.fetchone()
                        db.execute(f"update Sessions set date = '{result[0]}',time = '{result[1]}' where id = '{session[0]}'")
                        conn.commit()
                        db.execute(f"delete from Availabilities where Availabilities.trainer = '{trainer}' and Availabilities.date = '{result[0]}' and Availabilities.time = '{result[1]}'")
                        conn.commit()
                        db.execute(f"insert into Availabilities(trainer,date,time) values('{trainer}','{old[0]}','{old[1]}')")
                        conn.commit()
                        print("Session rescheduled")
                        displayUser(user)
                print("Invalid input please try again")
        else:
            choice = int(input("Type the id of the session you want to delete: "))
            db.execute(f"select 1 from Sessions where Sessions. id = '{choice}' and Sessions.member = '{user}'")
            if(db.rowcount != 0):
                db.execute(f"select trainer,date,time from Sessions where Sessions.id = '{choice}'")
                old = db.fetchone()
                db.execute(f"delete from Sessions where Sessions.id = '{choice}'")
                conn.commit()
                db.execute(f"insert into Availabilities(trainer,date,time) values('{old[0]}','{old[1]}','{old[2]}')")
                conn.commit()
                print("Deletion succesful")
                displayUser(user)
    else:
        print("Available Classes:")
        db.execute(f"select * from Classes where not(select exists(select 1 from Takes where Takes.member = '{user}' and Takes.class = Classes.id))")
        print("ID|Date|Time|Room")
        print(db.fetchall())
        while(True):
            choice = int(input("Type in the id of the class you want to join: "))
            db.execute(f"select 1 from Classes where Classes.id = '{choice}'")
            if(db.rowcount != 0):
                break
            print("There is no class with this id please try again")
        db.execute(f"select date,time from Classes where Classes.id = '{choice}'")
        result = db.fetchone()
        db.execute(f"select 1 from Sessions where member = '{user}' and date = '{result[0]}' and time = '{result[1]}'")
        if(db.rowcount != 0):
            print("You have a private session during this class time")
            userSchedule(user)
        db.execute(f"select 1 from Takes join Classes on Takes.class = Classes.id where Takes.member = '{user}' and Classes.date = '{result[0]}' and Classes.time = '{result[1]}'")
        if(db.rowcount != 0):
            print("You have another class during this class time")
            userSchedule(user)
        else:
            db.execute(f"insert into Takes(member,class) values('{user}','{choice}')")
            conn.commit()
            print("You have been added to the class")
            displayUser(user)


                 
def trainerSchedule(user):
    print("Availabilities:")
    db.execute(f"select date,time from Availabilities where Availabilities.trainer = '{user}' order by date,time")
    print(db.fetchall())
    choice = 0
    while(True):
        print("1. Add a new availability")
        print("2. Remove an availability")
        choice = int(input())
        if(choice >= 1 and choice <= 2):
            break
        print("Invalid input please try again")
    if(choice == 1):
        while(True):
            year = int(input("Type in a year: "))
            month = int(input("Type in a month: "))
            day = int(input("Type in a day: "))
            hour = int(input("Type in an hour: "))
            minute = int(input("Type in a number of minutes: "))
            date = datetime.date(year,month,day)
            time = datetime.time(hour,minute,0)
            db.execute(f"select 1 from Availabilities where Availabilities.trainer = '{user}' and Availabilities.date = '{date}' and Availabilities.time = '{time}'")
            if(db.rowcount == 0):
                db.execute(f"insert into Availabilities(trainer,date,time) values('{user}','{date}','{time}')")
                conn.commit()
                print("Availability added")
                trainerSchedule(user)
            else:
                print("You already have this availability please try again")
    else:
        while(True):
            choice = int(input("Please type 1 to remove the first availability, 2 to remove the second one, etc: "))
            db.execute(f"select count(date) from Availabilities where Availabilities.trainer = '{user}'")
            if(db.fetchone()[0] >= choice and choice >= 1):
                db.execute(f"select date,time from Availabilities order by date,time offset '{choice-1}' limit 1")
                result = db.fetchone()
                db.execute(f"delete from Availabilities where Availabilities.trainer = '{user}' and Availabilities.date = '{result[0]}' and Availabilities.time = '{result[1]}'")
                conn.commit()
                print("Deletion succesful")
                trainerSchedule(user)
            else:
                print("Invalid input please try again")

def searchMembers():
    print("Members:")
    db.execute("select id,first_name,last_name from Members")
    print(db.fetchall())
    choice = 0
    while(True):
        choice = int(input("Type in the id of the member who's profile you want to view: "))
        db.execute(f"select 1 from Members where Members.id = '{choice}'")
        if(db.rowcount != 0):
            db.execute(f'select first_name from Members where Members.id = {choice}')
            print(f"First name: {db.fetchone()[0]}")
            db.execute(f'select last_name from Members where Members.id = {choice}')
            print(f"Last name: {db.fetchone()[0]}")
            print("Exercises:")
            print("Name|Goal|Current Record|Routine")
            db.execute(f"select type,goal,current,method from Exercises where Exercises.member = '{choice}'")
            print(db.fetchall())
            print("Booked sessions:")
            db.execute(f"select first_name || ' ' || last_name as trainer,date,time from Sessions join Trainers on Sessions.trainer = Trainers.id where member = '{choice}'")
            print(db.fetchall())
            print("Registered classes:")
            db.execute(f"select time,date,room from Classes join Takes on Classes.id = Takes.class where member = '{choice}'")
            print(db.fetchall())
            break
        print("There is no member with this id please try again")
                
def classSchedule():
    print("Classes:")
    db.execute("select * from Classes order by date,time")
    print("ID|Time|Date|Room")
    print(db.fetchall())
    choice = 0
    while(True):
        print("1. Add a new class")
        print("2. Update an existing class")
        print("3. Delete a class")
        choice = int(input())
        if(choice >= 1 and choice <= 3):
            break
        print("Invalid input please try again")
    if(choice == 1):
        while(True):
            year = int(input("Type in a year: "))
            month = int(input("Type in a month: "))
            day = int(input("Type in a day: "))
            hour = int(input("Type in an hour: "))
            minute = int(input("Type in a number of minutes: "))
            date = datetime.date(year,month,day)
            time = datetime.time(hour,minute,0)
            room = input("Type in a room name: ")
            db.execute(f"select 1 from Classes where Classes.date = '{date}' and Classes.time = '{time}' and Classes.room = '{room}'")
            if(db.rowcount == 0):
                db.execute(f"insert into Classes(date,time,room) values('{date}','{time}','{room}')")
                conn.commit()
                print("Class added")
                classSchedule()
            else:
                print("There is already a class in this room at this time please try again")
    elif(choice == 2):
        while(True):
            choice = int(input("Type the id of the class you want to change: "))
            db.execute(f"select 1 from Classes where Classes.id = '{choice}'")
            if(db.rowcount != 0):
                id = choice
                db.execute(f"select date,time,room from Classes where Classes.id = '{id}'")
                result = db.fetchone()
                while(True):
                    print("1. Update the date")
                    print("2. Update the time")
                    print("3. Update the room")
                    choice = int(input())
                    if(choice >= 1 and choice <= 3):
                        break
                    print("Invalid input please try again")
                if(choice == 1):
                    while(True):
                        year = int(input("Type in a year: "))
                        month = int(input("Type in a month: "))
                        day = int(input("Type in a day: "))
                        date = datetime.date(year,month,day)
                        db.execute(f"select 1 from Classes where Classes.date = '{date}' and Classes.time = '{result[1]}' and Classes.room = '{result[2]}'")
                        if(db.rowcount == 0):
                            db.execute(f"update Classes set date = '{date}' where id = '{id}'")
                            conn.commit()
                            print("Update succesful")
                            classSchedule()
                        print("Changing to this date would cause a scheduling conflict")
                elif(choice == 2):
                    while(True):
                        hour = int(input("Type in an hour: "))
                        minute = int(input("Type in a number of minutes: "))
                        time = datetime.time(hour,minute,0)
                        db.execute(f"select 1 from Classes where Classes.date = '{result[0]}' and Classes.time = '{time}' and Classes.room = '{result[2]}'")
                        if(db.rowcount == 0):
                            db.execute(f"update Classes set time = '{time}' where id = '{id}'")
                            conn.commit()
                            print("Update succesful")
                            classSchedule()
                        print("Changing to this time would cause a scheduling conflict")
                else:
                    while(True):
                        room = input("Type in a room name: ")
                        db.execute(f"select 1 from Classes where Classes.date = '{result[0]}' and Classes.time = '{result[1]}' and Classes.room = '{room}'")
                        if(db.rowcount == 0):
                            db.execute(f"update Classes set room = '{room}' where id = '{id}'")
                            conn.commit()
                            print("Update succesful")
                            classSchedule()
                        print("Changing to this room would cause a scheduling conflict")
            print("There is no class with this id please try again")
    else:
        while(True):
            choice = int(input("Type the id of the class you want to delete: "))
            db.execute(f"select 1 from Classes where Classes.id = '{choice}'")
            if(db.rowcount != 0):
                db.execute(f"delete from Classes where Classes.id = '{choice}'")
                conn.commit()
                print("Deletion succesful")
                classSchedule()
            print("There is no class with this id please try again")

def manageEquipment():
    print("Equipment:")
    db.execute("select * from Equipment")
    print("Name|Needs Maintenance")
    print(db.fetchall())
    choice = 0
    while(True):
        choice = input("Type which equipment you would like to perform maintenance on: ")
        db.execute(f"select 1 from Equipment where Equipment.type = '{choice}'")
        if(db.rowcount != 0):
            db.execute(f"update Equipment set needs_maintenance = FALSE where type = '{choice}'")
            conn.commit()
            print("Maintenance Successful")
            manageEquipment()
        print("Invalid input please try again")

def processPayment():
    print("Members who haven't paid membership:")
    db.execute("select id,first_name,last_name from Members where Members.paid_fees = FALSE")
    print("ID|First|Last")
    print(db.fetchall())
    print("Sessions that haven't been paid for")
    db.execute("select id,member,trainer,date,time from Sessions where Sessions.paid_for = FALSE")
    print("ID|Member ID|Trainer ID|Date|Time")
    print(db.fetchall())
    choice = 0
    while(True):
        print("1. Collect payment for membership")
        print("2. Collect payment for sessions")
        choice = int(input())
        if(choice >= 1 and choice <= 2):
            break
        print("Invalid input please try again")
    if(choice == 1):
        while(True):
            choice = int(input("Type the id of the member whom you want to collect payment from: "))
            db.execute(f"select 1 from Members where Members.id = '{choice}' and Members.paid_fees = FALSE")
            if(db.rowcount != 0):
                db.execute(f"Update Members set paid_fees = TRUE where id = '{choice}'")
                conn.commit()
                print("Payment processed")
                processPayment()
            print("This member either doesn't exist or has already paid their fees please try again")
    else:
        while(True):
            choice = int(input("Type the id of the session you want to collect payment for: "))
            db.execute(f"select 1 from Sessions where Sessions.id = '{choice}' and Sessions.paid_for = FALSE")
            if(db.rowcount != 0):
                db.execute(f"Update Sessions set paid_for = TRUE where id = '{choice}'")
                conn.commit()
                print("Payment processed")
                processPayment()
            print("This session either doesn't exist or has already been paid for please try again")

def registerMember():
    fname = input("Type in your first name: ")
    lname = input("Type in your last name: ")
    db.execute(f"insert into Members(first_name,last_name,paid_fees) values('{fname}','{lname}',FALSE)")
    conn.commit()
    db.execute(f"select id from Members where Members.first_name = '{fname}' and Members.last_name = '{lname}' order by Members.id desc limit 1")
    id = db.fetchone()[0]
    print(f"This is your user ID that you will use to sign in: {id}")
    displayUser(id)


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
            db.execute(f"select 1 from Members where Members.id = '{choice}'")
            if(db.rowcount != 0):
                break
            print("Invalid ID please try again")
        displayUser(choice)
    elif(choice == 2):
        while(True):
            print("Please type in your trainer ID: ")
            choice = int(input())
            db.execute(f"select 1 from Trainers where Trainers.id = '{choice}'")
            if(db.rowcount != 0):
                break
            print("Invalid ID please try again")
        id = choice
        while(True):
            db.execute(f'select first_name from Trainers where Trainers.id = {id}')
            print(f"First name: {db.fetchone()[0]}")
            db.execute(f'select last_name from Trainers where Trainers.id = {id}')
            print(f"Last name: {db.fetchone()[0]}")
            print("1. View your schedule")
            print("2. Search for a member")
            choice = int(input())
            if(choice >= 1 and choice <= 2):
                break
            print("Invalid input please try again")
        if(choice == 1):
            trainerSchedule(id)
        else:
            searchMembers()
    else:
        while(True):
            print("Please type in your admin ID: ")
            choice = int(input())
            db.execute(f"select 1 from Admins where Admins.id = '{choice}'")
            if(db.rowcount != 0):
                break
            print("Invalid ID please try again")
        while(True):
            print("1. Manage class schedule")
            print("2. Manage equipment")
            print("3. Process payments")
            choice = int(input())
            if(choice >= 1 and choice <= 3):
                break
            print("Invalid input please try again")
        if(choice == 1):
            classSchedule()
        elif(choice == 2):
            manageEquipment()
        else:
            processPayment()

else:
    registerMember()







    

  




