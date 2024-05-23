import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton

class Vectors(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Vector Calculator")
        self.setGeometry(100, 100, 400, 300)  # Increased the window height to accommodate instructions
        
        self.initUI()
        
    def initUI(self):
        main_layout = QVBoxLayout()
        
        # Step 1: Label and input field for Vector 1
        self.label_vector1 = QLabel("Step 1: Enter the values of Vector 1 separated by commas:")
        self.input_vector1 = QLineEdit()
        
        # Step 2: Label and input field for Vector 2
        self.label_vector2 = QLabel("Step 2: Enter the values of Vector 2 separated by commas:")
        self.input_vector2 = QLineEdit()
        
        # Step 3: Buttons to perform operations
        self.btn_sum = QPushButton("Sum Vectors")
        self.btn_sum.clicked.connect(self.sum_vectors)
        
        self.btn_dot_product = QPushButton("Dot Product")
        self.btn_dot_product.clicked.connect(self.calculate_dot_product)
        
        # Step 4: Label to show results or error messages
        self.label_result = QLabel("Step 4: Click 'Sum Vectors' or 'Dot Product' to get the result.")
        
        # Step 5: Labels for detailed instructions on how operations are performed
        self.label_sum_instructions = QLabel("How to sum vectors:\nTo sum two vectors, add the corresponding elements of each vector.")
        self.label_dot_product_instructions = QLabel("How to calculate dot product:\nThe dot product is calculated by multiplying corresponding elements of the two vectors and summing them.")
        
        # Add widgets to the main layout
        main_layout.addWidget(self.label_vector1)
        main_layout.addWidget(self.input_vector1)
        main_layout.addWidget(self.label_vector2)
        main_layout.addWidget(self.input_vector2)
        
        layout_buttons = QHBoxLayout()
        layout_buttons.addWidget(self.btn_sum)
        layout_buttons.addWidget(self.btn_dot_product)
        
        main_layout.addLayout(layout_buttons)
        main_layout.addWidget(self.label_result)
        
        # Add detailed instructions
        main_layout.addWidget(self.label_sum_instructions)
        main_layout.addWidget(self.label_dot_product_instructions)
        
        self.setLayout(main_layout)
        
    def sum_vectors(self):
        # Paso 6: Extraer vectores de los campos de entrada
        vector1 = [int(x) for x in self.input_vector1.text().split(",")]
        vector2 = [int(x) for x in self.input_vector2.text().split(",")]
        
        # Paso 7: Verificar si los vectores tienen la misma longitud
        if len(vector1) != len(vector2):
            self.label_result.setText("Error! Los vectores tienen dimensiones diferentes y no se puede calcular el producto punto.")
            return
        
        # Paso 8: Calcular la suma de vectores
        sum_result = [vector1[i] + vector2[i] for i in range(len(vector1))]
        
        # Paso 9: Mostrar el resultado
        self.label_result.setText("La suma de los vectores es: " + str(sum_result))

    
    def calculate_dot_product(self):
        # Step 6: Extract vectors from input fields
        vector1 = [int(x) for x in self.input_vector1.text().split(",")]
        vector2 = [int(x) for x in self.input_vector2.text().split(",")]
        
        # Step 7: Check if vectors have the same length
        if len(vector1) != len(vector2):
            self.label_result.setText("Error! Vectors have different dimensions and dot product cannot be calculated.")
            return
        
        # Step 8: Calculate dot product
        dot_product = sum([vector1[i] * vector2[i] for i in range(len(vector1))])
        
        # Step 9: Show the result
        self.label_result.setText("The dot product is: " + str(dot_product))
