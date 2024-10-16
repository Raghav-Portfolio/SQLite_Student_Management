from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QVBoxLayout, QLabel, QWidget, QGridLayout, QLineEdit,\
     QPushButton
import sys
from datetime import datetime

class AgeCalculator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Age Calculator')
        grid = QGridLayout()
        
        #Create Widgets 
        self.name_label = QLabel('Name: ')
        self.name_line_edit = QLineEdit()
        
        dob_label = QLabel('Date of Birth MM/DD/YYYY: ')
        self.dob_edit_line = QLineEdit()
        
        calculate_button = QPushButton('Calculate Age')
        calculate_button.clicked.connect(self.calculate_age)
        self.output_label = QLabel('Output:')
        
        grid.addWidget(self.name_label,0,0) #add name label at position 0,0
        grid.addWidget(self.name_line_edit,0,1) 
        grid.addWidget(dob_label,1,0) 
        grid.addWidget(self.dob_edit_line,1,1) 
        grid.addWidget(calculate_button,2,0,1,2) #The last two arguments signify 
        #that the button should cover 1 row and both columns
        grid.addWidget(self.output_label,3,0,1,2) 
        
        self.setLayout(grid)
        # we access the setLayout method of the QWidget to see the windows, without which we won't see any output
        # We have to use the self keyword to access the super class
        
    def calculate_age(self):
        current_year = datetime.now().year
        dob = self.dob_edit_line.text()  #change dob_edit_line from local variable to instance variable
        year_of_birth = datetime.strptime(dob, "%m/%d/%Y").date().year
        age = current_year - year_of_birth
        self.output_label.setText(f'{self.name_line_edit.text()} is {age} years old')
        
app = QApplication(sys.argv)        
age = AgeCalculator()
age.show()
sys.exit(app.exec())