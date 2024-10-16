from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QAction
import sys
import sqlite3

from PyQt6.QtWidgets import QWidget

class MainWindow(QMainWindow): #this class allows us to add functionalities like a tool bar, status bar, menu bar etc
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Student Management System')
        
        file_menu = self.menuBar().addMenu('&File') #adding '&' before the name of the menu is standard practice
        help_menu = self.menuBar().addMenu('&Help')
        
        
        add_student = QAction('Add Student', self)
        add_student.triggered.connect(self.insert)
        file_menu.addAction(add_student)
        
        about_action = QAction('About', self) #Adding self in both instances of QAction will connect them to the class
        help_menu.addAction(about_action)
        
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(('ID','Name','Course','Mobile Number')) #  this method expects a tuple  
        self.table.verticalHeader().setVisible(False)
        self.setCentralWidget(self.table)
        

    def insert(self):
        dialog = InsertDialog()
        dialog.exec()
        
    def load_data(self):
        """ Interact with the SQL Table """
        connection = sqlite3.connect('database.db')
        result = connection.execute("SELECT * FROM students")
        self.table.setRowCount(0)
        #populate the table with the data now
        for row_number, row_data in enumerate(result):
            self.table.insertRow(row_number)
            for columm_number, data in enumerate(row_data):
                self.table.setItem(row_number, columm_number,QTableWidgetItem(str(data)))
        connection.close()
        
class InsertDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Insert Student Data')
        self.setFixedHeight(300)
        self.setFixedWidth(300)
        
        layout = QVBoxLayout()
        
        #Add Student Name Widget
        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText('Name')
        layout.addWidget(self.student_name)
        
        #Add Courses Dropdown Menu
        self.course_name = QComboBox()
        courses = ['Biology','Math','Astronomy', 'Physics']
        self.course_name.addItems(courses)
        layout.addWidget(self.course_name)
        
        #Add mobile no. widget
        self.number = QLineEdit()
        self.number.setPlaceholderText('Phone Number')
        layout.addWidget(self.number)
        
        #Add submit button
        submit = QPushButton("Submit")
        submit.clicked.connect(self.add_student)
        layout.addWidget(submit)
        
        self.setLayout(layout)
    
    def add_student(self):
        name = self.student_name.text()
        course = self.course_name.itemText(self.course_name.currentIndex()) #itemText as it is a combobox
        mobile = self.number.text()
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        cursor.execute ("INSERT INTO students (name, course, mobile) VALUES (?,?,?)",
                        (name, course, mobile)
                        )   
        connection.commit()
        cursor.close()
        connection.close()
        main.load_data() # to show changes in the table in real time
        
app = QApplication(sys.argv)        
main = MainWindow()
main.show()
main.load_data()
sys.exit(app.exec())
    