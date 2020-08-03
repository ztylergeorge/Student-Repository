'''
Created on Aug 3, 2020
Create a simple HTML output using flask 
Get the results from a database query using SQLite
Store those results in a dictionary to be loaded by flask 
Output the results using the base.html template and students_grades template
@author: Zach George
'''

from flask import Flask, render_template 
import sqlite3

app: Flask = Flask(__name__)

@app.route('/student_grades')
def students_grades_summary() -> str:
    
    """ Create a website using flask from our student database """
    
    query: str = """select s.Name, s.CWID, g.Course, g.Grade, i.Name
                        from Students s join Grades g on s.CWID=g.StudentCWID
                        join Instructors i on g.InstructorCWID=i.CWID"""
                        
    db_file: str = 'C:/Users/Class2018/eclipse-workspace/HW09/src/Files/HW11_Zach_George.db' 
    
    student_db: sqlite3.Connection = sqlite3.connect(db_file)
    
    data: Dict[str, str] = \
            [{'student_name': student_name, 'student_cwid': student_cwid, 'course': course, 'grade': grade, 
              'instructor_name': instructor_name} for student_name, student_cwid, course, grade, 
            instructor_name in student_db.execute(query)]
    
    student_db.close()
    
    return render_template('students_grades.html',
                           title="Stevens Repository",
                           table_title="Student, Course, Grade, and Instructor",
                           reports=data) 

app.run(debug=True)