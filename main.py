import sys
from PyQt6.QtWidgets import QApplication
from menu import Menu

def main():
    app = QApplication(sys.argv)
    login = Menu()
    sys.exit(app.exec())
main()