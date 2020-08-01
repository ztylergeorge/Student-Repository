'''
Created on Jul 13, 2020
Tests the classes and functions made in HW09
@author: Zach George
'''

import unittest 
import sqlite3
from typing import List, Any, Tuple
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
        
        student_db: sqlite3.Connection = sqlite3.connect('C:/Users/Class2018/eclipse-workspace/HW09/src/Files/testing.db')
        
        query: str = """select s.Name, s.CWID, g.Course, g.Grade, i.Name
                        from Students s join Grades g on s.CWID=g.StudentCWID
                        join Instructors i on g.InstructorCWID=i.CWID"""
        
        test_university: Universty = University(good_path)
        
        students_info: List[List[Any]] = [['10103', 'Jobs, S', 'SFEN', {'SSW 810': 'A-', 'CS 501': 'B'}],
                                          ['10115', 'Bezos, J', 'SFEN', {'SSW 810': 'A', 'CS 546': 'F'}],
                                          ['10183', 'Musk, E', 'SFEN', {'SSW 555': 'A', 'SSW 810': 'A'}],
                                          ['11714', 'Gates, B', 'CS', {'SSW 810': 'B-', 'CS 546': 'A', 'CS 570': 'A-'}]
                                          ]
        
        instructors_info: List[List[Any]] = [['98764', 'Cohen, R', 'SFEN', {'CS 546': 1}],
                                            ['98763', 'Rowland, J', 'SFEN', {'SSW 810': 4, 'SSW 555': 1}],
                                            ['98762', 'Hawking, S', 'CS', {'CS 501': 1, 'CS 546': 1, 'CS 570': 1}]
                                            ]
        
        students_completed_courses: List[List[str, Set[str]]] = [['10103', {'CS 501', 'SSW 810'}],
                                                                 ['10115', {'SSW 810'}],
                                                                 ['10183', {'SSW 555', 'SSW 810'}],
                                                                 ['11714', {'CS 546', 'CS 570', 'SSW 810'}]
                                                                 ]
        
        students_missing_courses: List[List[str, Set[str]]] = [['10103', {'SSW 540', 'SSW 555'}],
                                                                 ['10115', {'SSW 540', 'SSW 555'}],
                                                                 ['10183', {'SSW 540'}],
                                                                 ['11714', {}]
                                                                 ]
        
        students_missing_electives: List[List[str, Set[str]]] = [['10103', {}],
                                                                 ['10115', {'CS 501', 'CS 546'}],
                                                                 ['10183', {'CS 501', 'CS 546'}],
                                                                 ['11714', {}]
                                                                 ]
        
        students_grade_summary: List[Tuple[str, str, str, str, str]] = [('Jobs, S', '10103', 'SSW 810', 'A-', 'Rowland, J'),
                                                                        ('Jobs, S', '10103', 'CS 501', 'B', 'Hawking, S'),
                                                                        ('Bezos, J', '10115', 'SSW 810', 'A', 'Rowland, J'),
                                                                        ('Bezos, J', '10115', 'CS 546', 'F', 'Hawking, S'),
                                                                        ('Musk, E', '10183', 'SSW 555', 'A', 'Rowland, J'),
                                                                        ('Musk, E', '10183', 'SSW 810', 'A', 'Rowland, J'),
                                                                        ('Gates, B', '11714', 'SSW 810', 'B-', 'Rowland, J'),
                                                                        ('Gates, B', '11714', 'CS 546', 'A', 'Cohen, R'),
                                                                        ('Gates, B', '11714', 'CS 570', 'A-', 'Hawking, S'),
                                                                        ]
                                         
        self.assertEqual([[student._cwid, student._name, student._major._name, student._courses_grades] for student in test_university._students.values()], students_info)
        self.assertEqual([[instructor._cwid, instructor._name, instructor._department, instructor._courses_students] for instructor in test_university._instructors.values()], instructors_info)
        self.assertEqual([[student._cwid, student._completed_courses] for student in test_university._students.values()], students_completed_courses)
        self.assertEqual([[student._cwid, student._remaining_courses] for student in test_university._students.values()], students_missing_courses)
        self.assertEqual([[student._cwid, student._remaining_electives] for student in test_university._students.values()], students_missing_electives)
        self.assertEqual(students_grade_summary, [row for row in student_db.execute(query)])
        
                    
if __name__ == '__main__':
    unittest.main(exit=False, verbosity=2)
