from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLineEdit, QPushButton, QLabel, QSpinBox, QHBoxLayout, QGridLayout, QFrame, QScrollArea
import numpy as np
from fractions import Fraction

class Inverse(QWidget):
    def __init__(self):
        super().__init__()
        self.generate_determinant()

    def generate_determinant(self):
        self.setWindowTitle('Inverse of a matrix')
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
        self.result_label.setWordWrap(True)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_area.setWidget(self.scroll_content)
        self.scroll_layout.addWidget(self.result_label)
        
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

        self.calculate_button = QPushButton('Calculate inverse')
        self.calculate_button.clicked.connect(self.calculate_inverse)

        self.principal.addLayout(self.up)
        self.principal.addWidget(self.calculate_button)
        self.principal.addLayout(self.result_matrix)

    def calculate_inverse(self):
        rows = self.row_input.value()
        cols = rows

        matrix_values = []
        for i in range(rows):
            row_values = []
            for j in range(cols):
                value = float(Fraction(self.matrix1_inputs[i][j].text()))
                row_values.append(value)
            matrix_values.append(row_values)

        matrix = np.array(matrix_values)
        identity = np.identity(rows)

        try:
            steps_text = "Steps to calculate the inverse matrix:\n\n"
            step_count = 1

            for i in range(rows):
                pivot = matrix[i][i]
                matrix[i] /= pivot
                identity[i] /= pivot

                steps_text += f"Step {step_count}: Make pivot of row {i+1} equal to 1 (Divide row {i+1} by {pivot})\n"
                steps_text += self.format_matrices_side_by_side(matrix, identity) + "\n\n"
                step_count += 1

                for j in range(i + 1, rows):
                    factor = matrix[j][i]
                    matrix[j] -= factor * matrix[i]
                    identity[j] -= factor * identity[i]

                    steps_text += f"Step {step_count}: Make elements below pivot in column {i+1} equal to 0 (Subtract {factor} * row {i+1} from row {j+1})\n"
                    steps_text += self.format_matrices_side_by_side(matrix, identity) + "\n\n"
                    step_count += 1

            for i in range(rows - 1, -1, -1):
                for j in range(i - 1, -1, -1):
                    factor = matrix[j][i]
                    matrix[j] -= factor * matrix[i]
                    identity[j] -= factor * identity[i]

                    steps_text += f"Step {step_count}: Make elements above pivot in column {i+1} equal to 0 (Subtract {factor} * row {i+1} from row {j+1})\n"
                    steps_text += self.format_matrices_side_by_side(matrix, identity) + "\n\n"
                    step_count += 1

            inverse_matrix = identity

            steps_text += "The inverse matrix is obtained in the identity matrix:\n"
            steps_text += self.matrix_to_string(inverse_matrix)

            self.result_label.setText(steps_text)

        except np.linalg.LinAlgError:
            self.result_label.setText("An error occurred while calculating the inverse matrix.")

    def matrix_to_string(self, matrix):
        matrix_str = ""
        for row in matrix:
            row_str = " ".join(str(Fraction(x).limit_denominator()) for x in row)
            matrix_str += row_str + "\n"
        return matrix_str

    def format_matrices_side_by_side(self, matrix1, matrix2):
        matrix_str = ""
        for row1, row2 in zip(matrix1, matrix2):
            row1_str = " ".join(str(Fraction(x).limit_denominator()) for x in row1)
            row2_str = " ".join(str(Fraction(x).limit_denominator()) for x in row2)
            matrix_str += f"{row1_str} | {row2_str}\n"
        return matrix_str

    def clear(self):
        self.close()
        self.new = Inverse()
        self.new.show()
