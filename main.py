import sys
from PyQt5.QtWidgets import QApplication
from ui.text_replacement_app import TextReplacementApp

def main():
    app = QApplication(sys.argv)
    window = TextReplacementApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
