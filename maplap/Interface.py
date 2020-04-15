import sys
from PyQt5 import QtWidgets, QtGui, QtCore
import design

#to const file?
START_PICTURE = "maplap/templates/MapLap.png"
SIZE_PANEL = 140
SIZE_LINE = 25
BORDER = 9
ROTATE = 90
FULL_ROTATE = 360
MIN_H = 300
ZERO = 0
DOUBLE = 2
INIT_FACTOR = 1.0
UPDATE = True
TEMPLATE_FILE = "*.png *.pdf *.jpg *.bmp"
#

width_screen = ZERO; height_screen = ZERO


class MainWindow(QtWidgets.QMainWindow, design.Ui_MapLap):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.cropping.clicked.connect(self.__cropping)
        self.select_area.clicked.connect(self.__select_area)
        self.choose_file.clicked.connect(self.__choose_file)
        self.save_tex.clicked.connect(self.__save_tex)
        self.save_pdf.clicked.connect(self.__save_pdf)
        self.rotate.clicked.connect(self.__rotate)

        self.angle = ZERO
        self.picture = START_PICTURE
        self.picture_factor = INIT_FACTOR

        pixmap = QtGui.QPixmap(START_PICTURE)
        self.picture_in.setPixmap(pixmap)
        self.picture_out.setPixmap(pixmap)
        self.picture_in._pixmap = QtGui.QPixmap(self.picture_in.pixmap())
        self.picture_out._pixmap = QtGui.QPixmap(self.picture_in.pixmap())
        self.resize(DOUBLE * (SIZE_LINE + pixmap.width()) + SIZE_PANEL, pixmap.height())

    def update_image(self):
        pixmap = QtGui.QPixmap(self.picture)
        pixmap = pixmap.transformed(QtGui.QTransform().rotate(self.angle))
        new_width = DOUBLE * (SIZE_LINE + pixmap.width()) + SIZE_PANEL
        #handle maximum screen size!
        self.setMinimumSize(QtCore.QSize(new_width / pixmap.height() * MIN_H, MIN_H))
        self.picture_in.setPixmap(pixmap)
        self.picture_out.setPixmap(pixmap)
        self.picture_in._pixmap = QtGui.QPixmap(self.picture_in.pixmap())
        self.picture_out._pixmap = QtGui.QPixmap(self.picture_out.pixmap())
        self.resize(new_width * self.picture_factor, pixmap.height() * self.picture_factor)
        self.resizeEvent(UPDATE)

    def __cropping(self):
        pass

    def __select_area(self):
        pass

    def __choose_file(self):
        dialog = QtWidgets.QFileDialog(self)
        dialog.setFileMode(QtWidgets.QFileDialog.ExistingFile)
        dialog.setNameFilter(TEMPLATE_FILE)
        if dialog.exec_():
            self.picture = "".join(dialog.selectedFiles())
            self.angle = ZERO
            self.picture_factor = INIT_FACTOR
            self.update_image()

    def __save_tex(self):
        #changing, save ...
        pass
        
    def __save_pdf(self):
        #save
        pass

    def __rotate(self):
        pixmap = QtGui.QPixmap(self.picture)
        pixmap = pixmap.transformed(QtGui.QTransform().rotate(self.angle))
        self.picture_factor = (self.picture_in.height() + DOUBLE * BORDER) / pixmap.height()
        self.angle = (self.angle + ROTATE) % FULL_ROTATE
        self.update_image()

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Return: #enter
            print('enter')
            #...
        elif event.key() == QtCore.Qt.Key_Escape:
            print('exit')
            #...

    def resizeEvent(self, event):
        self.picture_in.setPixmap(self.picture_in._pixmap.scaled(
            self.width(), self.height(),
            QtCore.Qt.KeepAspectRatio))
        self.picture_out.setPixmap(self.picture_out._pixmap.scaled(
            self.width(), self.height(),
            QtCore.Qt.KeepAspectRatio))

    def focusInEvent(self, event):
        pass

    #...

def main():
    app = QtWidgets.QApplication(sys.argv)
    screen_rect = app.desktop().screenGeometry()
    global width_screen, height_screen
    width_screen, height_screen = screen_rect.width(), screen_rect.height()
    window = MainWindow()
    window.show()
    app.exec_()
    

if __name__ == '__main__':
    main()