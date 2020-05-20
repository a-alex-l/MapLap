"""interface"""
import sys

from PyQt5 import Qt, QtCore, QtGui, QtWidgets

import constant as CO
from design import UiMapLap
from settings import Settings, SettingsParams
from geometry import Rectangle
from math import sqrt
import detector
import generator_latex_code as gen


class MainWindow(QtWidgets.QMainWindow, UiMapLap):
    """Main window"""

    def __init__(self, screen_w, screen_h):
        super().__init__()
        self.setupUi(self, screen_w, screen_h)
        self.detect.clicked.connect(self.__detect)
        self.select_area.clicked.connect(self.__select_area)
        self.choose_file.clicked.connect(self.__choose_file)
        self.save_tex.clicked.connect(self.__save_tex)
        self.save_pdf.clicked.connect(self.__save_pdf)
        self.rotate.clicked.connect(self.__rotate)
        self.pencil.clicked.connect(self.__pencil)
        self.eraser.clicked.connect(self.__eraser)
        self.lineI.clicked.connect(self.__line)
        self.circleI.clicked.connect(self.__circle)
        self.spin_block_size.valueChanged.connect(self.__settings_block_size_spin)
        self.slider_block_size.valueChanged.connect(self.__settings_block_size_slider)
        self.spin_max_thick.valueChanged.connect(self.__settings_max_thick)
        self.slider_max_thick.valueChanged.connect(self.__settings_max_thick)
        self.spin_min_line_len.valueChanged.connect(self.__settings_min_line_len)
        self.slider_min_line_len.valueChanged.connect(self.__settings_min_line_len)
        self.spin_min_radius.valueChanged.connect(self.__settings_min_radius)
        self.slider_min_radius.valueChanged.connect(self.__settings_min_radius)
        self.spin_speed_rate.valueChanged.connect(self.__settings_speed_rate_spin)
        self.slider_speed_rate.valueChanged.connect(self.__settings_speed_rate_slider)

        self.settings = Settings()
        self.angle = [CO.ZERO, CO.ZERO]
        self.picture = self.picture_res = CO.START_PICTURE
        self.picture_factor = CO.INIT_FACTOR
        self.action = "no"
        self.area = Rectangle()
        self.line = Rectangle()
        self.circle = Rectangle()
        self.need_update = False
        self.is_area_up = False
        self.picture_in.mouseMoveEvent = self.do_nothing
        self.picture_in.mousePressEvent = self.do_nothing
        self.picture_in.mouseReleaseEvent = self.do_nothing
        self.path = Qt.QPainterPath()
        self.lines = []
        self.circles = []
        self.init_picture()
        self.set_settings()

    def __save_tex(self):
        """changing, save ..."""
        dialog = QtWidgets.QFileDialog(self)
        file_out = dialog.getSaveFileName(self, CO.OPEN, "", CO.TEMPLATE_TEX)
        if file_out[0] != "":
            gen.GeneratorLatexCode(self.circles + self.lines).generator_latex_tex(self.circles + self.lines, file_out[0])

    def __save_pdf(self):
        """saving pdf"""
        dialog = QtWidgets.QFileDialog(self)
        file_out = dialog.getSaveFileName(self, CO.OPEN, "", CO.TEMPLATE_PDF)
        if file_out[0] != "":
            gen.GeneratorLatexCode(self.circles + self.lines).generator_latex_pdf(self.circles + self.lines, file_out[0])

    def __detect(self):
        """run the algorithm and display the picture"""
        self.fix_param()
        self.settings.save_settings()
        self.picture_res = CO.RES
        self.save_image(CO.PICTURE_OUT)
        detect = detector.Detector(self.settings)
        self.lines, self.circles = detect.detect(self.picture_res)
        self.update_image()

    def init_picture(self):
        """initial installation of the picture"""
        self.resize_window()
        self.picture = CO.TEMP
        self.save_image()
        self.__detect()
        self.resize_window()

    def save_image(self, is_picture_in=True, file_format=CO.FORMAT):
        """saves the image to the desired file"""
        if is_picture_in:
            self.picture_in.pixmap().save(CO.TEMP, file_format)
            self.angle[0] = CO.ZERO
        else:
            self.picture_in.pixmap().save(CO.RES, file_format)
            self.angle[1] = CO.ZERO

    def resize_window(self):
        """normalizes the window size when changing it"""
        pixmap = QtGui.QPixmap(self.picture)
        pixmap_res = QtGui.QPixmap(self.picture_res)
        pixmap = pixmap.transformed(QtGui.QTransform().rotate(self.angle[0]))
        pixmap_res = pixmap_res.transformed(QtGui.QTransform().rotate(self.angle[1]))
        width_some = CO.DOUBLE * CO.SIZE_LINE + CO.SIZE_PANEL
        width_pixmap_res = pixmap_res.width() * pixmap.height() / pixmap_res.height()
        new_width = pixmap.width() + width_pixmap_res
        self.setMinimumSize(
            QtCore.QSize(new_width / pixmap.height() * CO.MIN_H + width_some, CO.MIN_H)
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
        self.resizeEvent(CO.UPDATE)

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
            self.resizeEvent(CO.UPDATE)
        elif mode == "select":
            self.select_area.setText("no select area")
            self.picture_in.setProperty("cursor", QtGui.QCursor(QtCore.Qt.CrossCursor))
            self.picture_in.mouseMoveEvent = self.mouse_move_event_select
            self.picture_in.mousePressEvent = self.mouse_press_event_select
            self.picture_in.mouseReleaseEvent = self.mouse_release_event_select
        elif mode == "eraser":
            self.select_area.setText("select area")
            self.picture_in.setProperty(
                "cursor", QtGui.QCursor(QtCore.Qt.PointingHandCursor)
            )
            self.picture_in.mouseMoveEvent = self.draw
            self.picture_in.mousePressEvent = self.set_point
            self.picture_in.mouseReleaseEvent = self.end_path
            self.resizeEvent(CO.UPDATE)
        elif mode == "pencil":
            self.select_area.setText("select area")
            self.picture_in.setProperty(
                "cursor", QtGui.QCursor(QtCore.Qt.PointingHandCursor)
            )
            self.picture_in.mouseMoveEvent = self.draw
            self.picture_in.mousePressEvent = self.set_point
            self.picture_in.mouseReleaseEvent = self.end_path
            self.resizeEvent(CO.UPDATE)
        elif mode == "line":
            self.select_area.setText("select area")
            self.picture_in.setProperty(
                "cursor", QtGui.QCursor(QtCore.Qt.PointingHandCursor)
            )
            self.picture_in.mouseMoveEvent = self.move_line
            self.picture_in.mousePressEvent = self.draw_line
            self.picture_in.mouseReleaseEvent = self.end_line
            self.resizeEvent(CO.UPDATE)
        elif mode == "circle":
            self.select_area.setText("select area")
            self.picture_in.setProperty(
                "cursor", QtGui.QCursor(QtCore.Qt.PointingHandCursor)
            )
            self.picture_in.mouseMoveEvent = self.move_circle
            self.picture_in.mousePressEvent = self.draw_circle
            self.picture_in.mouseReleaseEvent = self.end_circle
            self.resizeEvent(CO.UPDATE)
        else:
            print("error in change_action")
            self.change_action("no")
        self.action = mode

    def __choose_file(self):
        """file selection from the directory"""
        dialog = QtWidgets.QFileDialog(self)
        dialog.setFileMode(QtWidgets.QFileDialog.ExistingFile)
        dialog.setNameFilter(CO.TEMPLATE_FILE)
        if dialog.exec_():
            self.picture = "".join(dialog.selectedFiles())
            self.angle[0] = CO.ZERO
            self.picture_factor = CO.INIT_FACTOR
            self.init_picture()

    def __rotate(self):
        """rotates images"""
        pixmap = QtGui.QPixmap(self.picture)
        pixmap = pixmap.transformed(QtGui.QTransform().rotate(self.angle[0]))
        self.picture_factor = (
            self.picture_in.height() + CO.DOUBLE * CO.BORDER
        ) / pixmap.height()
        self.angle[0] = (self.angle[0] + CO.ROTATE) % CO.FULL_ROTATE
        self.angle[1] = (self.angle[1] + CO.ROTATE) % CO.FULL_ROTATE
        self.resize_window()

    def check_area_coord(self):
        """normalizes the coordinates of the selected area"""
        if self.area.x_start > self.area.x_end:
            self.area.x_start, self.area.x_end = self.area.x_end, self.area.x_start
        if self.area.y_start > self.area.y_end:
            self.area.y_start, self.area.y_end = self.area.y_end, self.area.y_start
        self.area.x_start = max(self.area.x_start, CO.ZERO)
        self.area.y_start = max(self.area.y_start, CO.ZERO)
        self.area.x_end = min(self.area.x_end, self.picture_in.width())
        self.area.y_end = min(self.area.y_end, self.picture_in.height() + CO.CURSOR)

    def keyPressEvent(self, event):
        """keyboard click events"""
        if event.key() == QtCore.Qt.Key_Return:  # enter
            if self.is_area_up:
                self.resizeEvent(CO.UPDATE)
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
                self.resizeEvent(CO.UPDATE)
                self.check_area_coord()
                self.erase_rect()
                self.save_image()
                self.resize_window()
        elif event.key() == QtCore.Qt.Key_F5:
            self.resizeEvent(CO.UPDATE)
            self.__detect()
        elif event.key() == QtCore.Qt.Key_F4:
            self.__rotate()
        elif event.modifiers():
            if event.key() == QtCore.Qt.Key_Up:
                self.move(self.pos().x() - CO.STEP, self.pos().y())
            if event.key() == QtCore.Qt.Key_Down:
                self.move(self.pos().x() + CO.STEP, self.pos().y())
            elif event.key() == QtCore.Qt.Key_Escape:
                sys.exit(0)
        else:
            if event.key() == QtCore.Qt.Key_Up:
                self.move(self.pos().x(), self.pos().y() - CO.STEP)
            if event.key() == QtCore.Qt.Key_Down:
                self.move(self.pos().x(), self.pos().y() + CO.STEP)

    def resizeEvent(self, event):
        """the resize event of the window"""
        self.picture_in.setPixmap(
            self.picture_in._pixmap.scaled(
                self.width(), self.height(), QtCore.Qt.KeepAspectRatio
            )
        )
        self.picture_out.setPixmap(
            self.picture_out._pixmap.scaled(
                self.width(), self.height(), QtCore.Qt.KeepAspectRatio
            )
        )
        self.is_area_up = False

    def do_nothing(self, event):
        """empty link (is used)"""
        self.action = self.action

    def mouse_press_event_select(self, event):
        """press event in select"""
        if self.action == "select":
            self.resizeEvent(CO.UPDATE)
            self.area.x_start = event.x()
            self.area.y_start = event.y() + CO.CURSOR

    def mouse_move_event_select(self, event):
        """move event in select"""
        if self.action == "select":
            self.need_update = True
            self.area.x_end = event.x()
            self.area.y_end = event.y() + CO.CURSOR
            self.picture_in.update()

    def mouse_release_event_select(self, event):
        """release event in select"""
        if self.action == "select":
            self.area.x_end = event.x()
            self.area.y_end = event.y() + CO.CURSOR

    def paintEvent(self, event):
        """draws at window"""
        if self.need_update and (self.action == "line"
                                 or self.action == "circle"
                                 or self.action == "select"):
            self.need_update = False    
            self.update_image()
            paint = QtGui.QPainter()
            paint.begin(self.picture_in.pixmap())
            self.draw_some(paint)
            paint.end()
            if self.action == "select":
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

    def __line(self):
        """sets the activity on the wipe"""
        if self.action == "line":
            self.change_action("no")
        else:
            self.change_action("line")

    def __circle(self):
        """sets the activity on the wipe"""
        if self.action == "circle":
            self.change_action("no")
        else:
            self.change_action("circle")

    def set_point(self, event):
        """sets the start point for drawing"""
        self.path.moveTo(event.pos())

    def draw(self, event):
        """draw event on image"""
        self.path.lineTo(event.pos())
        draw = Qt.QPainter(self.picture_in.pixmap())
        self.draw_some(draw)
        self.picture_in.update()

    def end_path(self, event):
        """drawing end event"""
        self.save_image()
        self.path = Qt.QPainterPath()
        self.update_image()

    def erase_rect(self):
        """deletes a rectangular area"""
        draw = Qt.QPainter(self.picture_in.pixmap())
        draw.setPen(self.set_pen(CO.DELETE))
        draw.setBrush(QtCore.Qt.white)
        draw.drawRect(
            self.area.x_start,
            self.area.y_start,
            self.area.x_end - self.area.x_start,
            self.area.y_end - self.area.y_start,
        )

    def set_pen(self, delete=False):
        """sets the desired pen"""
        if self.action in ["pencil", "line", "circle"] and not delete:
            return Qt.QPen(QtCore.Qt.black, CO.BLACK_W)
        elif self.action == "select":
            return Qt.QPen(QtCore.Qt.white)
        return Qt.QPen(QtCore.Qt.white, CO.WHITE_W)

    def move_line(self, event):
        """move event in line"""
        if self.action == "line":
            self.need_update = True
            self.line.x_end = event.x()
            self.line.y_end = event.y() + CO.CURSOR
            self.picture_in.update()

    def draw_line(self, event):
        """start event in line"""
        if self.action == "line":
            self.resizeEvent(CO.UPDATE)
            self.line.x_start = event.x()
            self.line.y_start = event.y() + CO.CURSOR

    def end_line(self, event):
        """end event in line"""
        if self.action == "line":
            self.line.x_end = event.x()
            self.line.y_end = event.y() + CO.CURSOR
            self.update_image()
            draw = Qt.QPainter(self.picture_in.pixmap())
            self.draw_some(draw)
            draw.end()
            self.picture_in.update()
            self.save_image()
            self.update_image()

    def move_circle(self, event):
        """move event in circle"""
        if self.action == "circle":
            self.need_update = True
            self.circle.x_end = event.x()
            self.circle.y_end = event.y() + CO.CURSOR
            self.picture_in.update()

    def draw_circle(self, event):
        """start event in circle"""
        if self.action == "circle":
            self.resizeEvent(CO.UPDATE)
            self.circle.x_start = event.x()
            self.circle.y_start = event.y() + CO.CURSOR

    def end_circle(self, event):
        """end event in circle"""
        if self.action == "circle":
            self.circle.x_end = event.x()
            self.circle.y_end = event.y() + CO.CURSOR
            self.update_image()
            draw = Qt.QPainter(self.picture_in.pixmap())
            self.draw_some(draw)
            draw.end()
            self.picture_in.update()
            self.save_image()
            self.update_image()

    def draw_some(self, draw):
        """draw all, that can be drawn"""
        draw.setPen(self.set_pen())
        if self.action == "pencil" or self.action == "eraser":
            draw.drawPath(self.path)
        elif self.action == "select":
            draw.setOpacity(CO.OPACITY_AREA)
            draw.setBrush(QtGui.QBrush(QtCore.Qt.blue))
            draw.drawRect(
                self.area.x_start,
                self.area.y_start,
                self.area.x_end - self.area.x_start,
                self.area.y_end - self.area.y_start,
            )
        elif self.action == "line":
            draw.drawLine(
                    self.line.x_start,
                    self.line.y_start,
                    self.line.x_end,
                    self.line.y_end
            )
        elif self.action == "circle":
            leng = lambda x1, y1, x2, y2: sqrt((x1 - x2)**2 + (y1 - y2)**2)
            radius = leng(
                self.circle.x_start, 
                self.circle.y_start, 
                self.circle.x_end,
                self.circle.y_end)
            draw.drawEllipse(
                Qt.QPoint(
                    self.circle.x_start,
                    self.circle.y_start),
                radius,
                radius
            )

    def __settings_block_size_slider(self, new_num):
        """change block size everywhere"""
        self.spin_block_size.setProperty("value", new_num * CO.DOUBLE + CO.BS_START)
        setattr(
            getattr(self.settings, CO.SETTINGS_ATR[CO.BLOCK_SIZE]),
            CO.SETTINGS_PARAM_ATR[CO.VALUE],
            new_num * CO.DOUBLE + CO.BS_START,
        )

    def __settings_block_size_spin(self, new_num):
        """change block size everywhere"""
        self.slider_block_size.setProperty("value", (new_num - CO.BS_START) / CO.DOUBLE)
        setattr(
            getattr(self.settings, CO.SETTINGS_ATR[CO.BLOCK_SIZE]),
            CO.SETTINGS_PARAM_ATR[CO.VALUE],
            new_num,
        )

    def __settings_max_thick(self, new_num):
        """change max thick everywhere"""
        self.slider_max_thick.setProperty("value", new_num)
        self.spin_max_thick.setProperty("value", new_num)
        setattr(
            getattr(self.settings, CO.SETTINGS_ATR[CO.MAX_THICKNESS]),
            CO.SETTINGS_PARAM_ATR[CO.VALUE],
            new_num,
        )

    def __settings_min_line_len(self, new_num):
        """change min line length everywhere"""
        self.slider_min_line_len.setProperty("value", new_num)
        self.spin_min_line_len.setProperty("value", new_num)
        setattr(
            getattr(self.settings, CO.SETTINGS_ATR[CO.MIN_LINE_LENGTH]),
            CO.SETTINGS_PARAM_ATR[CO.VALUE],
            new_num,
        )

    def __settings_min_radius(self, new_num):
        """change min radius everywhere"""
        self.slider_min_radius.setProperty("value", new_num)
        self.spin_min_radius.setProperty("value", new_num)
        setattr(
            getattr(self.settings, CO.SETTINGS_ATR[CO.MIN_RADIUS]),
            CO.SETTINGS_PARAM_ATR[CO.VALUE],
            new_num,
        )

    def __settings_speed_rate_slider(self, new_num):
        """change speed rate spin"""
        self.spin_speed_rate.setProperty("value", new_num / CO.TEN)
        setattr(
            getattr(self.settings, CO.SETTINGS_ATR[CO.SPEED_RATE]),
            CO.SETTINGS_PARAM_ATR[CO.VALUE],
            new_num / CO.TEN,
        )

    def __settings_speed_rate_spin(self, new_num):
        """change speed rate slider"""
        self.slider_speed_rate.setProperty("value", new_num * CO.TEN)
        setattr(
            getattr(self.settings, CO.SETTINGS_ATR[CO.SPEED_RATE]),
            CO.SETTINGS_PARAM_ATR[CO.VALUE],
            new_num,
        )

    def give_atr(self, atr):
        param = getattr(self.settings, CO.SETTINGS_ATR[atr])
        atr_descr = getattr(param, CO.SETTINGS_PARAM_ATR[CO.DESCRIPTION])
        atr_range = getattr(param, CO.SETTINGS_PARAM_ATR[CO.RANGE])
        return atr_descr, atr_range

    def fix_param(self):
        param = getattr(self.settings, CO.SETTINGS_ATR[CO.BLOCK_SIZE])
        atr_value = int(getattr(param, CO.SETTINGS_PARAM_ATR[CO.VALUE]))
        if atr_value % CO.DOUBLE == CO.ZERO:
            atr_value += 1
            self.slider_block_size.setProperty(
                "value", (atr_value - CO.BS_START) / CO.DOUBLE
            )
            self.spin_block_size.setProperty("value", atr_value)
            setattr(
                getattr(self.settings, CO.SETTINGS_ATR[CO.BLOCK_SIZE]),
                CO.SETTINGS_PARAM_ATR[CO.VALUE],
                atr_value,
            )

    def set_settings(self):
        """set init settings"""
        self.slider_block_size.setProperty(
            "value",
            getattr(
                getattr(self.settings, CO.SETTINGS_ATR[CO.BLOCK_SIZE]),
                CO.SETTINGS_PARAM_ATR[CO.VALUE],
            ),
        )
        self.spin_block_size.setProperty(
            "value",
            (
                getattr(
                    getattr(self.settings, CO.SETTINGS_ATR[CO.BLOCK_SIZE]),
                    CO.SETTINGS_PARAM_ATR[CO.VALUE],
                )
                - CO.BS_START
            )
            / CO.DOUBLE,
        )
        self.slider_max_thick.setProperty(
            "value",
            getattr(
                getattr(self.settings, CO.SETTINGS_ATR[CO.MAX_THICKNESS]),
                CO.SETTINGS_PARAM_ATR[CO.VALUE],
            ),
        )
        self.spin_max_thick.setProperty(
            "value",
            getattr(
                getattr(self.settings, CO.SETTINGS_ATR[CO.MAX_THICKNESS]),
                CO.SETTINGS_PARAM_ATR[CO.VALUE],
            ),
        )
        self.slider_min_line_len.setProperty(
            "value",
            getattr(
                getattr(self.settings, CO.SETTINGS_ATR[CO.MIN_LINE_LENGTH]),
                CO.SETTINGS_PARAM_ATR[CO.VALUE],
            ),
        )
        self.spin_min_line_len.setProperty(
            "value",
            getattr(
                getattr(self.settings, CO.SETTINGS_ATR[CO.MIN_LINE_LENGTH]),
                CO.SETTINGS_PARAM_ATR[CO.VALUE],
            ),
        )
        self.slider_min_radius.setProperty(
            "value",
            getattr(
                getattr(self.settings, CO.SETTINGS_ATR[CO.MIN_RADIUS]),
                CO.SETTINGS_PARAM_ATR[CO.VALUE],
            ),
        )
        self.spin_min_radius.setProperty(
            "value",
            getattr(
                getattr(self.settings, CO.SETTINGS_ATR[CO.MIN_RADIUS]),
                CO.SETTINGS_PARAM_ATR[CO.VALUE],
            ),
        )
        self.spin_speed_rate.setProperty(
            "value",
            getattr(
                getattr(self.settings, CO.SETTINGS_ATR[CO.SPEED_RATE]),
                CO.SETTINGS_PARAM_ATR[CO.VALUE],
            ),
        )
        self.slider_speed_rate.setProperty(
            "value",
            getattr(
                getattr(self.settings, CO.SETTINGS_ATR[CO.SPEED_RATE]),
                CO.SETTINGS_PARAM_ATR[CO.VALUE],
            )
            * CO.TEN,
        )

        atr_descr, atr_range = self.give_atr(CO.BLOCK_SIZE)
        self.box_block_size.setToolTip(
            f"Discription: <i>{atr_descr}</i>Range: <i>{atr_range}</i>"
        )
        self.box_block_size.setToolTipDuration(CO.TIME_TIP)

        atr_descr, atr_range = self.give_atr(CO.MAX_THICKNESS)
        self.box_max_thick.setToolTip(
            f"Discription: <i>{atr_descr}</i>Range: <i>{atr_range}</i>"
        )
        self.box_max_thick.setToolTipDuration(CO.TIME_TIP)

        atr_descr, atr_range = self.give_atr(CO.MIN_LINE_LENGTH)
        self.box_min_line_len.setToolTip(
            f"Discription: <i>{atr_descr}</i>Range: <i>{atr_range}</i>"
        )
        self.box_min_line_len.setToolTipDuration(CO.TIME_TIP)

        atr_descr, atr_range = self.give_atr(CO.MIN_RADIUS)
        self.box_min_radius.setToolTip(
            f"Discription: <i>{atr_descr}</i>Range: <i>{atr_range}</i>"
        )
        self.box_min_radius.setToolTipDuration(CO.TIME_TIP)

        atr_descr, atr_range = self.give_atr(CO.SPEED_RATE)
        self.box_speed_rate.setToolTip(
            f"Discription: <i>{atr_descr}</i>Range: <i>{atr_range}</i>"
        )
        self.box_speed_rate.setToolTipDuration(CO.TIME_TIP)


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
