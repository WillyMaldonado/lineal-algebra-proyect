from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLineEdit, QPushButton, QLabel, QSpinBox, QHBoxLayout, QGridLayout, QFrame, QScrollArea
import numpy as np
from fractions import Fraction

class Determinant(QWidget):
    def __init__(self):
        super().__init__()
        self.generate_determinant()

    def generate_determinant(self):
        self.setWindowTitle('Determinant of a matrix')
        self.resize(800, 600)
        self.generate_window()
        self.show()

    def generate_window(self):
        self.principal = QVBoxLayout()
        self.setLayout(self.principal)

        self.row_label = QLabel('Write the order of the matrix:')
        self.row_input = QSpinBox()
        self.row_input.setRange(1, 10)

        self.generate_button = QPushButton('Create matrix')
        self.generate_button.clicked.connect(self.create_matrices)
        self.clear_button = QPushButton('Clear')
        self.clear_button.clicked.connect(self.clear)

        input_layout = QHBoxLayout()
        input_layout.addWidget(self.row_label)
        input_layout.addWidget(self.row_input)
        input_layout.addWidget(self.generate_button)
        input_layout.addWidget(self.clear_button)

        self.principal.addLayout(input_layout)

        self.result_label = QLabel()
        self.principal.addWidget(self.result_label)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.steps_label = QLabel()
        self.steps_label.setWordWrap(True)
        self.scroll_layout.addWidget(self.steps_label)
        self.scroll_area.setWidget(self.scroll_content)

        self.principal.addWidget(self.scroll_area)

    def create_matrices(self):
        rows = self.row_input.value()
        cols = rows

        self.matrix1 = QGridLayout()
        self.matrix2 = QGridLayout()
        self.result_matrix = QGridLayout()

        self.matrix1_inputs = []

        for i in range(rows):
            row_inputs1 = []
            for j in range(cols):
                input1 = QLineEdit('0')
                self.matrix1.addWidget(input1, i, j)
                row_inputs1.append(input1)
            self.matrix1_inputs.append(row_inputs1)

        self.divider = QFrame()
        self.divider.setFrameShape(QFrame.Shape.VLine)
        self.divider.setFrameShadow(QFrame.Shadow.Sunken)

        self.up = QHBoxLayout()
        self.up.addLayout(self.matrix1)
        self.up.addWidget(self.divider)
        self.up.addLayout(self.matrix2)

        self.calculate_button = QPushButton('Calculate determinant')
        self.calculate_button.clicked.connect(self.calculate_determinant)

        self.principal.addLayout(self.up)
        self.principal.addWidget(self.calculate_button)
        self.principal.addLayout(self.result_matrix)

    def calculate_determinant(self):
        rows = self.row_input.value()
        cols = rows

        matrix_values = []
        for i in range(rows):
            row_values = []
            for j in range(cols):
                value_str = self.matrix1_inputs[i][j].text()
                value = Fraction(value_str)
                row_values.append(value)
            matrix_values.append(row_values)

        matrix = np.array(matrix_values)
        original_matrix = matrix.copy()

        steps = []
        step_count = 1  
        steps.append(f"Initial matrix:\n{self.matrix_to_string(matrix)}\n")
        for i in range(rows):
            for j in range(cols):
                if i != j:
                    factor = matrix[j][i] / matrix[i][i]
                    steps.append(f"Step {step_count}: subtract {factor} * row {i+1} from row {j+1}")
                    matrix[j] -= factor * matrix[i]
                    step_count += 1  
                    steps.append(f"Matrix after step {step_count}:\n{self.matrix_to_string(matrix)}\n")
        determinant = np.prod(np.diag(matrix))
        steps.append(f"Step {step_count + 1}: Multiply the diagonal elements to get the determinant")
        steps.append(f"The determinant is: {determinant}")
        step_count += 2  

        steps_text = "\n".join(steps)
        self.steps_label.setText(steps_text)

        self.result_label.setText(f"The determinant is: {determinant}")

    def matrix_to_string(self, matrix):
        matrix_str = ""
        for row in matrix:
            row_str = " | ".join(str(Fraction(element).limit_denominator()) for element in row)
            matrix_str += row_str + "\n"
        return matrix_str

    def clear(self):
        self.close()
        self.new = Determinant()
        self.new.show()
