INSERT INTO Members (first_name, last_name, paid_fees)
VALUES ('John', 'Doe', FALSE),
       ('Alice', 'Smith', FALSE),
       ('Michael', 'Johnson', FALSE);

INSERT INTO Trainers (first_name, last_name, price)
VALUES ('Emily', 'Brown', 50),
       ('David', 'Wilson', 60),
       ('Sarah', 'Jones', 55);

INSERT INTO Sessions (member, trainer, time, date,paid_for)
VALUES (1, 1, '10:00:00', '2024-03-28',FALSE),
       (2, 2, '12:00:00', '2024-03-29',FALSE),
       (3, 3, '14:00:00', '2024-03-30',FALSE);

INSERT INTO Classes (time, date, room)
VALUES ('08:00:00', '2024-03-28', 'Room A'),
       ('10:00:00', '2024-03-29', 'Room B'),
       ('12:00:00', '2024-03-30', 'Room C');

INSERT INTO Takes (member, class)
VALUES (1, 1),
       (2, 2),
       (3, 3);

INSERT INTO Exercises (member, type, goal, current, method)
VALUES (1, 'Weight', '150 pounds', '175 pounds', 'Go vegan'),
       (2, 'Bench Press', '200 pounds', '100 pounds', '3 sets of 10 3 times a week'),
       (3, 'Mile Run', '5 minutes', '7 minutes', 'Run a mile everyday');

INSERT INTO Availabilities (trainer, time, date)
VALUES (1, '10:00:00', '2024-03-28'),
       (2, '12:00:00', '2024-03-29'),
       (3, '14:00:00', '2024-03-30');

INSERT INTO Equipment (type, needs_maintenance)
VALUES ('Treadmill', FALSE),
       ('Dumbbells', FALSE),
       ('Yoga mats', TRUE);

INSERT INTO Admins DEFAULT VALUES;

