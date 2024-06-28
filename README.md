# Grade book application
A grade book maintains a record of scores that students have in all courses that they have 
registered for. In addition, a grade book provides a list of all students who have 
passed as well as a list of students who have course referrals/fails. A student is 
considered to have failed if they have less than 60 in any course they have 
undertaken. Each student undertakes five courses. For each course, each student 
does five assignments as seen in the class Student. Each student object can 
generate the student’s average mark using the method percentage_gen. See 
Student class. Each course maintains the following details: instructor, TAs, 
semester, course name, and class list. The class list maintains a list of Student 
objects – i.e., the students who have registered for the course. This is shown in the 
Course class.

* student.py: contains definition for the Student classes.
* course.py: contains definition for the Course classes.
* gradebook.py: contains GradeBook class and test_grade_book function.
* course1.txt, course2.txt, course3.txt, course4.txt, course5.txt: sample input files in 
data folder.

Below is a sample input file(course1.txt):

04808E

Programming and Problem Solving II

Fall 2021

Frank Ike

Fikita, Nikita, Vikita

S1000:George Williams:80:90:70:99:60

S1002:Elaine Hazimana:85:86:78:99:89

S1003:Peter Pathos:70:90:70:95:91

S1005:Celestine Taylor:60:95:88:99:100

S1006:Khalil Abdi:80:82:75:92:86

**Where:** First line: course id; Second line: course name; Third line: semester; 
Fouth line: instructor; Fifth line: list of TAs; and Subsequent lines: student 
details (roll number, name, and marks for the assignments).

**Assumption:** All students have registered for the same five courses. All students 
have done five assignments per course. Therefore, there is no missing assignment 
mark.
