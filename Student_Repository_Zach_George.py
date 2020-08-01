'''
Created on Jul 13, 2020
This assignment is the start to creating a repository of courses, 
students, and instructors. 
A Student Class and Instructor Class are made which are used with the
University Class.
These two classes are only initialized and have their own capabilities
to print Pretty Tables.
The University Class reads in a _directory path and finds the files for
students, instructors, and grades.
The grades file is analyzed and modifies each individual Student and 
Instructor object 
The main part of the function asks the user for a _directory path of the 
University's files and then outputs the results.

Updates 7/21/2020
Added Major class to read majors for a university
Major class determines the required courses and remaining courses and electives needed for a student 
Added GPA output for student 
@author: Zachary George
'''
from collections import defaultdict
from typing import Dict, Iterator, List, Tuple, DefaultDict, Optional, Set
from prettytable import PrettyTable
import os
import sqlite3
    
def _file_reader(path: str, fields: int, sep: str, header: bool) -> Iterator[List[str]]:
    
    """ Return a formatted list of strings from a file """
    
    if type(fields) is not int or type(sep) is not str or type(header) is not bool:
        raise TypeError('One or more of the arguments are of' + 
                        'the incorrect type. Please try again.')
    
    try:
        fp = open(path, 'r')
        
    except FileNotFoundError as e:
        raise FileNotFoundError(f'{path} could not be opened. Please try again') from e
    
    else:
        line_count: int = 0
        
        with fp:
            
            if header is True:
                first_line = fp.readline().rstrip('\n').split(sep)
                if len(first_line) != fields:
                    raise ValueError(f'{path} has {len(first_line)} arguments in' + 
                                    (f'the header instead of {fields}.'))
                
            for line in fp:
                line_count += 1
                line = line.rstrip('\n')
                if len(line.split(sep)) != fields:
                    raise ValueError(f'{path} has {len(line.split(sep))} arguments on line' +
                                     (f'{line_count} instead of {fields}.'))
                
                else:
                    yield line.split(sep)
                    
                    
class Major:
    
    
    """ Defines the attributes and methods of Major Class """
    
    
    def __init__(self, name: str) -> None:     
        
        """ Initialize a Major """
        
        self._name: str = name
        self._required_courses: Set[str] = set()
        self._required_electives: Set[str] = set()
        
    def add_requirement(self, course: str, require: str):
        
        """ Add a required course or elective to its proper set """
        
        if require == 'R':
            self._required_courses.add(course)
        
        if require == 'E':
            self._required_electives.add(course)
        
    def _remaining_courses(self, passed_courses: Set[str]) -> Set[str]:
        
        """ Determine the remaining courses of a student based off of their major """
        
        if len(self._required_courses.difference(passed_courses)) == 0:
            return {}
        
        else:
            return self._required_courses.difference(passed_courses)
    
    def _remaining_electives(self, passed_courses: Set[str]) -> Set[str]: 
        
        """ Determine the remaining electives of a student based off of their major """
        
        if len(passed_courses.intersection(self._required_electives)) > 0:
            return {}
          
        else:
            return set(self._required_electives)
        
    def summary_pretty_table(self) -> PrettyTable:
        
        """ Print a pretty table for the student's courses and grades """
        
        pt: PrettyTable = PrettyTable(field_names= ['Course', 'R/E?'])
        
        for course in self._required_courses:
            pt.add_row([course, 'R'])
        
        for elective in self._required_electives:
            pt.add_row([elective, 'E'])
            
        return pt
    
    def add_pt_row(self) -> Tuple[str, Set[str], Set[str]]:
        
        """ Add a row of information for a major for a pretty table """
        
        return self._name, self._required_courses, self._required_electives
             
                    
class Student:
    
    
    """ Defines the attributes and methods of the Student class """
    
    def __init__(self, cwid: str, name: str, major: Major) -> None:
        
        """ Define the attributes of a Student object """
        
        self._cwid: str = cwid
        self._name: str = name
        self._major: Major = major
        self._courses_grades: Dict[str, str] = dict() #key: course name value: grade earned
        self._required_courses: Set[str] = self._major._required_courses
        self._required_electives: Set[str] = self._major._required_electives
        self._completed_courses: Set[str] = set()
        self._remaining_courses: Set[str] = set()
        self._remaining_electives: Set[str] = set()
                
    def _calculate_gpa(self) -> Optional[float]:
        
        """ Calculate the GPA for a student """
        
        gpa_scale: Dict[str, float] = {'A': 4.0, 'A-': 3.75, 'B+': 3.25, 'B': 3.0, 'B-': 2.75, 'C+': 2.25, 
                                       'C': 2.0, 'C-': 0, 'D+': 0, 'D': 0, 'D-': 0, 'F': 0}
        
        if len(self._courses_grades) == 0:
            return None
        else:
            return round(sum(gpa_scale[key] for key in self._courses_grades.values()) 
                         / len(self._courses_grades.values()), 2)
            
    def add_course_grade(self, course: str, grade: str) -> None:
        
        """ Add a course and grade to the student """
    
        self._courses_grades[course] = grade
        
    def add_completed_course(self, course: str, grade: str) -> None:
        
        """ Add a completed course to the student """

        if grade in ['A', 'A-', 'B+', 'B', 'B-', 'C+', 'C']:
            self._completed_courses.add(course)
    
    def find_remaining_courses(self) -> None:
        
        """ Find the remaining courses for a student """
        
        self._remaining_courses = self._major._remaining_courses(self._completed_courses)
        
    def find_remaining_electives(self) -> None:
        
        """ Find the remaining electives for a student """
        
        self._remaining_electives = self._major._remaining_electives(self._completed_courses)
            
    def _summary_pretty_table(self) -> PrettyTable:
        
        """ Print a pretty table for the student's courses and grades """
        
        pt: PrettyTable = PrettyTable(field_names= ['Course', 'Grade'])
        
        for course, grade in self._courses_grades.items():
            pt.add_row([course, grade])
            
        return pt
    
    def add_pt_row(self) -> Tuple[str, str, str, List[str], Set[str], Set[str], int]:
        
        """ Return a tuple of information needed for a pretty table """
        
        return self._cwid, self._name, self._major._name, sorted(list(self._completed_courses)), self._remaining_courses, self._remaining_electives, self._calculate_gpa()
    
    
class Instructor:
    
    
    """ Defines the attributes and methods of the Instructor class """
    
    
    def __init__(self, cwid: str, name: str, department: str) -> None:
        
        """ Define the attributes of an Instructor object """
        
        self._cwid: str = cwid
        self._name: str = name
        self._department: str = department
        self._courses_students: DefaultDict[str, int] = defaultdict(int) #key: course name value: number of students in course
        
    def add_course_student(self, course: str) -> None:
        
        """ Add a student to a course """
        
        self._courses_students[course] += 1
    
    def _summary_pretty_table(self) -> PrettyTable:
        
        """ Print a pretty table for an instructors and their 
        courses with number of students """
        
        pt: PrettyTable = PrettyTable(field_names= ['Course', 'Number of Students'])
        
        for course, students in self._courses_students.items():
            pt.add_row([course, students])
            
        return pt
    
    def add_pt_rows(self) -> Iterator[Tuple[str, str, str, str, int]]:
        
        """ Yield rows for a pretty table for all instructors """
        
        for course, count in self._courses_students.items():
            yield self._cwid, self._name, self._department, course, count
    
                  
class University:
    
    
    """ Defines the attributes and methods of the University class """
    
    def __init__(self, directory: str) -> None:
        
        """ Defines the attributes of a University object """
        
        if type(directory) is not str:
            raise TypeError(f'{directory} is not a string. Please try again.')
        
        try:
            os.chdir(directory)
            self._directory: List[str] = os.listdir(directory)
            
        except FileNotFoundError as e:
            raise FileNotFoundError(f'{directory} could not be opened.') from e
        
        self._majors: Dict[str, Major] = self._majors_information() #key: major name value: Major information
        
        self._students: Dict[str, Student] = self._students_information() #key: cwid value: Student
        self._instructors: Dict[str, Instructor] = self._instructors_information() #key: cwid value: Instructor
        
        self.__process_grades()
        
    def _majors_information(self) -> List[Tuple[str, str, List[str]]]:
        
        """ Read the information about majors """
        
        majors: Dict[str, Major] = dict() #key: major value: Major
        
        if 'majors.txt' in self._directory: 
            
            for major, require, course in _file_reader('majors.txt', fields=3, sep='\t', header=True):
                if major not in majors:
                    majors[major] = Major(major)
                    
                majors[major].add_requirement(course, require)
                
        else:
            raise ValueError('The majors file does not exist. Please try again.')
                
        return majors
                    
    def _students_information(self) -> Dict[str, Student]:
        
        """ Read information about the students """
        
        students: Dict[str, Student] = dict() #key: cwid value: Student object
        
        if 'students.txt' in self._directory:
            
            for cwid, name, major in _file_reader('students.txt', fields=3, sep='\t', header=True):
                
                if major not in self._majors:
                    raise KeyError(f'An unexpected major was found: {major}')
                
                else:
                    students[cwid] = Student(cwid, name, self._majors[major])
                
        else:
            raise ValueError('The students file does not exist. Please try again.')
                    
        return students
    
    def _instructors_information(self) -> Dict[str, Instructor]:
        
        """ Read information about the instructors """
        
        instructors: Dict[str, Instructor] = dict() #key: cwid value: Instructor object
        
        if 'instructors.txt' in self._directory:
            
            for cwid, name, department in _file_reader('instructors.txt', fields=3, sep='\t', header=True):
                instructors[cwid] = Instructor(cwid, name, department)

        else:
            raise ValueError('The instructors file does not exist. Please try again.')
                         
        return instructors
                      
    def __process_grades(self) -> None:
        
        """ Process the grades for each students """
                 
        if 'grades.txt' in self._directory:
                
            for student_cwid, course, grade, instructor_cwid  in _file_reader('grades.txt', fields=4, sep='\t', header=True):
                
                if student_cwid not in self._students:
                    raise KeyError(f'An unidentified student was found: {student_cwid}')
                
                else:
                    self._students[student_cwid].add_course_grade(course, grade)
                    self._students[student_cwid].add_completed_course(course, grade)
                            
                if instructor_cwid not in self._instructors:
                    raise KeyError(f'An unidentified instructor was found: {instructor_cwid}')
                
                else:
                    self._instructors[instructor_cwid].add_course_student(course)
            
            for student in self._students.values():
                student.find_remaining_courses()
                student.find_remaining_electives()      
                                                         
        else:
            raise ValueError('The grades file does not exist. Please try again.')
                  
    def print_students_pt(self) -> None:
        
        """ Print a prettytable of students """
        
        print('Student Summary')
        pt: PrettyTable = PrettyTable(field_names=['CWID', 'Name', 'Major', 'Completed Courses', 'Remaining Required', 
                                                   'Remaining Electives', 'GPA'])
        
        for student in self._students.values():
            pt.add_row(student.add_pt_row())
            
        print(pt)   
                
    def print_instructors_pt(self) -> None:
        
        """ Print a prettytable of instructors """
        
        print('Instructor Summary')
        pt: PrettyTable = PrettyTable(field_names=['CWID', 'Name', 
                                                   'Dept', 'Course', 'Students'])
        
        for instructor in self._instructors.values():
            for row in instructor.add_pt_rows():
                pt.add_row(row)
                
        print(pt)
    
    def print_majors_pt(self) -> None:
        
        """ Print a pretty table of majors """
        
        print('Majors Summary')
        pt: PrettyTable = PrettyTable(field_names=['Major', 'Required Courses', 'Required Electives'])
        
        for major in self._majors.values():
            pt.add_row(major.add_pt_row())
        
        print(pt)
        
    def student_grades_table_db(self, db_path: str) -> None:
        
        """ Print a pretty table of the student grades from a database file """
        
        db: sqlite3.Connection = sqlite3.connect(db_path)
        
        query: str = """select s.Name, s.CWID, g.Course, g.Grade, i.Name
                        from Students s join Grades g on s.CWID=g.StudentCWID
                        join Instructors i on g.InstructorCWID=i.CWID"""
        
        pt: PrettyTable = PrettyTable(field_names=['Student Name', 'Student CWID', 'Course', 'Grade', 'Instructor Name'])
        
        for row in db.execute(query):
            pt.add_row(row)
            
        db.close()
        
        print('Student Grade Summary')
        
        print(pt)
        

def main() -> None:
    
    """ Allow the user to request to enter a _directory pathway and 
    display the information about the files """
    
    univ_files: str = input("Please enter the directory for your University's files:\n")
    try:
        univ: University = University(univ_files)
        
    except ValueError as e:
        print(e)
        
    except FileNotFoundError as e:
        print(e)
    
    except KeyError as e:
        print(e)
        
    else:
        print('Please see results below...\n')
        univ.print_majors_pt()
        univ.print_students_pt()
        univ.print_instructors_pt()
        univ.student_grades_table_db('C:/Users/Class2018/eclipse-workspace/HW09/src/Files/HW11_Zach_George.db')
    
    
if __name__ == "__main__":
    main()
