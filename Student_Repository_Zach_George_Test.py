'''
Created on Jul 13, 2020
Tests the classes and functions made in HW09
@author: Zach George
'''

import unittest 
from typing import List, Any
from Student_Repository_Zach_George import University


class UniversityTest(unittest.TestCase):


    def test_university_error_catching(self) -> None:
        
        """ Test the University class at error handling """
        
        fake_path: str ='C:/Users/Class2018/eclipse-workspace/HW09/src/Fake' 
        missing_students_path: str = 'C:/Users/Class2018/eclipse-workspace/HW09/src/Missing Students'
        missing_grades_path: str = 'C:/Users/Class2018/eclipse-workspace/HW09/src/Missing Grades'
        missing_instructors_path: str = 'C:/Users/Class2018/eclipse-workspace/HW09/src/Missing Instructors'
        missing_majors_path: str = 'C:/Users/Class2018/eclipse-workspace/HW09/src/Missing Majors'
        unknown_student_path: str = 'C:/Users/Class2018/eclipse-workspace/HW09/src/Unknown Student'
        unknown_instructor_path: str = 'C:/Users/Class2018/eclipse-workspace/HW09/src/Unknown Instructor'
        unknown_major_path: str = 'C:/Users/Class2018/eclipse-workspace/HW09/src/Unknown Major'
        too_many_fields_path: str = 'C:/Users/Class2018/eclipse-workspace/HW09/src/Too Many Fields'
        
        with self.assertRaises(FileNotFoundError):
            University(fake_path)
        with self.assertRaises(ValueError):
            University(missing_students_path)
        with self.assertRaises(ValueError):
            University(missing_instructors_path)
        with self.assertRaises(ValueError):
            University(missing_grades_path)
        with self.assertRaises(ValueError):
            University(missing_majors_path)
        with self.assertRaises(KeyError):
            University(unknown_student_path)
        with self.assertRaises(KeyError):
            University(unknown_instructor_path)
        with self.assertRaises(KeyError):
            University(unknown_major_path)
        with self.assertRaises(ValueError):
            University(too_many_fields_path)
            
    def test_university_functionality(self) -> None:
        
        """ Test the functionality of the University class and its subclasses and functions """
        
        good_path: str = 'C:/Users/Class2018/eclipse-workspace/HW09/src/Files'
        
        test_university: Universty = University(good_path)
        
        students_info: List[List[Any]] = [[str(10103), 'Baldwin, C', 'SFEN', {'SSW 567': 'A', 'SSW 564': 'A-', 'SSW 687': 'B', 'CS 501': 'B'}],
                                          [str(10115), 'Wyatt, X', 'SFEN', {'SSW 567': 'A', 'SSW 564': 'B+', 'SSW 687': 'A', 'CS 545': 'A'}],
                                          [str(10172), 'Forbes, I', 'SFEN', {'SSW 555': 'A', 'SSW 567': 'A-'}],
                                          [str(10175), 'Erickson, D', 'SFEN', {'SSW 567': 'A', 'SSW 564': 'A', 'SSW 687': 'B-'}],
                                          [str(10183), 'Chapman, O', 'SFEN', {'SSW 689': 'A'}],
                                          [str(11399), 'Cordova, I', 'SYEN', {'SSW 540': 'B'}],
                                          [str(11461), 'Wright, U', 'SYEN', {'SYS 800': 'A', 'SYS 750': 'A-', 'SYS 611': 'A'}],
                                          [str(11658), 'Kelly, P', 'SYEN', {'SSW 540': 'F'}],
                                          [str(11714), 'Morton, A', 'SYEN', {'SYS 611': 'A', 'SYS 645': 'C'}],
                                          [str(11788), 'Fuller, E', 'SYEN', {'SSW 540': 'A'}]
                                          ]
        
        instructors_info: List[List[Any]] = [[str(98765), 'Einstein, A', 'SFEN', {'SSW 567': 4, 'SSW 540': 3}],
                                            [str(98764), 'Feynman, R', 'SFEN', {'SSW 564': 3, 'SSW 687': 3, 'CS 501': 1, 'CS 545': 1}],
                                            [str(98763), 'Newton, I', 'SFEN', {'SSW 555': 1, 'SSW 689': 1}],
                                            [str(98762), 'Hawking, S', 'SYEN', {}],
                                            [str(98761), 'Edison, A', 'SYEN', {}],
                                            [str(98760), 'Darwin, C', 'SYEN', {'SYS 800': 1, 'SYS 750': 1, 'SYS 611': 2, 'SYS 645': 1}]
                                             ]
        
        students_completed_courses: List[List[str, Set[str]]] = [['10103', {'CS 501', 'SSW 564', 'SSW 567', 'SSW 687'}],
                                                                 ['10115', {'CS 545', 'SSW 564', 'SSW 567', 'SSW 687'}],
                                                                 ['10172', {'SSW 555', 'SSW 567'}],
                                                                 ['10175', {'SSW 564', 'SSW 567', 'SSW 687'}],
                                                                 ['10183', {'SSW 689'}],
                                                                 ['11399', {'SSW 540'}],
                                                                 ['11461', {'SYS 611', 'SYS 750', 'SYS 800'}],
                                                                 ['11658', set()],
                                                                 ['11714', {'SYS 611', 'SYS 645'}],
                                                                 ['11788', {'SSW 540'}]
                                                                 ]
        
        students_missing_courses: List[List[str, Set[str]]] = [['10103', {'SSW 555', 'SSW 540'}],
                                                                 ['10115', {'SSW 540', 'SSW 555'}],
                                                                 ['10172', {'SSW 540', 'SSW 564'}],
                                                                 ['10175', {'SSW 540', 'SSW 555'}], 
                                                                 ['10183', {'SSW 540', 'SSW 555', 'SSW 564', 'SSW 567'}],
                                                                 ['11399', {'SYS 612', 'SYS 671', 'SYS 800'}],
                                                                 ['11461', {'SYS 612', 'SYS 671'}],
                                                                 ['11658', {'SYS 612', 'SYS 671', 'SYS 800'}],
                                                                 ['11714', {'SYS 612', 'SYS 671', 'SYS 800'}],
                                                                 ['11788', {'SYS 612', 'SYS 671', 'SYS 800'}]
                                                                 ]
        
        students_missing_electives: List[List[str, Set[str]]] = [['10103', {}],
                                                                 ['10115', {}],
                                                                 ['10172', {'CS 501', 'CS 513', 'CS 545'}],
                                                                 ['10175', {'CS 501', 'CS 513', 'CS 545'}],
                                                                 ['10183', {'CS 501', 'CS 513', 'CS 545'}],
                                                                 ['11399', {}],
                                                                 ['11461', {'SSW 540', 'SSW 565', 'SSW 810'}],
                                                                 ['11658', {'SSW 540', 'SSW 565', 'SSW 810'}],
                                                                 ['11714', {'SSW 540', 'SSW 565', 'SSW 810'}],
                                                                 ['11788', {}]
                                                                 ]
                                         
        self.assertEqual([[student._cwid, student.name, student.major.name, student._courses_grades] for student in test_university._students.values()], students_info)
        self.assertEqual([[instructor._cwid, instructor.name, instructor.department, instructor._courses_students] for instructor in test_university._instructors.values()], instructors_info)
        self.assertEqual([[student._cwid, student._completed_courses] for student in test_university._students.values()], students_completed_courses)
        self.assertEqual([[student._cwid, student._remaining_courses] for student in test_university._students.values()], students_missing_courses)
        self.assertEqual([[student._cwid, student._remaining_electives] for student in test_university._students.values()], students_missing_electives)
        
                    
if __name__ == '__main__':
    unittest.main(exit=False, verbosity=2)
