from PyQt6.QtWidgets import (
    QPushButton, QLabel, QVBoxLayout, QHBoxLayout,
    QGridLayout, QWidget, QLineEdit, QSpinBox, QSizePolicy, QFrame, QScrollArea
)
from PyQt6.QtCore import Qt

class Sum(QWidget):
    def __init__(self):
        super().__init__()
        self.generate_sum()

    def generate_sum(self):
        self.setWindowTitle('Adding between matrix')
        self.resize(800, 600)  
        self.generate_window()
        self.show()

    def generate_window(self):
        self.principal = QVBoxLayout()
        self.setLayout(self.principal)

        self.row_label = QLabel('Number of rows:')
        self.row_input = QSpinBox()
        self.row_input.setRange(1, 10) 

        self.col_label = QLabel('Number of columns:')
        self.col_input = QSpinBox()
        self.col_input.setRange(1, 10) 
        self.generate_button = QPushButton('Generate Matrices')
        self.generate_button.clicked.connect(self.create_matrices)
        self.clear_button = QPushButton('Clear')
        self.clear_button.clicked.connect(self.clear)

        input_layout = QHBoxLayout()
        input_layout.addWidget(self.row_label)
        input_layout.addWidget(self.row_input)
        input_layout.addWidget(self.col_label)
        input_layout.addWidget(self.col_input)
        input_layout.addWidget(self.generate_button)
        input_layout.addWidget(self.clear_button)

        self.principal.addLayout(input_layout)

    def create_matrices(self):
        rows = self.row_input.value()
        cols = self.col_input.value()

        self.matrix1 = QGridLayout()
        self.matrix2 = QGridLayout()
        self.result_matrix = QGridLayout()

        self.matrix1_inputs = []
        self.matrix2_inputs = []

        for i in range(rows):
            row_inputs1 = []
            row_inputs2 = []
            for j in range(cols):
                input1 = QLineEdit('0')
                input2 = QLineEdit('0')
                self.matrix1.addWidget(input1, i, j)
                self.matrix2.addWidget(input2, i, j)
                row_inputs1.append(input1)
                row_inputs2.append(input2)
            self.matrix1_inputs.append(row_inputs1)
            self.matrix2_inputs.append(row_inputs2)

        self.divider = QFrame()
        self.divider.setFrameShape(QFrame.Shape.VLine)
        self.divider.setFrameShadow(QFrame.Shadow.Sunken)

        self.up = QHBoxLayout()
        self.up.addLayout(self.matrix1)
        self.up.addWidget(self.divider)
        self.up.addLayout(self.matrix2)

        self.calculate_button = QPushButton('Calculate Sum')
        self.calculate_button.clicked.connect(self.calculate_sum)

        self.principal.addLayout(self.up)
        self.principal.addWidget(self.calculate_button)
        self.principal.addLayout(self.result_matrix)

    def calculate_sum(self):
        rows = self.row_input.value()
        cols = self.col_input.value()

        # Clear previous results
        for i in reversed(range(self.result_matrix.count())):
            self.result_matrix.itemAt(i).widget().setParent(None)

        explanation_layout = QVBoxLayout()
        explanation_label = QLabel("Step-by-Step:")
        explanation_layout.addWidget(explanation_label)
        
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        explanation_widget = QWidget()
        explanation_widget.setLayout(explanation_layout)
        scroll_area.setWidget(explanation_widget)

        for i in range(rows):
            for j in range(cols):
                value1 = int(self.matrix1_inputs[i][j].text())
                value2 = int(self.matrix2_inputs[i][j].text())
                result = value1 + value2

                result_label = QLabel(str(result))
                result_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                result_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
                self.result_matrix.addWidget(result_label, i, j)

                # Add step-by-step explanation
                step_label = QLabel(f"({i}, {j}): {value1} + {value2} = {result}")
                explanation_layout.addWidget(step_label)

        self.principal.addWidget(scroll_area)

    def clear(self):
        self.close()
        self.new = Sum()
        self.new.show()