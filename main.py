from PyQt6.QtWidgets import *
from PyQt6.QtGui import QAction
import sys

class MainWindow(QMainWindow): #this class allows us to add functionalities like a tool bar, status bar, menu bar etc
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Student Management System')
        
        file_menu = self.menuBar().addMenu('&File') #adding '&' before the name of the menu is standard practice
        help_menu = self.menuBar().addMenu('&Help')
        
        add_student = QAction('Add Student', self)
        file_menu.addAction(add_student)
        
        about_action = QAction('About', self) #Adding self in both instances of QAction will connect them to the class
        help_menu.addAction(about_action)
        
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(('ID','Name','Course','Mobile Number')) #  this method expects a tuple  
        self.setCentralWidget(self.table)
        

        
    def load_data(self):
        self.table
        
                
app = QApplication(sys.argv)        
main = MainWindow()
main.show()
sys.exit(app.exec())
    