create table Members(
    id Serial Primary Key,
    first_name Varchar(255),
    last_name Varchar(255),
    paid_fees Boolean
);

create table Trainers(
    id Serial Primary Key,
    first_name Varchar(255),
    last_name Varchar(255),
    price Int
);

create table Sessions(
    id Serial Primary Key,
    member Int,
    trainer Int,
    time Time,
    date Date,
    paid_for Boolean,
    Foreign Key(member) references Members(id) On Delete Cascade On Update Cascade,
    Foreign Key(trainer) references Trainers(id) On Delete Cascade On Update Cascade
);

create table Classes(
    id Serial Primary Key,
    time Time,
    date Date,
    room Varchar(255)
);

create table Takes(
    member Int,
    class Int ,
    Foreign Key(member) references Members(id) On Delete Cascade On Update Cascade,
    Foreign Key(class) references Classes(id) On Delete Cascade On Update Cascade,
    Primary Key(member,class)
);

create table Exercises(
    member Int,
    type Varchar(255),
    goal Varchar(255),
    current Varchar(255),
    method Varchar(255),
    Foreign Key(member) references Members(id) On Delete Cascade On Update Cascade,
    Primary Key(member,type)
);

create table Availabilities(
    trainer int,
    time Time,
    date Date,
    Foreign Key(trainer) references Trainers(id) On Delete Cascade On Update Cascade,
    Primary Key(trainer,time,date)
);

create table Equipment(
    type Varchar(255) Primary Key,
    needs_maintenance Boolean
);

create table Admins(
    id Serial Primary Key
);