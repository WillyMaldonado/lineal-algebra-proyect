import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QGridLayout, QTextEdit
from PyQt6.QtCore import Qt
import numpy as np

class CryptoApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Crypto App')
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.message_label = QLabel("Message:")
        self.message_edit = QLineEdit()
        layout.addWidget(self.message_label)
        layout.addWidget(self.message_edit)

        self.key_label = QLabel("Write the key matrix (3x3):")
        layout.addWidget(self.key_label)
        self.key_edits = []
        key_layout = QGridLayout()
        for i in range(3):
            row_edits = []
            for j in range(3):
                edit = QLineEdit()
                key_layout.addWidget(edit, i, j)
                row_edits.append(edit)
            self.key_edits.append(row_edits)
        layout.addLayout(key_layout)

        self.encrypt_button = QPushButton("Encrypt")
        self.encrypt_button.clicked.connect(self.encrypt_message)
        layout.addWidget(self.encrypt_button)

        self.decrypt_button = QPushButton("Decrypt")
        self.decrypt_button.clicked.connect(self.decrypt_message)
        layout.addWidget(self.decrypt_button)

        self.clear_button = QPushButton("Clear")
        self.clear_button.clicked.connect(self.clear)
        layout.addWidget(self.clear_button)

        self.output_textedit = QTextEdit()
        self.output_textedit.setReadOnly(True)
        layout.addWidget(self.output_textedit)

        self.setLayout(layout)

    def text_to_numbers(self, text):
        letter_to_number = {chr(i): i - 64 for i in range(65, 91)}
        letter_to_number[' '] = 0
        return [letter_to_number[char] for char in text.upper()]

    def numbers_to_text(self, numbers):
        number_to_letter = {i - 64: chr(i) for i in range(65, 91)}
        number_to_letter[0] = ' '
        return ''.join(number_to_letter[number] for number in numbers)

    def vector_to_matrix(self, vector, columns=3):
        rows = 3
        matrix = np.zeros((rows, len(vector) // rows + (len(vector) % rows > 0)), dtype=int)
        for i, num in enumerate(vector):
            matrix[i % rows, i // rows] = num
        return matrix

    def encrypt_message(self):
        sys.stdout = StdoutRedirector(self.output_textedit)

        message = self.message_edit.text()
        key = [[int(edit.text()) for edit in row] for row in self.key_edits]

        try:
            self.output_textedit.clear()
            self.output_textedit.append("Step-by-Step Encryption Process:")

            self.output_textedit.append("\nStep 1: Input Message")
            self.output_textedit.append(message)

            self.output_textedit.append("\nStep 2: Convert Message to Numbers")
            numbers_vector = self.text_to_numbers(message)
            self.output_textedit.append(str(numbers_vector))

            self.output_textedit.append("\nStep 3: Convert Numbers Vector to Matrix")
            original_matrix = self.vector_to_matrix(numbers_vector, columns=3)
            self.output_textedit.append("\n" + str(original_matrix).replace("\n", "\n\t"))

            self.output_textedit.append("\nStep 4: Multiply with Key Matrix")
            encrypted_matrix = np.dot(key, original_matrix)
            self.output_textedit.append("\n" + str(encrypted_matrix).replace("\n", "\n\t"))

            self.encrypted_matrix = encrypted_matrix
        except Exception as e:
            self.output_textedit.append(f"Error: {e}")

    def decrypt_message(self):
        sys.stdout = StdoutRedirector(self.output_textedit)

        try:
            key = [[int(edit.text()) for edit in row] for row in self.key_edits]

            self.output_textedit.append("\nStep-by-Step Decryption Process:")

            self.output_textedit.append("\nStep 1: Key Matrix")
            self.output_textedit.append(str(np.array(key)).replace("\n", "\n\t"))

            self.output_textedit.append("\nStep 2: Inverse Key Matrix")
            inverse_key_matrix = np.linalg.inv(key)
            self.output_textedit.append(str(inverse_key_matrix).replace("\n", "\n\t"))

            self.output_textedit.append("\nStep 3: Multiply Inverse Key Matrix with Encrypted Matrix")
            decrypted_matrix = np.dot(inverse_key_matrix, self.encrypted_matrix)
            self.output_textedit.append("\n" + str(decrypted_matrix).replace("\n", "\n\t"))

            transpose_matrix = np.transpose(decrypted_matrix)

            self.output_textedit.append("\nStep 4: Convert Matrix to Numbers Vector")
            decrypted_numbers = transpose_matrix.flatten().astype(int).tolist()
            self.output_textedit.append(str(decrypted_numbers))

            self.output_textedit.append("\nStep 5: Convert Numbers Vector to Text")
            decrypted_message = self.numbers_to_text(decrypted_numbers)
            self.output_textedit.append(self.message_edit.text())
        except Exception as e:
            self.output_textedit.append(f"Error: {e}")

    def clear(self):
        self.message_edit.clear()
        for row in self.key_edits:
            for edit in row:
                edit.clear()
        self.output_textedit.clear()

class StdoutRedirector:
    def __init__(self, text_edit):
        self.text_edit = text_edit

    def write(self, text):
        self.text_edit.insertPlainText(text)
        self.text_edit.verticalScrollBar().setValue(self.text_edit.verticalScrollBar().maximum())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    crypto_app = CryptoApp()
    crypto_app.show()
    sys.exit(app.exec())

