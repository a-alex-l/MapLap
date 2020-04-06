import sys
from PyQt5 import QtWidgets
import design

class ExampleApp(QtWidgets.QMainWindow, design.Ui_MapLap):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.cropping.clicked.connect(self.__cropping)
        self.select_area.clicked.connect(self.__select_area)
        self.choose_file.clicked.connect(self.__choose_file)
        self.save_tex.clicked.connect(self.__save_tex)
        self.save_pdf.clicked.connect(self.__save_pdf)
        self.rotate.clicked.connect(self.__rotate)

    def __cropping(self):
        pass

    def __select_area(self):
        pass

    def __choose_file(self):
        pass

    def __save_tex(self):
        pass

    def __save_pdf(self):
        pass

    def __rotate(self):
        pass

def main():
    app = QtWidgets.QApplication(sys.argv)
    window = ExampleApp()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()