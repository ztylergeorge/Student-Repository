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
        
        self.name: str = name
        self.required_courses: Set[str] = set()
        self.required_electives: Set[str] = set()
    
    def _remaining_courses(self, courses: Dict[str, str]) -> Set[str]:
        
        """ Determine the remaining courses of a student based off of their major """
        
        passed_courses: Set[str] = set([key for key in courses if courses[key] in 
                                        ['A', 'A-', 'B+', 'B', 'B-', 'C+', 'C']])
        
        return self.required_courses.difference(passed_courses)
    
    def _remaining_electives(self, courses: Dict[str, str]) -> Set[str]: 
        
        """ Determine the remaining electives of a student based off of their major """
        
        passed_courses: Set[str] = set([key for key in courses if courses[key] in 
                                        ['A', 'A-' 'B+', 'B', 'B-', 'C+', 'C']])
        
        if len(passed_courses.intersection(self.required_electives)) > 0:
            return {}
          
        else:
            return set(self.required_electives)
        
    def _summary_pretty_table(self) -> PrettyTable:
        
        """ Print a pretty table for the student's courses and grades """
        
        pt: PrettyTable = PrettyTable(field_names= ['Course', 'R/E?'])
        
        for course in self.required_courses:
            pt.add_row([course, 'R'])
        
        for elective in self.required_electives:
            pt.add_row([elective, 'E'])
            
        return pt
             
                    
class Student:
    
    
    """ Defines the attributes and methods of the Student class """
    
    def __init__(self, cwid: str, name: str) -> None:
        
        """ Define the attributes of a Student object """
        
        self._cwid: str = cwid
        self.name: str = name
        self._courses_grades: Dict[str, str] = dict() #key: course name value: grade earned
        self._required_courses: Set[str] = set()
        self._required_electives: Set[str] = set()
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
            
    def _summary_pretty_table(self) -> PrettyTable:
        
        """ Print a pretty table for the student's courses and grades """
        
        pt: PrettyTable = PrettyTable(field_names= ['Course', 'Grade'])
        
        for course, grade in self.courses_grades.items():
            pt.add_row([course, grade])
            
        return pt
    
    
class Instructor:
    
    
    """ Defines the attributes and methods of the Instructor class """
    
    
    def __init__(self, cwid: str, name: str, department: str) -> None:
        
        """ Define the attributes of an Instructor object """
        
        self._cwid: str = cwid
        self.name: str = name
        self.department: str = department
        self._courses_students: DefaultDict[str, int] = defaultdict(int) #key: course name value: number of students in course
        
    def _summary_pretty_table(self) -> PrettyTable:
        
        """ Print a pretty table for an instructors and their 
        courses with number of students """
        
        pt: PrettyTable = PrettyTable(field_names= ['Course', 'Number of Students'])
        
        for course, students in self.courses_students.items():
            pt.add_row([course, students])
            
        return pt
    
                  
class University:
    
    
    """ Defines the attributes and methods of the University class """
    
    def __init__(self, _directory: str) -> None:
        
        """ Defines the attributes of a University object """
        
        if type(_directory) is not str:
            raise TypeError(f'{_directory} is not a string. Please try again.')
        
        try:
            os.chdir(_directory)
            self._directory: List[str] = os.listdir(_directory)
            
        except FileNotFoundError as e:
            raise FileNotFoundError(f'{_directory} could not be opened.') from e
        
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
                
                if require == 'R':
                    majors[major].required_courses.add(course)
                    
                if require == 'E':
                    majors[major].required_electives.add(course)
        else:
            raise ValueError('The majors file does not exist. Please try again.')
                
        return majors
                    
    def _students_information(self) -> Dict[str, Student]:
        
        """ Read information about the students """
        
        students: Dict[str, Student] = dict() #key: cwid value: Student object
        
        if 'students.txt' in self._directory:
            
            for cwid, name, major in _file_reader('students.txt', fields=3, sep=';', header=True):
                students[cwid] = Student(cwid, name)
                
                if major in self._majors:
                    students[cwid].major = self._majors[major]
                else:
                    raise KeyError(f'An unexpected major was found: {major}')
                
        else:
            raise ValueError('The students file does not exist. Please try again.')
                    
        return students
    
    def _instructors_information(self) -> Dict[str, Instructor]:
        
        """ Read information about the instructors """
        
        instructors: Dict[str, Instructor] = dict() #key: cwid value: Instructor object
        
        if 'instructors.txt' in self._directory:
            
            for cwid, name, department in _file_reader('instructors.txt', fields=3, sep='|', header=True):
                instructors[cwid] = Instructor(cwid, name, department)

        else:
            raise ValueError('The instructors file does not exist. Please try again.')
                         
        return instructors
                      
    def __process_grades(self) -> None:
        
        """ Process the grades for each students """
                 
        if 'grades.txt' in self._directory:
                
            for student_cwid, course, grade, instructor_cwid  in _file_reader('grades.txt', fields=4, sep='|', header=True):
                
                if student_cwid not in self._students:
                    raise KeyError(f'An unidentified student was found: {student_cwid}')
                
                else:
                    self._students[student_cwid]._courses_grades[course] = grade
                            
                if instructor_cwid not in self._instructors:
                    raise KeyError(f'An unidentified instructor was found: {instructor_cwid}')
                
                else:
                    self._instructors[instructor_cwid]._courses_students[course] += 1
                
            for student in self._students.values():
                
                student._completed_courses = set([key for key in student._courses_grades if student._courses_grades[key] in 
                                                  ['A', 'A-', 'B+', 'B', 'B-', 'C+', 'C']])
                student._remaining_courses = student.major._remaining_courses(student._courses_grades)
                student._remaining_electives = student.major._remaining_electives(student._courses_grades)       
                                                         
        else:
            raise ValueError('The grades file does not exist. Please try again.')
                  
    def print_students_pt(self) -> None:
        
        """ Print a prettytable of students """
        
        print('Student Summary')
        pt: PrettyTable = PrettyTable(field_names=['CWID', 'Name', 'Major', 'Completed Courses', 'Remaining Required', 
                                                   'Remaining Electives', 'GPA'])
        
        for student in self._students.values():
            pt.add_row([student._cwid, student.name, student.major.name, sorted(list(student._completed_courses)), 
                        student._remaining_courses, student._remaining_electives, student._calculate_gpa()])
            
        print(pt)   
                
    def print_instructors_pt(self) -> None:
        
        """ Print a prettytable of instructors """
        
        print('Instructor Summary')
        pt: PrettyTable = PrettyTable(field_names=['CWID', 'Name', 
                                                   'Dept', 'Course', 'Students'])
        
        for instructor in self._instructors.values():
            for i in range(len(instructor._courses_students)):
                pt.add_row([instructor._cwid, instructor.name, instructor.department, 
                            list(instructor._courses_students)[i], 
                            list(instructor._courses_students.values())[i]])
        print(pt)
    
    def print_majors_pt(self) -> None:
        
        """ Print a pretty table of majors """
        
        print('Majors Summary')
        pt: PrettyTable = PrettyTable(field_names=['Major', 'Required Courses', 'Required Electives'])
        
        for major in self._majors.values():
            pt.add_row([major.name, major.required_courses, major.required_electives])
        
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
    
    
if __name__ == "__main__":
    main()
