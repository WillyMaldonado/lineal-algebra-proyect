from PyQt6.QtWidgets import (
    QPushButton, QLabel, QVBoxLayout, QHBoxLayout,
    QGridLayout, QWidget, QLineEdit, QSpinBox, QSizePolicy, QFrame, QScrollArea
)
from PyQt6.QtCore import Qt
from Operation_matrix import sum, subtraction, multiply
class OperationMenu(QWidget):
    def __init__(self):
        super().__init__()
        self.generate_op_menu()

    def generate_op_menu(self):
        self.setWindowTitle('Operation matrix menu')
        self.resize(800,600)
        self.generate_ui()
        self.show()

    def generate_ui(self):
        self.principal = QHBoxLayout()
        self.setLayout(self.principal)

        self.sum_button = QPushButton("Add matrix")
        self.multiply_button = QPushButton("Multiply matrix")
        self.subtraction_button = QPushButton("Subtraction matrix")
        self.sum_button.clicked.connect(self.add)
        self.subtraction_button.clicked.connect(self.sub)
        self.multiply_button.clicked.connect(self.Multiply)

        self.principal.addWidget(self.sum_button)
        self.principal.addWidget(self.multiply_button)
        self.principal.addWidget(self.subtraction_button)


    def add(self):
        self.sum_view = sum.Sum()
        self.sum_view.show()
    
    def sub(self):
        self.sub_view = subtraction.Sub()
        self.sub_view.show()

    def Multiply(self):
        self.multiply_view = multiply.Multiply()
        self.multiply_view.show()