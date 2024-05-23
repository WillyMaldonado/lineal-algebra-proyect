from PyQt6.QtWidgets import (
    QApplication, QPushButton, QLabel, QVBoxLayout, QHBoxLayout,
    QGridLayout, QWidget, QLineEdit, QSpinBox, QSizePolicy, QFrame, QScrollArea,
    QMessageBox
)
from PyQt6.QtCore import Qt

class Multiply(QWidget):
    def __init__(self):
        super().__init__()
        self.generate_inverse()

    def generate_inverse(self):
        self.setWindowTitle("Multiply matrix")
        self.resize(700, 500)
        self.generate_window()
        self.show()

    def generate_window(self):
        self.principal = QVBoxLayout()
        self.setLayout(self.principal)

        self.input_rows1 = QSpinBox()
        self.label_rows1 = QLabel("Select the number of rows of the first matrix")
        self.input_rows1.setRange(1, 10)

        self.input_cols1 = QSpinBox()
        self.label_cols1 = QLabel("Select the numbers of columns of the first matrix")
        self.input_cols1.setRange(1, 10)

        self.input_rows2 = QSpinBox()
        self.label_rows2 = QLabel("Select the numbers of rows of the second matrix")
        self.input_rows2.setRange(1, 10)

        self.input_cols2 = QSpinBox()
        self.label_cols2 = QLabel("Select the numbers of cols of the second matrix")
        self.input_cols2.setRange(1, 10)

        self.create_button = QPushButton('Generate matrix')
        self.create_button.clicked.connect(self.create_matrix)

        self.clear_button = QPushButton("Clear")
        self.clear_button.clicked.connect(self.clear)

        input_layout1 = QHBoxLayout()
        input_layout2 = QHBoxLayout()
        buttons_layout = QHBoxLayout()
        input_layout1.addWidget(self.label_rows1)
        input_layout1.addWidget(self.input_rows1)
        input_layout1.addWidget(self.label_cols1)
        input_layout1.addWidget(self.input_cols1)
        input_layout2.addWidget(self.label_rows2)
        input_layout2.addWidget(self.input_rows2)
        input_layout2.addWidget(self.label_cols2)
        input_layout2.addWidget(self.input_cols2)

        buttons_layout.addWidget(self.create_button)
        buttons_layout.addWidget(self.clear_button)

        self.principal.addLayout(input_layout1)
        self.principal.addLayout(input_layout2)
        self.principal.addLayout(buttons_layout)

    def create_matrix(self):
        rows1 = self.input_rows1.value()
        cols1 = self.input_cols1.value()
        rows2 = self.input_rows2.value()
        cols2 = self.input_cols2.value()

        if cols1 == rows2:
            self.matrix_input_layout = QHBoxLayout()
            self.matrix1 = QGridLayout()
            self.matrix2 = QGridLayout()
            self.matrix1_inputs = []
            self.matrix2_inputs = []

            for i in range(rows1):
                rows_inputs1 = []
                for j in range(cols1):
                    input1 = QLineEdit('0')
                    self.matrix1.addWidget(input1, i, j)
                    rows_inputs1.append(input1)
                self.matrix1_inputs.append(rows_inputs1)

            for i in range(rows2):
                rows_inputs2 = []
                for j in range(cols2):
                    input2 = QLineEdit('0')
                    self.matrix2.addWidget(input2, i, j)
                    rows_inputs2.append(input2)
                self.matrix2_inputs.append(rows_inputs2)

            self.divider = QFrame()
            self.divider.setFrameShape(QFrame.Shape.VLine)
            self.divider.setFrameShadow(QFrame.Shadow.Sunken)

            self.calculate_button = QPushButton("Calculate the product of the matrix")
            self.calculate_button.clicked.connect(self.calculate_product)

            self.matrix_input_layout.addLayout(self.matrix1)
            self.matrix_input_layout.addWidget(self.divider)
            self.matrix_input_layout.addLayout(self.matrix2)

            self.principal.addLayout(self.matrix_input_layout)
            self.principal.addWidget(self.calculate_button)
        else:
            QMessageBox.warning(self, "Size error", "The number of columns does not match with the number of rows\n",
                                QMessageBox.StandardButton.Close, QMessageBox.StandardButton.Close)

    def calculate_product(self):
        rows1 = self.input_rows1.value()
        cols1 = self.input_cols1.value()
        rows2 = self.input_rows2.value()
        cols2 = self.input_cols2.value()

        try:
            matrix1 = [[int(self.matrix1_inputs[i][j].text()) for j in range(cols1)] for i in range(rows1)]
            matrix2 = [[int(self.matrix2_inputs[i][j].text()) for j in range(cols2)] for i in range(rows2)]
            result_matrix = [[0] * cols2 for _ in range(rows1)]

            calculation_layout = QVBoxLayout()

            for i in range(rows1):
                for j in range(cols2):
                    calculation_text = QLabel(f"Result[{i}][{j}] = ")

                    calculation_result = 0
                    calculation_steps = []
                    for k in range(cols1):
                        step = f"({matrix1[i][k]} * {matrix2[k][j]})"
                        calculation_steps.append(step)
                        calculation_result += matrix1[i][k] * matrix2[k][j]

                    calculation_text.setText(f"Result[{i}][{j}] = {' + '.join(calculation_steps)} = {calculation_result}")
                    calculation_layout.addWidget(calculation_text)

                    result_matrix[i][j] = calculation_result

            result_label = QLabel("Result Matrix:")
            self.principal.addWidget(result_label)

            for i in range(rows1):
                row_layout = QHBoxLayout()
                for j in range(cols2):
                    result_label = QLabel(str(result_matrix[i][j]))
                    row_layout.addWidget(result_label)
                self.principal.addLayout(row_layout)

            self.principal.addLayout(calculation_layout)

        except ValueError:
            QMessageBox.warning(self, "Input error", "All matrix elements must be integers and cannot be empty.",
                                QMessageBox.StandardButton.Close, QMessageBox.StandardButton.Close)


    def clear(self):
        self.close()
        self.new = Multiply()
        self.new.show()