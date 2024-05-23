import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QSpinBox, QPushButton, QGridLayout, QLineEdit, QScrollArea


class MatrixInputWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout()

        self.row_input = QSpinBox()
        self.col_input = QSpinBox()

        self.row_input.setMinimum(1)
        self.col_input.setMinimum(1)

        self.layout.addWidget(QLabel("Enter number of rows:"))
        self.layout.addWidget(self.row_input)
        self.layout.addWidget(QLabel("Enter number of columns:"))
        self.layout.addWidget(self.col_input)

        self.generate_button = QPushButton("Generate Matrix")
        self.generate_button.clicked.connect(self.generate_matrix)

        self.layout.addWidget(self.generate_button)

        self.matrix_layout = QGridLayout()
        self.matrix_inputs = []

        self.layout.addWidget(QLabel("Matrix:"))
        self.layout.addLayout(self.matrix_layout)

        self.setLayout(self.layout)

    def generate_matrix(self):
        rows = self.row_input.value()
        cols = self.col_input.value()

        for i in reversed(range(self.matrix_layout.count())):
            self.matrix_layout.itemAt(i).widget().setParent(None)

        self.matrix_inputs.clear()

        for i in range(rows):
            row_inputs = []
            for j in range(cols):
                input_field = QLineEdit('0')
                self.matrix_layout.addWidget(input_field, i, j)
                row_inputs.append(input_field)
            self.matrix_inputs.append(row_inputs)

    def clear(self):
        self.row_input.setValue(1)
        self.col_input.setValue(1)
        self.generate_matrix()


class Rank(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Rank of a matrix")
        self.layout = QVBoxLayout()

        self.matrix_input_widget = MatrixInputWidget()

        self.calculate_button = QPushButton("Calculate Rank")
        self.calculate_button.clicked.connect(self.calculate_rank)

        self.clear_button = QPushButton("Clear")
        self.clear_button.clicked.connect(self.clear)

        self.result_label = QLabel()

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.result_label)

        self.layout.addWidget(QLabel("Enter matrix size and elements:"))
        self.layout.addWidget(self.matrix_input_widget)
        self.layout.addWidget(self.calculate_button)
        self.layout.addWidget(self.clear_button)
        self.layout.addWidget(QLabel("Result:"))
        self.layout.addWidget(self.scroll_area)

        self.setLayout(self.layout)

        self.resize(800, 600)

    def calculate_rank(self):
        matrix_inputs = self.matrix_input_widget.matrix_inputs
        matrix = [[float(input_field.text()) for input_field in row] for row in matrix_inputs]

        rank = self.gaussian_elimination(matrix)

        explanation = (
            "To calculate the rank of a matrix, we first apply the Gaussian elimination method. "
            "This method involves performing row operations to reduce the matrix to a row-echelon form, "
            "where each non-zero row begins with more leading zeros than the previous row.\n\n"
        )

        explanation += "Gaussian elimination process:\n\n"
        for step in range(rank):
            explanation += f"Step {step + 1}:\n"
            explanation += "  Multiply the top row by a factor to make the diagonal element equal to 1.\n"
            explanation += "  Subtract multiples of the top row from the rows below to make the elements below the diagonal equal to 0.\n\n"

        result_text = f"{explanation}\n"
        result_text += f"The entered matrix is:\n"
        for row in matrix:
            result_text += "  ".join(map(str, row)) + "\n"
        result_text += f"\nThe rank of the matrix is: {rank}"
        self.result_label.setText(result_text)

    def gaussian_elimination(self, matrix):
        rows = len(matrix)
        cols = len(matrix[0]) if matrix else 0
        rank = min(rows, cols)

        for row in range(rank):
            if matrix[row][row] != 0:
                for col in range(row + 1, rows):
                    ratio = matrix[col][row] / matrix[row][row]
                    for i in range(rank):
                        matrix[col][i] -= ratio * matrix[row][i]
            else:
                reduce = True
                for i in range(row + 1, rows):
                    if matrix[i][row] != 0:
                        matrix[row], matrix[i] = matrix[i], matrix[row]
                        reduce = False
                        break
                if reduce:
                    rank -= 1
                    for i in range(rows):
                        matrix[i][row] = matrix[i][rank]

        return rank

    def clear(self):
        self.close()
        self.new = Rank()
        self.new.show()

