"""design"""
from PyQt5 import QtCore, QtGui, QtWidgets


class UiMapLap():
    """Main window ui"""
    # pylint: disable=R0902
    # pylint: disable=R0915
    # pylint: disable=W0201
    # without this there is no way

    def setup_ui(self, maplap):
        """initial set up"""
        maplap.setObjectName("maplap")
        maplap.resize(500, 300)
        maplap.setMinimumSize(QtCore.QSize(500, 300))
        maplap.setAutoFillBackground(False)
        maplap.setStyleSheet("background-color: rgb(180, 200, 200);")
        self.central_widget = QtWidgets.QWidget(maplap)
        self.central_widget.setEnabled(True)
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred,
                                            QtWidgets.QSizePolicy.Preferred)
        size_policy.setHorizontalStretch(100)
        size_policy.setVerticalStretch(100)
        size_policy.setHeightForWidth(self.central_widget.sizePolicy().hasHeightForWidth())
        self.central_widget.setSizePolicy(size_policy)
        self.central_widget.setFocusPolicy(QtCore.Qt.NoFocus)
        self.central_widget.setObjectName("central_widget")
        self.grid_layout = QtWidgets.QGridLayout(self.central_widget)
        self.grid_layout.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        self.grid_layout.setObjectName("grid_layout")
        self.panel_settings = QtWidgets.QTabWidget(self.central_widget)
        self.panel_settings.setMinimumSize(QtCore.QSize(140, 0))
        self.panel_settings.setMaximumSize(QtCore.QSize(140, 16777215))
        self.panel_settings.setAutoFillBackground(False)
        self.panel_settings.setObjectName("panel_settings")
        self.panel_tab = QtWidgets.QWidget()
        self.panel_tab.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.panel_tab.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.panel_tab.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.panel_tab.setAutoFillBackground(False)
        self.panel_tab.setObjectName("panel_tab")
        self.vertical_layout_2 = QtWidgets.QVBoxLayout(self.panel_tab)
        self.vertical_layout_2.setObjectName("vertical_layout_2")
        self.painting = QtWidgets.QHBoxLayout()
        self.painting.setObjectName("painting")
        self.pencil = QtWidgets.QPushButton(self.panel_tab)
        self.pencil.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("maplap/templates/pensil.png"), QtGui.QIcon.Normal,
                       QtGui.QIcon.Off)
        self.pencil.setIcon(icon)
        self.pencil.setObjectName("pencil")
        self.painting.addWidget(self.pencil)
        self.eraser = QtWidgets.QPushButton(self.panel_tab)
        self.eraser.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("maplap/templates/eraser.png"), QtGui.QIcon.Normal,
                        QtGui.QIcon.Off)
        self.eraser.setIcon(icon1)
        self.eraser.setObjectName("eraser")
        self.painting.addWidget(self.eraser)
        self.vertical_layout_2.addLayout(self.painting)
        self.cropping = QtWidgets.QPushButton(self.panel_tab)
        self.cropping.setObjectName("cropping")
        self.vertical_layout_2.addWidget(self.cropping)
        self.select_area = QtWidgets.QPushButton(self.panel_tab)
        self.select_area.setObjectName("select_area")
        self.vertical_layout_2.addWidget(self.select_area)
        self.choose_file = QtWidgets.QPushButton(self.panel_tab)
        self.choose_file.setObjectName("choose_file")
        self.vertical_layout_2.addWidget(self.choose_file)
        self.save_tex = QtWidgets.QPushButton(self.panel_tab)
        self.save_tex.setObjectName("save_tex")
        self.vertical_layout_2.addWidget(self.save_tex)
        self.save_pdf = QtWidgets.QPushButton(self.panel_tab)
        self.save_pdf.setObjectName("save_pdf")
        self.vertical_layout_2.addWidget(self.save_pdf)
        self.rotate = QtWidgets.QPushButton(self.panel_tab)
        self.rotate.setObjectName("rotate")
        self.vertical_layout_2.addWidget(self.rotate)
        self.panel_settings.addTab(self.panel_tab, "")
        self.settings_tab = QtWidgets.QWidget()
        self.settings_tab.setObjectName("settings_tab")
        self.vertical_layout_3 = QtWidgets.QVBoxLayout(self.settings_tab)
        self.vertical_layout_3.setObjectName("vertical_layout_3")
        self.plain_text_settings = QtWidgets.QPlainTextEdit(self.settings_tab)
        self.plain_text_settings.setEnabled(True)
        self.plain_text_settings.setObjectName("plain_text_settings")
        self.vertical_layout_3.addWidget(self.plain_text_settings)
        self.panel_settings.addTab(self.settings_tab, "")
        self.grid_layout.addWidget(self.panel_settings, 0, 0, 1, 1)
        self.picture_in = QtWidgets.QLabel(self.central_widget)
        self.picture_in.setText("")
        self.picture_in.setObjectName("picture_in")
        self.grid_layout.addWidget(self.picture_in, 0, 3, 1, 1)
        spacer_item = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding,
                                            QtWidgets.QSizePolicy.Minimum)
        self.grid_layout.addItem(spacer_item, 0, 2, 1, 1)
        spacer_item_1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding,
                                              QtWidgets.QSizePolicy.Minimum)
        self.grid_layout.addItem(spacer_item_1, 0, 8, 1, 1)
        self.line = QtWidgets.QFrame(self.central_widget)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.grid_layout.addWidget(self.line, 0, 1, 1, 1)
        self.line_picture = QtWidgets.QFrame(self.central_widget)
        self.line_picture.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_picture.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_picture.setObjectName("line_picture")
        self.grid_layout.addWidget(self.line_picture, 0, 5, 1, 1)
        self.picture_out = QtWidgets.QLabel(self.central_widget)
        self.picture_out.setText("")
        self.picture_out.setObjectName("picture_out")
        self.grid_layout.addWidget(self.picture_out, 0, 7, 1, 1)
        spacer_item_2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding,
                                              QtWidgets.QSizePolicy.Minimum)
        self.grid_layout.addItem(spacer_item_2, 0, 6, 1, 1)
        spacer_item_3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding,
                                              QtWidgets.QSizePolicy.Minimum)
        self.grid_layout.addItem(spacer_item_3, 0, 4, 1, 1)
        maplap.setCentralWidget(self.central_widget)
        self.retranslate_ui(maplap)
        self.panel_settings.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(maplap)

    def retranslate_ui(self, maplap):
        """init some"""
        _translate = QtCore.QCoreApplication.translate
        maplap.setWindowTitle(_translate("maplap", "maplap"))
        self.cropping.setText(_translate("maplap", "cropping"))
        self.select_area.setText(_translate("maplap", "select area"))
        self.choose_file.setText(_translate("maplap", "choose file"))
        self.save_tex.setText(_translate("maplap", "save tex"))
        self.save_pdf.setText(_translate("maplap", "save pdf"))
        self.rotate.setText(_translate("maplap", "rotate"))
        self.panel_settings.setTabText(self.panel_settings.indexOf(self.panel_tab),
                                       _translate("maplap", "panel"))
        self.plain_text_settings.setPlainText(
            _translate("maplap", "Здесь будут размещены необходимые значения для алгоритма"))
        self.panel_settings.setTabText(self.panel_settings.indexOf(self.settings_tab),
                                       _translate("maplap", "settings"))

    def none_for_pylint(self):
        """do nothing"""
        self.none_for_pylint()
