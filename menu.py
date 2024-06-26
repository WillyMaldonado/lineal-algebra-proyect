from PyQt6.QtWidgets import QPushButton, QDialog, QLabel, QVBoxLayout, QHBoxLayout,QGridLayout, QWidget, QApplication
from Operation_matrix import operation_menu
from markov import MatrixApp
from determinant import Determinant
from inverse import Inverse
from rank import Rank
from vectors.vectors import Vectors
from encrypt import CryptoApp


class Menu(QWidget):
    def __init__(self):
        super().__init__()
        self.generate_menu()

    def generate_menu(self):
        self.setWindowTitle("Lineal algebra menu")
        self.resize(800,600)
        self.generate_window()
        self.show()

    def generate_window(self):
        # Creation of the buttons for the menu
        self.button_matrix_op = QPushButton("Matrix operation")
        self.button_inv_matrix = QPushButton("Inverse of a matrix")
        self.button_det_matrix = QPushButton("Determinant of a matrix")
        self.button_range_matrix = QPushButton("Range of a matrix")
        self.button_encrypt_matrix = QPushButton("Encryption of a matrix")
        self.button_markov = QPushButton("Markov chain")
        self.button_vector_op = QPushButton("Operation between vectors")
        #Add functionality to the buttons
        self.button_matrix_op.clicked.connect(self.operationMenu)
        self.button_inv_matrix.clicked.connect(self.Inv)
        self.button_det_matrix.clicked.connect(self.Det)
        self.button_range_matrix.clicked.connect(self.Ran)
        self.button_encrypt_matrix.clicked.connect(self.crypt)
        self.button_markov.clicked.connect(self.Markov)
        self.button_vector_op.clicked.connect(self.vector)

        self.layout = QGridLayout()
        self.layout.addWidget(self.button_matrix_op,0,0)
        self.layout.addWidget(self.button_inv_matrix,0,1)
        self.layout.addWidget(self.button_det_matrix,0,2)
        self.layout.addWidget(self.button_range_matrix,1,0)
        self.layout.addWidget(self.button_encrypt_matrix,1,1)
        self.layout.addWidget(self.button_markov,1,2)
        self.layout.addWidget(self.button_vector_op)

        self.setLayout(self.layout)

    def operationMenu(self):
        self.menu_view = operation_menu.OperationMenu()
        self.menu_view.show()

    def Markov(self):
        self.markov_view = MatrixApp()
        self.markov_view.show()

    def Det(self):
        self.det_view = Determinant()
        self.det_view.show()

    def Inv(self):
        self.inv_view = Inverse()
        self.inv_view.show()
        
    def Ran(self):
        self.rank_view = Rank()
        self.rank_view.show()

    def vector(self):
        self.vector_view = Vectors()
        self.vector_view.show()

    def crypt(self):
        self.crypt_view = CryptoApp()
        self.crypt_view.show()