USE classmatch;

-- USERS
INSERT INTO users (email, password_hash, name, major, year, avatar, bio, study_prefs) VALUES
('alice.smith@university.edu','password123','Alice Smith','Computer Science','Junior','AS',
 'Love coding and collaborative learning. Looking for serious study partners!',
 JSON_OBJECT('times', JSON_ARRAY('Morning','Afternoon'),
             'location', JSON_ARRAY('Library','Coffee Shop'),
             'style', 'Group Discussion')),
('bob.johnson@university.edu','password123','Bob Johnson','Computer Science','Senior','BJ',
 'Senior CS major, happy to help underclassmen. Work-study friendly hours.',
 JSON_OBJECT('times', JSON_ARRAY('Evening','Weekend'),
             'location', JSON_ARRAY('Library','Online'),
             'style', 'One-on-One')),
('carol.williams@university.edu','password123','Carol Williams','Software Engineering','Sophomore','CW',
 'Passionate about web dev and databases. Let''s build projects together!',
 JSON_OBJECT('times', JSON_ARRAY('Afternoon','Evening'),
             'location', JSON_ARRAY('Campus Center','Online'),
             'style', 'Group Discussion')),
('david.brown@university.edu','password123','David Brown','Computer Science','Junior','DB',
 'Early bird coder. Prefer morning study sessions and structured learning.',
 JSON_OBJECT('times', JSON_ARRAY('Morning'),
             'location', JSON_ARRAY('Library','Engineering Lab'),
             'style', 'Structured Study')),
('emma.davis@university.edu','password123','Emma Davis','Data Science','Junior','ED',
 'Data enthusiast! Looking for project partners and algorithm study buddies.',
 JSON_OBJECT('times', JSON_ARRAY('Afternoon','Evening'),
             'location', JSON_ARRAY('Library','Coffee Shop'),
             'style', 'Project-Based')),
('frank.miller@university.edu','password123','Frank Miller','Computer Science','Senior','FM',
 'Final year CS student. Capstone partner needed. Also tutoring data structures.',
 JSON_OBJECT('times', JSON_ARRAY('Afternoon','Weekend'),
             'location', JSON_ARRAY('Innovation Center','Online'),
             'style', 'Project-Based'));

-- COURSES
INSERT INTO courses (id, code, name, section, instructor, schedule, students, building, room) VALUES
('CS1101','CS 1101','Introduction to Computer Science','001','Dr. Sarah Johnson','MWF 9:00-10:00 AM',45,'Engineering Hall','201'),
('CS2201','CS 2201','Data Structures and Algorithms','002','Prof. Michael Chen','TR 2:00-3:30 PM',38,'Science Building','315'),
('CS3310','CS 3310','Database Systems','001','Dr. Emily Rodriguez','MWF 11:00-12:00 PM',32,'Engineering Hall','405'),
('CS4090','CS 4090','Capstone Project I','001','Prof. David Williams','MW 3:00-4:30 PM',25,'Innovation Center','102'),
('MATH2410','MATH 2410','Discrete Mathematics','003','Dr. Lisa Anderson','TR 9:30-11:00 AM',40,'Math Building','210'),
('CS3320','CS 3320','Web Development','001','Prof. James Martinez','TR 12:30-2:00 PM',35,'Engineering Hall','301'),
('CS2301','CS 2301','Computer Architecture','002','Dr. Robert Taylor','MWF 1:00-2:00 PM',42,'Science Building','220'),
('CS3380','CS 3380','Artificial Intelligence','001','Dr. Amanda Lee','TR 3:30-5:00 PM',30,'Innovation Center','205');

-- ENROLLMENTS
INSERT INTO enrollments (user_id, course_id) VALUES
((SELECT id FROM users WHERE email='alice.smith@university.edu'),'CS2201'),
((SELECT id FROM users WHERE email='alice.smith@university.edu'),'CS3310'),
((SELECT id FROM users WHERE email='alice.smith@university.edu'),'MATH2410'),

((SELECT id FROM users WHERE email='bob.johnson@university.edu'),'CS4090'),
((SELECT id FROM users WHERE email='bob.johnson@university.edu'),'CS3380'),

((SELECT id FROM users WHERE email='carol.williams@university.edu'),'CS2201'),
((SELECT id FROM users WHERE email='carol.williams@university.edu'),'CS3320'),
((SELECT id FROM users WHERE email='carol.williams@university.edu'),'CS3310'),

((SELECT id FROM users WHERE email='david.brown@university.edu'),'CS2301'),
((SELECT id FROM users WHERE email='david.brown@university.edu'),'MATH2410'),
((SELECT id FROM users WHERE email='david.brown@university.edu'),'CS3310'),

((SELECT id FROM users WHERE email='emma.davis@university.edu'),'CS2201'),
((SELECT id FROM users WHERE email='emma.davis@university.edu'),'CS3380'),
((SELECT id FROM users WHERE email='emma.davis@university.edu'),'MATH2410'),

((SELECT id FROM users WHERE email='frank.miller@university.edu'),'CS4090'),
((SELECT id FROM users WHERE email='frank.miller@university.edu'),'CS3380');

-- AVAILABILITY (free-text)
INSERT INTO availability_text (user_id, slot) VALUES
((SELECT id FROM users WHERE email='alice.smith@university.edu'),'Monday 10am-12pm'),
((SELECT id FROM users WHERE email='alice.smith@university.edu'),'Wednesday 2pm-4pm'),
((SELECT id FROM users WHERE email='alice.smith@university.edu'),'Friday 1pm-3pm'),

((SELECT id FROM users WHERE email='bob.johnson@university.edu'),'Tuesday 6pm-8pm'),
((SELECT id FROM users WHERE email='bob.johnson@university.edu'),'Thursday 6pm-8pm'),
((SELECT id FROM users WHERE email='bob.johnson@university.edu'),'Saturday 10am-2pm'),

((SELECT id FROM users WHERE email='carol.williams@university.edu'),'Monday 3pm-5pm'),
((SELECT id FROM users WHERE email='carol.williams@university.edu'),'Wednesday 3pm-5pm'),
((SELECT id FROM users WHERE email='carol.williams@university.edu'),'Friday 4pm-6pm'),

((SELECT id FROM users WHERE email='david.brown@university.edu'),'Monday 8am-10am'),
((SELECT id FROM users WHERE email='david.brown@university.edu'),'Wednesday 8am-10am'),
((SELECT id FROM users WHERE email='david.brown@university.edu'),'Friday 9am-11am'),

((SELECT id FROM users WHERE email='emma.davis@university.edu'),'Tuesday 2pm-5pm'),
((SELECT id FROM users WHERE email='emma.davis@university.edu'),'Thursday 2pm-5pm'),

((SELECT id FROM users WHERE email='frank.miller@university.edu'),'Monday 1pm-4pm'),
((SELECT id FROM users WHERE email='frank.miller@university.edu'),'Wednesday 1pm-4pm'),
((SELECT id FROM users WHERE email='frank.miller@university.edu'),'Saturday 2pm-6pm');

-- GROUPS (note the backticks)
INSERT INTO `groups` (owner_user_id, course_id, name, description, meeting_time, location, max_members, tags)
VALUES
((SELECT id FROM users WHERE email='alice.smith@university.edu'),'CS2201',
 'Data Structures Study Circle',
 'Weekly meetups to go over lecture material and practice coding problems together.',
 'Wednesdays 3:00 PM','Library Study Room 3B',6,
 JSON_ARRAY('Algorithms','Coding Practice','Weekly Meetings')),

((SELECT id FROM users WHERE email='bob.johnson@university.edu'),'CS4090',
 'Capstone Project Team Alpha',
 'Building a student matching platform. Need frontend and backend developers.',
 'Mondays & Wednesdays 4:00 PM','Innovation Center Room 102',4,
 JSON_ARRAY('Project Team','Full Stack','Agile')),

((SELECT id FROM users WHERE email='alice.smith@university.edu'),'CS3310',
 'Database Design Workshop',
 'Hands-on practice with SQL, normalization, and database design patterns.',
 'Fridays 2:00 PM','Engineering Hall Lab 405',5,
 JSON_ARRAY('SQL','Database Design','Hands-on')),

((SELECT id FROM users WHERE email='emma.davis@university.edu'),'CS3380',
 'AI & ML Study Group',
 'Exploring machine learning algorithms and AI concepts. Python heavy!',
 'Thursdays 5:30 PM','Online (Discord)',8,
 JSON_ARRAY('Machine Learning','Python','Theory + Practice'));

-- GROUP MEMBERS (owners are admins; do NOT re-add owner as member)
-- g1
INSERT INTO group_members (group_id, user_id, role)
SELECT g.id, u.id, 'admin'
FROM `groups` g JOIN users u ON u.email='alice.smith@university.edu'
WHERE g.name='Data Structures Study Circle';

INSERT INTO group_members (group_id, user_id, role)
SELECT g.id, u.id, 'member'
FROM `groups` g JOIN users u ON u.email IN ('carol.williams@university.edu','emma.davis@university.edu')
WHERE g.name='Data Structures Study Circle';

-- g2
INSERT INTO group_members (group_id, user_id, role)
SELECT g.id, u.id, 'admin'
FROM `groups` g JOIN users u ON u.email='bob.johnson@university.edu'
WHERE g.name='Capstone Project Team Alpha';

INSERT INTO group_members (group_id, user_id, role)
SELECT g.id, u.id, 'member'
FROM `groups` g JOIN users u ON u.email IN ('frank.miller@university.edu')
WHERE g.name='Capstone Project Team Alpha';

-- g3
INSERT INTO group_members (group_id, user_id, role)
SELECT g.id, u.id, 'admin'
FROM `groups` g JOIN users u ON u.email='alice.smith@university.edu'
WHERE g.name='Database Design Workshop';

INSERT INTO group_members (group_id, user_id, role)
SELECT g.id, u.id, 'member'
FROM `groups` g JOIN users u ON u.email IN ('carol.williams@university.edu','david.brown@university.edu')
WHERE g.name='Database Design Workshop';

-- g4
INSERT INTO group_members (group_id, user_id, role)
SELECT g.id, u.id, 'admin'
FROM `groups` g JOIN users u ON u.email='emma.davis@university.edu'
WHERE g.name='AI & ML Study Group';

INSERT INTO group_members (group_id, user_id, role)
SELECT g.id, u.id, 'member'
FROM `groups` g JOIN users u ON u.email IN ('bob.johnson@university.edu','frank.miller@university.edu')
WHERE g.name='AI & ML Study Group';
