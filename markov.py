import numpy as np
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit

from Utils.PrinterManager import PrinterManager as Printer
from Utils.Matrix import Matrix, MatrixManager

class MatrixApp(QWidget):
    def __init__(self):
        super().__init__()
        self.generate_window()
    def generate_window(self):
        self.setWindowTitle('Matrix Steps Application')
        self.setGeometry(100, 100, 800, 600)
        self.generate_UI()
        self.show()
        
    def generate_UI(self):

        
        layout = QVBoxLayout()
        
        self.steps_label = QLabel('Number of Steps:', self)
        layout.addWidget(self.steps_label)
        
        self.steps_input = QLineEdit(self)
        self.steps_input.setText('0')
        layout.addWidget(self.steps_input)

        self.matrix_label = QLabel('Origin Matrix (comma-separated values per row, semicolon-separated rows):', self)
        layout.addWidget(self.matrix_label)
        
        self.matrix_input = QLineEdit(self)
        self.matrix_input.setText('0,0,0;0,0,0;0,0,0')
        layout.addWidget(self.matrix_input)
        
        self.init_percent_label = QLabel('Initial Percentages (comma-separated values):', self)
        layout.addWidget(self.init_percent_label)
        
        self.init_percent_input = QLineEdit(self)
        self.init_percent_input.setText('0,0,0')
        layout.addWidget(self.init_percent_input)
        
        self.run_button = QPushButton('Run', self)
        self.run_button.clicked.connect(self.run_matrix_calculation)
        layout.addWidget(self.run_button)
        
        self.output_text = QTextEdit(self)
        layout.addWidget(self.output_text)
        
        self.setLayout(layout)
        
    def run_matrix_calculation(self):
        self.output_text.clear()
        
        try:
            steps = int(self.steps_input.text())
            origin_matrix_str = self.matrix_input.text()
            init_percent_str = self.init_percent_input.text()

            origin_matrix = np.array([[float(num) for num in row.split(',')] for row in origin_matrix_str.split(';')])
            initial_percentages = np.array([[float(num)] for num in init_percent_str.split(',')])

            custom_matrix = Matrix('A', origin_matrix)
            custom_keys = Matrix('B', initial_percentages)
        except ValueError:
            self.output_text.append("Invalid input. Please enter numeric values correctly.")
            return

        custom_matrix = custom_matrix.transpose()
        
        self.output_text.append("Transposed Matrix:")
        self.output_text.append(str(custom_matrix.matrix))
        
        for i in range(steps):
            custom_keys = MatrixManager.matrix_multiply(custom_matrix, custom_keys)
            custom_keys.name = f"iter {i + 1}"
            self.output_text.append(f"\nResult after iteration {i + 1}:")
            self.output_text.append(str(custom_keys.matrix))
