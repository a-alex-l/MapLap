"""interface"""
import sys
from PyQt5 import QtCore, QtGui, QtWidgets, Qt
from maplap.design import Ui_MapLap
import constant as C

WIDTH_SCREEN = C.ZERO
HEIGHT_SCREEN = C.ZERO

class Rectangle:
    """Rectangle struct"""
    def __init__(self, x1=C.ZERO, y1=C.ZERO, x2=C.ZERO, y2=C.ZERO):
        self.x_start = x1
        self.y_start = y1
        self.x_end = x2
        self.y_end = y2

    def none_for_pylint(self):
        """do nothing"""
        self.none_for_pylint()

    def also_none_for_pylint(self):
        """also do nothing"""
        self.also_none_for_pylint()

class MainWindow(QtWidgets.QMainWindow, Ui_MapLap):
    """Main window"""
    # pylint: disable=R0902
    # 9/7 attributes - I will fix it later

    # but how fix:

    # pylint: disable=W0212
    # it is unclear how else to write _pixmap

    # pylint: disable=C0103
    # is it better to rewrite the originally defined methods like resizeEvent?

    # pylint: disable=W0613
    # event in resizeEvent and other

    # pylint: disable=R0912
    # many branches in keyPressEvent

    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.cropping.clicked.connect(self.__cropping)
        self.select_area.clicked.connect(self.__select_area)
        self.choose_file.clicked.connect(self.__choose_file)
        self.save_tex.clicked.connect(self.__save_tex)
        self.save_pdf.clicked.connect(self.__save_pdf)
        self.rotate.clicked.connect(self.__rotate)
        self.pencil.clicked.connect(self.__pencil)
        self.eraser.clicked.connect(self.__eraser)

        self.angle = [C.ZERO, C.ZERO]
        self.picture = self.picture_res = C.START_PICTURE
        self.picture_factor = C.INIT_FACTOR
        self.action = "no"
        self.area = Rectangle()
        self.need_update = False
        self.is_area_up = False
        self.picture_in.mouseMoveEvent = self.do_nothing
        self.picture_in.mousePressEvent = self.do_nothing
        self.picture_in.mouseReleaseEvent = self.do_nothing
        self.path = Qt.QPainterPath()
        self.init_picture()

    def __save_tex(self):
        """changing, save ..."""
        self.resize_window() #doesn't do anything yet
        ##

    def __save_pdf(self):
        """saving pdf"""
        self.picture_in.pixmap().save("maplap/templates/temp.pdf", "PDF") #it doesn't seem to work
        ##

    def __cropping(self):
        """run the algorithm and display the picture"""
        self.picture_res = C.RES
        self.save_image(C.PICTURE_OUT)
        self.update_image()
        ##

    def init_picture(self):
        """initial installation of the picture"""
        self.resize_window()
        self.picture = C.TEMP
        self.save_image()
        self.__cropping()
        self.resize_window()

    def save_image(self, is_picture_in=True, file_format=C.FORMAT):
        """saves the image to the desired file"""
        if is_picture_in:
            self.picture_in.pixmap().save(C.TEMP, file_format)
            self.angle[0] = C.ZERO
        else:
            self.picture_in.pixmap().save(C.RES, file_format)
            self.angle[1] = C.ZERO

    def resize_window(self):
        """normalizes the window size when changing it"""
        pixmap = QtGui.QPixmap(self.picture)
        pixmap_res = QtGui.QPixmap(self.picture_res)
        pixmap = pixmap.transformed(QtGui.QTransform().rotate(self.angle[0]))
        pixmap_res = pixmap_res.transformed(QtGui.QTransform().rotate(self.angle[1]))
        width_some = C.DOUBLE * C.SIZE_LINE + C.SIZE_PANEL
        new_width = min(pixmap.width() + pixmap_res.width() + width_some, WIDTH_SCREEN)
        self.setMinimumSize(QtCore.QSize(new_width / pixmap.height() * C.MIN_H, C.MIN_H))
        self.resize((pixmap.width() + pixmap_res.width()) * self.picture_factor + C.SIZE_PANEL,
                    pixmap.height() * self.picture_factor)
        self.update_image()

    def update_image(self):
        """updates images"""
        width = self.width()
        height = self.height()
        pixmap = QtGui.QPixmap(self.picture)
        pixmap_res = QtGui.QPixmap(self.picture_res)
        pixmap = pixmap.transformed(QtGui.QTransform().rotate(self.angle[0]))
        pixmap_res = pixmap_res.transformed(QtGui.QTransform().rotate(self.angle[1]))
        self.picture_in.setPixmap(pixmap)
        self.picture_out.setPixmap(pixmap_res)
        self.picture_in._pixmap = QtGui.QPixmap(self.picture_in.pixmap())
        self.picture_out._pixmap = QtGui.QPixmap(self.picture_out.pixmap())
        self.resize(width, height)
        self.resizeEvent(C.UPDATE)

    def __select_area(self):
        """changes the activity to select an area"""
        if self.action == "select":
            self.change_action("no")
        else:
            self.change_action("select")

    def change_action(self, mode):
        """sets the desired settings for the current mode activity"""
        if mode == "no":
            self.select_area.setText("select area")
            self.picture_in.setProperty("cursor", QtGui.QCursor(QtCore.Qt.ArrowCursor))
            self.picture_in.mouseMoveEvent = self.do_nothing
            self.picture_in.mousePressEvent = self.do_nothing
            self.picture_in.mouseReleaseEvent = self.do_nothing
            self.resizeEvent(C.UPDATE)
        elif mode == "select":
            self.select_area.setText("no select area")
            self.picture_in.setProperty("cursor", QtGui.QCursor(QtCore.Qt.CrossCursor))
            self.picture_in.mouseMoveEvent = self.mouse_move_event_select
            self.picture_in.mousePressEvent = self.mouse_press_event_select
            self.picture_in.mouseReleaseEvent = self.mouse_release_event_select
        elif mode == "eraser":
            self.select_area.setText("select area")
            self.picture_in.setProperty("cursor", QtGui.QCursor(QtCore.Qt.PointingHandCursor))
            self.picture_in.mouseMoveEvent = self.draw
            self.picture_in.mousePressEvent = self.set_point
            self.picture_in.mouseReleaseEvent = self.end_path
            self.resizeEvent(C.UPDATE)
        elif mode == "pencil":
            self.select_area.setText("select area")
            self.picture_in.setProperty("cursor", QtGui.QCursor(QtCore.Qt.PointingHandCursor))
            self.picture_in.mouseMoveEvent = self.draw
            self.picture_in.mousePressEvent = self.set_point
            self.picture_in.mouseReleaseEvent = self.end_path
            self.resizeEvent(C.UPDATE)
        else:
            print("error in change_action")
            self.change_action("no")
        self.action = mode

    def __choose_file(self):
        """file selection from the directory"""
        dialog = QtWidgets.QFileDialog(self)
        dialog.setFileMode(QtWidgets.QFileDialog.ExistingFile)
        dialog.setNameFilter(C.TEMPLATE_FILE)
        if dialog.exec_():
            self.picture = "".join(dialog.selectedFiles())
            self.angle[0] = C.ZERO
            self.picture_factor = C.INIT_FACTOR
            self.init_picture()

    def __rotate(self):
        """rotates images"""
        pixmap = QtGui.QPixmap(self.picture)
        pixmap = pixmap.transformed(QtGui.QTransform().rotate(self.angle[0]))
        self.picture_factor = (self.picture_in.height() + C.DOUBLE * C.BORDER) / pixmap.height()
        self.angle[0] = (self.angle[0] + C.ROTATE) % C.FULL_ROTATE
        self.angle[1] = (self.angle[1] + C.ROTATE) % C.FULL_ROTATE
        self.resize_window()

    def check_area_coord(self):
        """normalizes the coordinates of the selected area"""
        if self.area.x_start > self.area.x_end:
            self.area.x_start, self.area.x_end = self.area.x_end, self.area.x_start
        if self.area.y_start > self.area.y_end:
            self.area.y_start, self.area.y_end = self.area.y_end, self.area.y_start
        self.area.x_start = max(self.area.x_start, C.ZERO)
        self.area.y_start = max(self.area.y_start, C.ZERO)
        self.area.x_end = min(self.area.x_end, self.picture_in.width())
        self.area.y_end = min(self.area.y_end, self.picture_in.height() + C.CURSOR)

    def keyPressEvent(self, event):
        """keyboard click events"""
        if event.key() == QtCore.Qt.Key_Return: #enter
            if self.is_area_up:
                self.resizeEvent(C.UPDATE)
                self.check_area_coord()
                copy = self.picture_in.pixmap().copy(self.area.x_start, self.area.y_start,
                                                     self.area.x_end - self.area.x_start,
                                                     self.area.y_end - self.area.y_start)
                self.picture_in.setPixmap(copy)
                self.save_image()
                self.resize_window()
        if event.key() == QtCore.Qt.Key_Backspace:
            if self.is_area_up:
                self.resizeEvent(C.UPDATE)
                self.check_area_coord()
                self.erase_rect()
                self.save_image()
                self.resize_window()
        elif event.key() == QtCore.Qt.Key_F5:
            self.__cropping()
        elif event.key() == QtCore.Qt.Key_F4:
            self.__rotate()
        elif event.modifiers():
            if event.key() == QtCore.Qt.Key_Up:
                self.move(self.pos().x() - C.STEP, self.pos().y())
            if event.key() == QtCore.Qt.Key_Down:
                self.move(self.pos().x() + C.STEP, self.pos().y())
            elif event.key() == QtCore.Qt.Key_Escape:
                sys.exit(0)
        else:
            if event.key() == QtCore.Qt.Key_Up:
                self.move(self.pos().x(), self.pos().y() - C.STEP)
            if event.key() == QtCore.Qt.Key_Down:
                self.move(self.pos().x(), self.pos().y() + C.STEP)

    def resizeEvent(self, event):
        """the resize event of the window"""
        self.picture_in.setPixmap(self.picture_in._pixmap.scaled(
            self.width(), self.height(),
            QtCore.Qt.KeepAspectRatio))
        self.picture_out.setPixmap(self.picture_out._pixmap.scaled(
            self.width(), self.height(),
            QtCore.Qt.KeepAspectRatio))
        self.is_area_up = False

    def do_nothing(self, event):
        """empty link (is used)"""
        self.action = self.action

    def mouse_press_event_select(self, event):
        """press event in select"""
        if self.action == "select":
            self.resizeEvent(C.UPDATE)
            self.area.x_start = event.x()
            self.area.y_start = event.y() + C.CURSOR

    def mouse_move_event_select(self, event):
        """move event in select"""
        if self.action == "select":
            self.need_update = True
            self.area.x_end = event.x()
            self.area.y_end = event.y() + C.CURSOR
            self.picture_in.update()

    def mouse_release_event_select(self, event):
        """release event in select"""
        if self.action == "select":
            self.area.x_end = event.x()
            self.area.y_end = event.y() + C.CURSOR

    def paintEvent(self, event):
        """draws an area selection window"""
        if self.action == "select" and self.need_update:
            self.need_update = False
            self.update_image()
            paint = QtGui.QPainter()
            paint.begin(self.picture_in.pixmap())
            paint.setOpacity(C.OPACITY_AREA)
            paint.setBrush(QtGui.QBrush(QtCore.Qt.blue))
            paint.drawRect(self.area.x_start, self.area.y_start,
                           self.area.x_end - self.area.x_start,
                           self.area.y_end - self.area.y_start)
            paint.end()
            self.is_area_up = True

    def __pencil(self):
        """sets the drawing activity"""
        if self.action == "pencil":
            self.change_action("no")
        else:
            self.change_action("pencil")

    def __eraser(self):
        """sets the activity on the wipe"""
        if self.action == "eraser":
            self.change_action("no")
        else:
            self.change_action("eraser")

    def set_point(self, event):
        """sets the start point for drawing"""
        self.path.moveTo(event.pos())

    def draw(self, event):
        """draw event on image"""
        self.path.lineTo(event.pos())
        draw = Qt.QPainter(self.picture_in.pixmap())
        draw.setPen(self.set_pen())
        draw.drawPath(self.path)
        self.picture_in.update()

    def end_path(self, event):
        """drawing end event"""
        self.save_image()
        self.path = Qt.QPainterPath()
        self.update_image()

    def erase_rect(self):
        """deletes a rectangular area"""
        draw = Qt.QPainter(self.picture_in.pixmap())
        draw.setPen(self.set_pen(C.DELETE))
        draw.setBrush(QtCore.Qt.white)
        draw.drawRect(self.area.x_start, self.area.y_start,
                      self.area.x_end - self.area.x_start, self.area.y_end - self.area.y_start)

    def set_pen(self, delete=False):
        """sets the desired pen"""
        if self.action == "pencil" and not delete:
            return Qt.QPen(QtCore.Qt.black, C.BLACK_W)
        return Qt.QPen(QtCore.Qt.white, C.WHITE_W)

def main():
    # pylint: disable=W0603
    # understand how to handle the window size does not globally
    """program launch function"""
    app = QtWidgets.QApplication(sys.argv)
    screen_rect = app.desktop().screenGeometry()
    global WIDTH_SCREEN, HEIGHT_SCREEN
    WIDTH_SCREEN, HEIGHT_SCREEN = screen_rect.width(), screen_rect.height()
    window = MainWindow()
    window.show()
    app.exec_()

if __name__ == '__main__':
    main()
    