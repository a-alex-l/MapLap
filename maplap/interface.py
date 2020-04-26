"""interface"""
import sys

from PyQt5 import Qt, QtCore, QtGui, QtWidgets

import constant as C
from design import UiMapLap


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


class SettingsParams:
    """Params for settings"""

    # pylint: disable=R1721
    # I know that better - ok

    def __init__(self, line_param):
        params = [elem for elem in list(line_param.split(","))]
        assert len(params) == C.PARAMS_IN_SETTING
        for i in range(C.PARAMS_IN_SETTING):
            setattr(self, C.SETTINGS_PARAM_ATR[i], params[i])

    def none_for_pylint(self):
        """do nothing"""
        self.none_for_pylint()

    def also_none_for_pylint(self):
        """also do nothing"""
        self.also_none_for_pylint()


class Settings:
    """Settings struct"""

    # pylint: disable=R1721
    # I know that better - ok

    def __init__(self):
        with open(C.DEFAULT_SETTINGS, "r") as file_settings:
            all_lines = [line for line in file_settings]
            assert len(all_lines) == C.SETTINGS_PARAMS
            for i in range(C.SETTINGS_PARAMS):
                setattr(self, C.SETTINGS_ATR[i], SettingsParams(all_lines[i]))
        self.read_settings()

    def read_settings(self):
        """read settings file"""
        try:
            with open(C.SETTINGS, "r") as file_settings:
                all_lines = [line for line in file_settings]
                assert len(all_lines) == C.SETTINGS_PARAMS
                for i in range(C.SETTINGS_PARAMS):
                    name, value = all_lines[i].split()
                    setattr(getattr(self, C.SETTINGS_ATR[i]), C.SETTINGS_PARAM_ATR[0], name)
                    setattr(getattr(self, C.SETTINGS_ATR[i]), C.SETTINGS_PARAM_ATR[1], value)
        except IOError:
            print("Left default settings!")

    def save_settings(self):
        """save settings to file"""
        file_settings = open(C.SETTINGS, "w")
        for i in range(C.SETTINGS_PARAMS):
            file_settings.write(
                "{} {}\n".format(
                    getattr(getattr(self, C.SETTINGS_ATR[i]), C.SETTINGS_PARAM_ATR[0]),
                    getattr(getattr(self, C.SETTINGS_ATR[i]), C.SETTINGS_PARAM_ATR[1]),
                )
            )
        file_settings.close()


class MainWindow(QtWidgets.QMainWindow, UiMapLap):
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

    def __init__(self, screen_w, screen_h):
        super().__init__()
        self.setupUi(self, screen_w, screen_h)
        self.cropping.clicked.connect(self.__cropping)
        self.select_area.clicked.connect(self.__select_area)
        self.choose_file.clicked.connect(self.__choose_file)
        self.save_tex.clicked.connect(self.__save_tex)
        self.save_pdf.clicked.connect(self.__save_pdf)
        self.rotate.clicked.connect(self.__rotate)
        self.pencil.clicked.connect(self.__pencil)
        self.eraser.clicked.connect(self.__eraser)
        self.spin_block_size.valueChanged.connect(self.__settings_block_size)
        self.slider_block_size.valueChanged.connect(self.__settings_block_size)
        self.spin_max_thick.valueChanged.connect(self.__settings_max_thick)
        self.slider_max_thick.valueChanged.connect(self.__settings_max_thick)
        self.spin_min_line_len.valueChanged.connect(self.__settings_min_line_len)
        self.slider_min_line_len.valueChanged.connect(self.__settings_min_line_len)
        self.spin_min_radius.valueChanged.connect(self.__settings_min_radius)
        self.slider_min_radius.valueChanged.connect(self.__settings_min_radius)
        self.spin_speed_rate.valueChanged.connect(self.__settings_speed_rate_spin)
        self.slider_speed_rate.valueChanged.connect(self.__settings_speed_rate_slider)
        # print(self.desktop().screenGeometry().width())

        self.settings = Settings()
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
        self.set_settings()

    def __save_tex(self):
        """changing, save ..."""
        self.resize_window()  # doesn't do anything yet
        ##

    def __save_pdf(self):
        """saving pdf"""
        self.picture_in.pixmap().save("maplap/templates/temp.pdf", "PDF")  # it doesn't seem to work
        ##

    def __cropping(self):
        """run the algorithm and display the picture"""
        self.settings.save_settings()
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
        width_pixmap_res = pixmap_res.width() * pixmap.height() / pixmap_res.height()
        new_width = pixmap.width() + width_pixmap_res  #
        self.setMinimumSize(
            QtCore.QSize(new_width / pixmap.height() * C.MIN_H + width_some, C.MIN_H)
        )
        self.resize(
            (pixmap.width() + width_pixmap_res) * self.picture_factor + width_some,
            pixmap.height() * self.picture_factor,
        )
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
        if event.key() == QtCore.Qt.Key_Return:  # enter
            if self.is_area_up:
                self.resizeEvent(C.UPDATE)
                self.check_area_coord()
                copy = self.picture_in.pixmap().copy(
                    self.area.x_start,
                    self.area.y_start,
                    self.area.x_end - self.area.x_start,
                    self.area.y_end - self.area.y_start,
                )
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
            self.resizeEvent(C.UPDATE)
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
        self.picture_in.setPixmap(
            self.picture_in._pixmap.scaled(self.width(), self.height(), QtCore.Qt.KeepAspectRatio)
        )
        self.picture_out.setPixmap(
            self.picture_out._pixmap.scaled(self.width(), self.height(), QtCore.Qt.KeepAspectRatio)
        )
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
            paint.drawRect(
                self.area.x_start,
                self.area.y_start,
                self.area.x_end - self.area.x_start,
                self.area.y_end - self.area.y_start,
            )
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
        draw.drawRect(
            self.area.x_start,
            self.area.y_start,
            self.area.x_end - self.area.x_start,
            self.area.y_end - self.area.y_start,
        )

    def set_pen(self, delete=False):
        """sets the desired pen"""
        if self.action == "pencil" and not delete:
            return Qt.QPen(QtCore.Qt.black, C.BLACK_W)
        return Qt.QPen(QtCore.Qt.white, C.WHITE_W)

    def __settings_block_size(self, new_num):
        """change block size everywhere"""
        self.slider_block_size.setProperty("value", new_num)
        self.spin_block_size.setProperty("value", new_num)
        setattr(
            getattr(self.settings, C.SETTINGS_ATR[C.BLOCK_SIZE]),
            C.SETTINGS_PARAM_ATR[C.VALUE],
            new_num,
        )

    def __settings_max_thick(self, new_num):
        """change max thick everywhere"""
        self.slider_max_thick.setProperty("value", new_num)
        self.spin_max_thick.setProperty("value", new_num)
        setattr(
            getattr(self.settings, C.SETTINGS_ATR[C.MAX_THICKNESS]),
            C.SETTINGS_PARAM_ATR[C.VALUE],
            new_num,
        )

    def __settings_min_line_len(self, new_num):
        """change min line length everywhere"""
        self.slider_min_line_len.setProperty("value", new_num)
        self.spin_min_line_len.setProperty("value", new_num)
        setattr(
            getattr(self.settings, C.SETTINGS_ATR[C.MIN_LINE_LENGTH]),
            C.SETTINGS_PARAM_ATR[C.VALUE],
            new_num,
        )

    def __settings_min_radius(self, new_num):
        """change min radius everywhere"""
        self.slider_min_radius.setProperty("value", new_num)
        self.spin_min_radius.setProperty("value", new_num)
        setattr(
            getattr(self.settings, C.SETTINGS_ATR[C.MIN_RADIUS]),
            C.SETTINGS_PARAM_ATR[C.VALUE],
            new_num,
        )

    def __settings_speed_rate_slider(self, new_num):
        """change speed rate spin"""
        self.spin_speed_rate.setProperty("value", new_num / C.TEN)
        setattr(
            getattr(self.settings, C.SETTINGS_ATR[C.SPEED_RATE]),
            C.SETTINGS_PARAM_ATR[C.VALUE],
            new_num / C.TEN,
        )

    def __settings_speed_rate_spin(self, new_num):
        """change speed rate slider"""
        self.slider_speed_rate.setProperty("value", new_num * C.TEN)
        setattr(
            getattr(self.settings, C.SETTINGS_ATR[C.SPEED_RATE]),
            C.SETTINGS_PARAM_ATR[C.VALUE],
            new_num,
        )

    def set_settings(self):
        """set init settings"""
        self.slider_block_size.setProperty(
            "value",
            getattr(
                getattr(self.settings, C.SETTINGS_ATR[C.BLOCK_SIZE]), C.SETTINGS_PARAM_ATR[C.VALUE]
            ),
        )
        self.spin_block_size.setProperty(
            "value",
            getattr(
                getattr(self.settings, C.SETTINGS_ATR[C.BLOCK_SIZE]), C.SETTINGS_PARAM_ATR[C.VALUE]
            ),
        )
        self.slider_max_thick.setProperty(
            "value",
            getattr(
                getattr(self.settings, C.SETTINGS_ATR[C.MAX_THICKNESS]),
                C.SETTINGS_PARAM_ATR[C.VALUE],
            ),
        )
        self.spin_max_thick.setProperty(
            "value",
            getattr(
                getattr(self.settings, C.SETTINGS_ATR[C.MAX_THICKNESS]),
                C.SETTINGS_PARAM_ATR[C.VALUE],
            ),
        )
        self.slider_min_line_len.setProperty(
            "value",
            getattr(
                getattr(self.settings, C.SETTINGS_ATR[C.MIN_LINE_LENGTH]),
                C.SETTINGS_PARAM_ATR[C.VALUE],
            ),
        )
        self.spin_min_line_len.setProperty(
            "value",
            getattr(
                getattr(self.settings, C.SETTINGS_ATR[C.MIN_LINE_LENGTH]),
                C.SETTINGS_PARAM_ATR[C.VALUE],
            ),
        )
        self.slider_min_radius.setProperty(
            "value",
            getattr(
                getattr(self.settings, C.SETTINGS_ATR[C.MIN_RADIUS]), C.SETTINGS_PARAM_ATR[C.VALUE]
            ),
        )
        self.spin_min_radius.setProperty(
            "value",
            getattr(
                getattr(self.settings, C.SETTINGS_ATR[C.MIN_RADIUS]), C.SETTINGS_PARAM_ATR[C.VALUE]
            ),
        )
        self.spin_speed_rate.setProperty(
            "value",
            getattr(
                getattr(self.settings, C.SETTINGS_ATR[C.SPEED_RATE]), C.SETTINGS_PARAM_ATR[C.VALUE]
            ),
        )
        self.slider_speed_rate.setProperty(
            "value",
            getattr(
                getattr(self.settings, C.SETTINGS_ATR[C.SPEED_RATE]), C.SETTINGS_PARAM_ATR[C.VALUE]
            )
            * C.TEN,
        )

        self.box_block_size.setToolTip(
            "Discription: %sRange: %s"
            % (
                getattr(
                    getattr(self.settings, C.SETTINGS_ATR[C.BLOCK_SIZE]),
                    C.SETTINGS_PARAM_ATR[C.DESCRIPTION],
                ),
                getattr(
                    getattr(self.settings, C.SETTINGS_ATR[C.BLOCK_SIZE]),
                    C.SETTINGS_PARAM_ATR[C.RANGE],
                ),
            )
        )
        self.box_block_size.setToolTipDuration(C.TIME_TIP)
        self.box_max_thick.setToolTip(
            "Discription: %sRange: %s"
            % (
                getattr(
                    getattr(self.settings, C.SETTINGS_ATR[C.MAX_THICKNESS]),
                    C.SETTINGS_PARAM_ATR[C.DESCRIPTION],
                ),
                getattr(
                    getattr(self.settings, C.SETTINGS_ATR[C.MAX_THICKNESS]),
                    C.SETTINGS_PARAM_ATR[C.RANGE],
                ),
            )
        )
        self.box_max_thick.setToolTipDuration(C.TIME_TIP)
        self.box_min_line_len.setToolTip(
            "Discription: %sRange: %s"
            % (
                getattr(
                    getattr(self.settings, C.SETTINGS_ATR[C.MIN_LINE_LENGTH]),
                    C.SETTINGS_PARAM_ATR[C.DESCRIPTION],
                ),
                getattr(
                    getattr(self.settings, C.SETTINGS_ATR[C.MIN_LINE_LENGTH]),
                    C.SETTINGS_PARAM_ATR[C.RANGE],
                ),
            )
        )
        self.box_min_line_len.setToolTipDuration(C.TIME_TIP)
        self.box_min_radius.setToolTip(
            "Discription: %sRange: %s"
            % (
                getattr(
                    getattr(self.settings, C.SETTINGS_ATR[C.MIN_RADIUS]),
                    C.SETTINGS_PARAM_ATR[C.DESCRIPTION],
                ),
                getattr(
                    getattr(self.settings, C.SETTINGS_ATR[C.MIN_RADIUS]),
                    C.SETTINGS_PARAM_ATR[C.RANGE],
                ),
            )
        )
        self.box_min_radius.setToolTipDuration(C.TIME_TIP)
        self.box_speed_rate.setToolTip(
            "Discription: %sRange: %s"
            % (
                getattr(
                    getattr(self.settings, C.SETTINGS_ATR[C.SPEED_RATE]),
                    C.SETTINGS_PARAM_ATR[C.DESCRIPTION],
                ),
                getattr(
                    getattr(self.settings, C.SETTINGS_ATR[C.SPEED_RATE]),
                    C.SETTINGS_PARAM_ATR[C.RANGE],
                ),
            )
        )
        self.box_speed_rate.setToolTipDuration(C.TIME_TIP)


def main():
    """program launch function"""

    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow(
        app.desktop().screenGeometry().width(), app.desktop().screenGeometry().height()
    )
    window.show()
    app.exec_()


if __name__ == "__main__":
    main()
