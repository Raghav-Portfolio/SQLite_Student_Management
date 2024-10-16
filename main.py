from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QAction, QIcon
import sys
import sqlite3

from PyQt6.QtWidgets import QWidget

class MainWindow(QMainWindow): #this class allows us to add functionalities like a tool bar, status bar, menu bar etc
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Student Management System')
        self.setMinimumSize(800,600)
        
        file_menu = self.menuBar().addMenu('&File') #adding '&' before the name of the menu is standard practice
        help_menu = self.menuBar().addMenu('&Help')
        edit_menu = self.menuBar().addMenu('&Edit')
        
        add_student = QAction(QIcon("icons/icons/add.png"),'Add Student', self)
        add_student.triggered.connect(self.insert)
        file_menu.addAction(add_student)
        
        about_action = QAction('About', self) #Adding self in both instances of QAction will connect them to the class
        help_menu.addAction(about_action)
        
        search_action = QAction(QIcon('icons/icons/search.png'),'Search', self)
        search_action.triggered.connect(self.popup)
        edit_menu.addAction(search_action)
        
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(('ID','Name','Course','Mobile')) #  this method expects a tuple  
        self.table.verticalHeader().setVisible(False)
        self.setCentralWidget(self.table)
        
        #Create and add Toolbar
        toolbar = QToolBar()
        toolbar.setMovable(True)
        self.addToolBar(toolbar)
        toolbar.addAction(add_student)
        toolbar.addAction(search_action)
        
        #Create and add Status Bar
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)
        
        #Detect a cell being clicked on
        self.table.cellClicked.connect(self.cell_clicked)

    def cell_clicked(self):
        edit_button = QPushButton('Edit Record')
        edit_button.clicked.connect(self.edit)
        
        delete_button = QPushButton('Delete Record')
        delete_button.clicked.connect(self.delete)
        
        #remove any buttons that have been previously added
        children = self.findChildren(QPushButton)
        if children:
            for child in children:
                self.statusbar.removeWidget(child)            
        
        self.statusbar.addWidget(edit_button)
        self.statusbar.addWidget(delete_button)
        
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
        
    def insert(self):
        dialog = InsertDialog()
        dialog.exec()
        
    def popup(self):
        window = SearchPopup()
        window.exec()
        
    def edit(self):
        dialog = EditDialog()
        dialog.exec()
        
    def delete(self):
        dialog = DeleteDialog()
        dialog.exec()
        
        
class DeleteDialog(QDialog):
    # def __init(self):
    #     super().__init__()
    #     self.setWindowTitle('Edit')
    pass
    
class EditDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Update Student Data')
        self.setFixedHeight(300)
        self.setFixedWidth(300)
        
        layout = QVBoxLayout()
        
       
        
        #Get Student Name from Selected Row
        index = main.table.currentRow() #returns the index of the selected row
        student_name = main.table.item(index, 1).text()
        
        #Get ID from selected row
        self.student_id = main.table.item(index, 0).text()
        
        #Add Student Name Widget
        self.student_name = QLineEdit(student_name)
        self.student_name.setPlaceholderText('Name')
        layout.addWidget(self.student_name)
        
        #Add Courses Dropdown Menu
        course_name = main.table.item(index, 2).text()
        self.course_name = QComboBox()
        courses = ['Biology','Math','Astronomy', 'Physics']
        self.course_name.addItems(courses)
        self.course_name.setCurrentText(course_name)
        layout.addWidget(self.course_name)
        
        #Add mobile no. widget
        default_number = main.table.item(index, 3).text()
        self.number = QLineEdit(default_number)
        self.number.setPlaceholderText('Phone Number')
        layout.addWidget(self.number)
        
        #Add submit button
        submit = QPushButton("Submit")
        submit.clicked.connect(self.update_student)
        layout.addWidget(submit)
        
        self.setLayout(layout)
    
    def update_student(self):
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        cursor.execute('UPDATE students SET name = ?, course = ?, mobile = ? WHERE id =?', 
                       (self.student_name.text(), 
                        self.course_name.itemText(self.course_name.currentIndex()), #ComboBox needs itemText 
                        self.number.text(),
                        self.student_id)
                       )
        connection.commit()
        cursor.close()
        connection.close()
        #Refresh the table
        main.load_data()
            
class SearchPopup(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Insert Student Data')
        self.setFixedHeight(300)
        self.setFixedWidth(300)
        
        layout = QVBoxLayout() 
        
        self.searchbar = QLineEdit()
        self.searchbar.setPlaceholderText('Type Item To Search')
        layout.addWidget(self.searchbar)
        
        search = QPushButton("Search")
        search.clicked.connect(self.search_item)
        layout.addWidget(search)
        
        self.setLayout(layout)
    
    def search_item(self):
        name = self.searchbar.text()
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()
        result = cursor.execute('SELECT * FROM students WHERE name = ?', (name,))
        rows = list(result)
        print(rows)
        items = main.table.findItems(name, Qt.MatchFlag.MatchFixedString)
        for item in items:
            print(item)
            main.table.item(item.row(), 1).setSelected(True)
        cursor.close()
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
    