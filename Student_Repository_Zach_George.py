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
@author: Zachary George
'''
from collections import defaultdict
from typing import Dict, Iterator, List, Tuple, DefaultDict
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
                    
                    
class Student:
    
    
    """ Defines the attributes and methods of the Student class """
    
    def __init__(self, cwid: str, name: str, major: str) -> None:
        
        """ Define the attributes of a Student object """
        
        self._cwid: str = cwid
        self.name: str = name
        self.major: str = major
        self._courses_grades: Dict[str, str] = dict() #key: course name value: grade earned
        
        
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
        
        self._students: Dict[str, Student] = self._students_information() #key: cwid value: Student
        self._instructors: Dict[str, Instructor] = self._instructors_information() #key: cwid value: Instructor
        
        self.__process_grades()
    
    def _students_information(self) -> Dict[str, Student]:
        
        """ Read information about the students """
        
        students: Dict[str, Student] = dict() #key: cwid value: Student object
        
        if 'students.txt' in self._directory:
            
            for cwid, name, major in _file_reader('students.txt', fields=3, sep='\t', header=False):
                students[cwid] = Student(cwid, name, major)
                
        else:
            raise ValueError('The students file does not exist. Please try again.')
                      
        return students
    
    def _instructors_information(self) -> Dict[str, Instructor]:
        
        """ Read information about the instructors """
        
        instructors: Dict[str, Instructor] = dict() #key: cwid value: Instructor object
        
        if 'instructors.txt' in self._directory:
            
            for cwid, name, department in _file_reader('instructors.txt', fields=3, sep='\t', header=False):
                instructors[cwid] = Instructor(cwid, name, department)

        else:
            raise ValueError('The instructors file does not exist. Please try again.')
                         
        return instructors
            
    def __process_grades(self) -> None:
        
        """ Process the grades for each students """     
        
        if 'grades.txt' in self._directory:
                
            for grade in _file_reader('grades.txt', fields=4, sep='\t', header=False):
                
                if grade[0] not in self._students:
                    raise ValueError(f'An unidentified student was found: {grade[0]}')
                
                else:
                    self._students[grade[0]]._courses_grades[grade[1]] = grade[2]
                            
                if grade[3] not in self._instructors:
                    raise ValueError(f'An unidentified instructor was found: {grade[3]}')
                
                else:
                    self._instructors[grade[3]]._courses_students[grade[1]] += 1                                           
        else:
            raise ValueError('The grades file does not exist. Please try again.')
                          
    def print_students_pt(self) -> None:
        
        """ Print a prettytable of a student based on a CWID """
        
        print('Student Summary')
        pt: PrettyTable = PrettyTable(field_names=['CWID', 'Name', 'Completed Courses'])
        
        for student in self._students.values():
            pt.add_row([student.cwid, student.name, sorted(list(student._courses_grades))])
        print(pt)
                
                
    def print_instructors_pt(self) -> None:
        
        """ Print a prettytable of an instructor based on a CWID """
        
        print('Instructor Summary')
        pt: PrettyTable = PrettyTable(field_names=['CWID', 'Name', 
                                                   'Dept', 'Course', 'Students'])
        
        for instructor in self._instructors.values():
            for i in range(len(instructor.courses_students)):
                pt.add_row([instructor.cwid, instructor.name, instructor.department, 
                            list(instructor.courses_students)[i], 
                            list(instructor.courses_students.values())[i]])
        print(pt)


def main() -> None:
    
    """ Allow the user to request to enter a _directory pathway and 
    display the information about the files """
    
    univ_files: str = input("Please enter the _directory for your University's files:\n")
    try:
        univ: University = University(univ_files)
    except ValueError as e:
        print(e)
    except FileNotFoundError as e:
        print(e)
    else:
        print('Please see results below...\n')
        univ.print_students_pt()
        univ.print_instructors_pt()
    
if __name__ == "__main__":
    main()
