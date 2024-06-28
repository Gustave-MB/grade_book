"""
@author : gbwiraye
@date:October 1, 2022

Description: This program consists of GradeBook class which employs course module to perform
different tasks.It also contains the GradeBook test function called under main to test whether 
GradeBook class is performing its assigned tasks.
"""
from course import Course

class GradeBook():
    """
    Description: GradeBook class uses Course class from course module to create academic related documents such as 
    transcripts.txt, passes.txt,referrals.txt, grades.txt,(roll_number)_transcript.txt,(course_id)_grades.txt
    """
    
    def __init__(self):
        """
        Description: set up instance variable __courses
        """
        self.__courses = {}
        
        # Accessor
    def get_courses(self):
        return self.__courses

    def find(self, roll_num):
        """
        Description: find function takes the roll number and return True if it exists
        or False if it does not exist
        
        Parameters
        ----------
        roll_num : string
        """
        courses = list(self.__courses.values()) # getting Course objects from courses dictionary
        # looping throung students in each classlist to see whether the given roll number exist 
        for course in courses:
            for student in course.get_classlist():
                if roll_num == student.get_roll_num(): #checking whether the roll number exists
                    return True # returns True roll number exists
        else:
            return False  # returns False if the roll number don't exist

    def print_transcript(self, roll_num):
        """
        Description: print_transcript function takes the student roll number and creates
        a transcript.txt file in results the folder
        Parameters
        ----------
        roll_num : string
        """
        
        if self.find(roll_num): # cheching whether the given roll number exist and proceed only when it does exist
            _ = 0            
            # Opening file in writing mode using context manager
            with open(f"results\{roll_num}_transcript.txt", 'w') as filewriter: 
                # looping through each course to generate the transcript of the given roll number
                for key, value in sorted(self.__courses.items()): # dictionary items are sorted in ascending order
                    for student in value.get_classlist():
                        if roll_num == student.get_roll_num(): # checking whether the student number matches to the one given
                            # Conditioning the filewriter so that upper page border, roll number, student name will be written once on the transcript
                            while _ == 0: # loop executes once
                                filewriter.write(f"\n{'-'*54}\n\n{student.get_roll_num():8s}{student.get_name():20s}\n")
                                _ += 1
                            # writing to the transcript each course's description, percentage and grades
                            filewriter.write(f"\n{value.get_course_id():8s}{value.get_course_name():35s}{student.percentage_gen():8.2f}  {student.grade_gen():3s}\n")
                filewriter.write(f"\n{'-'*54}\n\n") # bottom page border
        else: print(f"Roll number '{roll_num}' doen't exist") # Notifying the user that the roll number doesn't exist

    def course_files_reader(self):
        """
        Description: this function prompts the user to enter 5 comma separated course names
            and store each course's information in courses dictionary such that course ID is
            the key and course object is the value 
        """
        # prompting the user to enter the comma separated course names and storing them as a list
        course_files = (input("please enter courses file names as comma separated\n")).split(",")
        courseList = ["course1","course2","course3","course4","course5"] # List of courses that exists
        
        for course in course_files:
            if (len(course) >= 7) and (course[:7] in courseList): # checking if the course entered are valid
                file_path = f"data\{course[0:7]}.txt" # giving all course names text file extension
    
                course_inst = Course() # creating a course object
                course_inst.add_course_data_from_file(file_path) # adding course data to the course object
                course_inst.add_students_from_file(file_path) # adding student data to the course object
                self.__courses[f"{course_inst.get_course_id()}"] = course_inst # assigning to the courses dictionary course ID as the key and course object holding all the data as value
            else:
                print(f"'{course} doen't exist'\n") # If there is any wrong course entered, the user will notified
                
    def passed_student(self):
        """
        Description: This function checks for students with marks greater than 60 in all courses
        and creates a text file named passes.txt with list of their names and roll number
        Returns
        -------
        passed_Student : set
        this program returns a set containing the students with pass
        """
        # Opening file in writing mode using context manager
        with open("results\passes.txt", 'w') as filewriter:
            failled_students = set() # A set of failled student
            students = set() # A set of all students
            
            # looping through the course to check for students with less than 60% in any course
            for value in self.__courses.values():
                for student in value.get_classlist():
                    if student.percentage_gen() < 60:
                        std= (student.get_roll_num(),student.get_name()) # creating a tuple of roll number and name of failled student
                        failled_students.add(std) # adding failled student to the set of failled students
                    # storing names and roll number of all students and addond them to the set of all students
                    studnt= (student.get_roll_num(),student.get_name())  
                    students.add(studnt)
            # checking for differnce between set of all students and the set of failled students to get passed students
            passed_Student = students.difference(failled_students)
            for student in passed_Student:
                filewriter.write(f"{student[0]:8s}{student[1]:20s}\n") # writing to passes.txt the passed student           
            return passed_Student
            #context manager will close the file properly


    def referrals(self):
        """
        Description: This function checks for students with grade 'E' in any course  and creates 
        a referrals.txt file with list of their names, roll number as well as course IDs and 
        course names of the courses they have grade 'E'
        """
        try:
            # Opening file in writing mode using context manager
            with open(r"results\referrals.txt",'w') as filewriter:
                # loop through courses for each student to identify those with referrals and their corresponding courses
                for stdent in list(self.__courses.values())[0].get_classlist(): # retrieve students from classlist in Course objects
                    roll_num = stdent.get_roll_num()
                    _=0
                    # looping through courses' marks to identify students with grade E
                    for course in self.__courses.values(): 
                        for student in course.get_classlist():
                            if (roll_num == student.get_roll_num()) and (student.grade_gen() == "E"):
                                while _==0: # loop executes once
                                    _+=1
                                    filewriter.write(f"{student.get_roll_num():8s}{student.get_name():20s}\n")
                                filewriter.write(f"{' '*8}{course.get_course_id():8s}{course.get_course_name():35s}\n")
            #context manager will close the file properly
        except:
            print("Opps! invalid course!\n")
    def all_grades(self,passed_student):
        """
        Description: all_grades function creates grades.txt file with a list of students, their grades
        in each course, average marks and the name and roll number of the best student 
        """
        try: # try prevents list indexing error of courses' keys for courses less than 5 
            with open("results\grades.txt", 'w') as filewriter:
                classlist = list(self.__courses.values())[0].get_classlist() # retrieve classlist
                ID = sorted(self.__courses.keys()) # store sorted course IDs in a list
                # writing to the title to file using name, roll nnumber and course IDs
                filewriter.write(f"Name\t  roll_num\t\t\t {ID[0]:8s}{ID[1]:8s}{ID[2]:8s}{ID[3]:8s}{ID[4]:8s}\tAvg\n")
                marks = {} # empty dictionary for storing student names and roll number with their respective average marks
                passed_max = {} # dictionary for storing passed students with their average marks
                # loop through all students and generate percentage of marks in each course and total averagee
                for studnt in classlist:
                    roll_num = studnt.get_roll_num()
                    std_name = studnt.get_name()
                    # writing the student roll number, name and each courses percentage to grades.txt
                    filewriter.write(f"{roll_num:8s}{std_name:20s}")
                    summation = 0
                    for ID, course in sorted(self.__courses.items()):
                        for student in course.get_classlist():
                            if roll_num == student.get_roll_num():
                                # compute percentage marks
                                percentage = student.percentage_gen()
                                # compute moving total
                                summation += percentage
                                filewriter.write(f"{percentage:8.2f}")
                                
                    # compute average
                    average = summation/5
                    marks[f"{roll_num},  {std_name:17s}"] = average # store student names and roll number as key and the average as value
                    filewriter.write(f" {average:8.2f}\n")
                # find students with pass mark and store their corresponding data
                for std,mark in marks.items():
                    student = std.split(",")
                    for stdnt in passed_student:
                        if student[0]==stdnt[0]: # Check whether the student is among those with pass
                            passed_max[std] = mark
                
                max_marks = max(passed_max.values()) # compute maximum average
                # find the best student with maximum marks among those with pass and write to the text file
                best_student = str([student for student, mark in passed_max.items() if mark == max_marks])
                best_student = best_student.replace("[", "").replace("]", "").replace("'", "")
                filewriter.write(f"\nBest Student: {best_student}\n")
        except: 
            print("Expected 5 courses, Please enter all courses correctly\n")

    def course_grades(self, course_id):
        """
        Description: this function takes course ID and creates grades.txt file with a list of students'roll number,
        name and their corresponding average marks and grade in that particular course
        Parameters
        ----------
        course_id : string
        """
        
        with open(f"results\{course_id}_grades.txt", 'w') as filewriter:
            course = self.__courses[course_id] # retrieve the course object using the course ID
            # loop through the classlist and write student roll number, name, percentage ang grade to the file
            for student in course.get_classlist():
                roll_nber = student.get_roll_num()
                std_name = student.get_name()
                # compute percentage
                percentage = student.percentage_gen()
                # compute grade
                grade = student.grade_gen()
                filewriter.write(f"{roll_nber:8s}{std_name:20s}{percentage:8.2f}  {grade:3s}\n")

    def all_transcripts(self):
        """
        Description: this function reads each student's data in each course and generate transcripts
        for each student in one text file
        """
        
        try:
            # open text file in writing mode using context manager
            with open(r"results\transcripts.txt", 'w') as filewriter:
                classlist = list(self.__courses.values())[0].get_classlist()
                # loop through the classlist and get one student's name and roll number at time write to the transcript
                for studnt in classlist:
                    roll_num = studnt.get_roll_num()
                    std_name = studnt.get_name()
                    filewriter.write(f"\n{'-'*54}\n\n{roll_num:8s}{std_name:20s}\n")
                    # loop through course and generate transcripts for student
                    for ID, course in sorted(self.__courses.items()):
                        for student in course.get_classlist():
                            if roll_num == student.get_roll_num():
                               
                                filewriter.write(f"\n{ID:8s}{course.get_course_name():35s}{student.percentage_gen():8.2f}  {student.grade_gen():3s}\n")
                    filewriter.write(f"\n{'-'*54}\n\n")
        except:
            print("No course found!")


##########################################################################


def test_grade_book():
    """
    Testing the Gradebook using some of its methods and generate different academic documents
    """
    course_id = input("Enter course ID\n")
    roll_num = input("Enter roll number\n")
    grade = GradeBook()
    grade.course_files_reader()
    grade.print_transcript(roll_num)
    passed_student=grade.passed_student()
    grade.all_transcripts()
    grade.all_grades(passed_student)
    grade.referrals()
    if course_id in grade.get_courses().keys():
        grade.course_grades(course_id)
    else:
        print(f"The course ID '{course_id}' does not exist\n")    
    

def main():
    test_grade_book()


if __name__ == "__main__":
    main()