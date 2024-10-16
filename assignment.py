from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import *
import sys
from datetime import datetime

class SpeedCalculator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Speed Calculator')
        grid = QGridLayout()
        
        #Create Widgets 
        distance_label = QLabel('Distance: ')
        self.distance_input = QLineEdit()
        
        time_label = QLabel('Time: ')
        self.time_input = QLineEdit()
        
        self.unit_combo = QComboBox()
        self.unit_combo.addItems(['Metric(km)', 'Imperial(miles)'])
        
        calculate_button = QPushButton('Calculate Average Speed')
        calculate_button.clicked.connect(self.calculate_age)
        self.output_label = QLabel('Average Speed:')
        
        grid.addWidget(distance_label,0,0) #add name label at position 0,0
        grid.addWidget(self.distance_input,0,1) 
        grid.addWidget(self.unit_combo,0,2) 
        grid.addWidget(time_label, 1,0)
        grid.addWidget(self.time_input,1,1) 
        grid.addWidget(calculate_button,2,1) #The last two arguments signify 
        #that the button should cover 1 row and both columns
        grid.addWidget(self.output_label,3,0,1,2) 
        
        self.setLayout(grid)
        # we access the setLayout method of the QWidget to see the windows, without which we won't see any output
        # We have to use the self keyword to access the super class
        
    def calculate_age(self):
        distance = float(self.distance_input.text())
        time = float(self.time_input.text())
        speed = distance/time

        if self.unit_combo.currentText() == 'Metric(km)':
            speed = round(speed, 2)
            unit = 'km/h'
        if self.unit_combo.currentText() == 'Imperial(miles)':
            speed = round(speed*0.621371, 2)
            unit = 'mph'
        #display the result
        self.output_label.setText(f"Average Speed: {speed} {unit}")
        
        
app = QApplication(sys.argv)        
speed = SpeedCalculator()
speed.show()
sys.exit(app.exec())