from PyQt6.QtWidgets import (
    QPushButton, QLabel, QVBoxLayout, QHBoxLayout,
    QGridLayout, QWidget, QLineEdit, QSpinBox, QSizePolicy, QFrame, QScrollArea,
    QMessageBox
)

class Multiply(QWidget):
    def __init__(self):
        super().__init__()
        self.generate_inverse()

    def generate_inverse(self):
        self.setWindowTitle("Multiply matrix")
        self.resize(1920,1080)
        self.generate_window()
        self.show()

    def generate_window(self):
        self.principal = QVBoxLayout()
        self.setLayout(self.principal)

        self.input_rows1 = QSpinBox()
        self.label_rows1 = QLabel("Select the number of rows of the first matrix")
        self.input_rows1.setRange(1,10)

        self.input_cols1 = QSpinBox()
        self.label_cols1 = QLabel("Select the numbers of columns of the first matrix")
        self.input_cols1.setRange(1,10)

        self.input_rows2 = QSpinBox()
        self.label_rows2 = QLabel("Select the numbers of rows of the second matrix")
        self.input_rows2.setRange(1,10)

        self.input_cols2 = QSpinBox()
        self.label_cols2 = QLabel("Select the numbers of cols of the second matrix")
        self.input_cols2.setRange(1,10)

        self.create_button = QPushButton('Generate matrix')
        self.create_button.clicked.connect(self.create_matrix)

        input_layout = QHBoxLayout()
        input_layout.addWidget(self.label_rows1)
        input_layout.addWidget(self.input_rows1)
        input_layout.addWidget(self.label_cols1)
        input_layout.addWidget(self.input_cols1)
        input_layout.addWidget(self.label_rows2)
        input_layout.addWidget(self.input_rows2)
        input_layout.addWidget(self.label_cols2)
        input_layout.addWidget(self.input_cols2)
        input_layout.addWidget(self.create_button)

        self.principal.addLayout(input_layout)

    def create_matrix(self):
        rows1 = self.input_rows1.value()
        cols1 = self.input_cols1.value()
        rows2 = self.input_rows2.value()
        cols2 = self.input_cols2.value()

        self.matrix1 = QGridLayout()
        self.matrix1_inputs = []
        if cols1 == rows2:
            for i in range(cols1):
                rows_inputs1 = []
                for j in range(rows1):
                    input1 = QLineEdit()
                    self.matrix1.addWidget(input1,i,j)
                    rows_inputs1.append(input1)
                self.matrix1_inputs.append(rows_inputs1)

            self.principal.addLayout(self.matrix1)
        else:
            QMessageBox.warning(self,"Error","The number of columns does not match with the number of rows\n", QMessageBox.StandardButton.Close,QMessageBox.StandardButton.Close)
            