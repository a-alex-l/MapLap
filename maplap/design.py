from PyQt5 import QtCore, QtGui, QtWidgets

import constant as C


class UiMapLap:
    """Main window ui"""

    # pylint: disable=R0902
    # pylint: disable=C0103
    # snake_case
    # pylint: disable=R0915
    # pylint: disable=W0201
    # without this there is no way
    def setupUi(self, MapLap, screen_w, screen_h):
        """initial set up"""
        MapLap.setObjectName("MapLap")
        MapLap.resize(500, 300)
        MapLap.setMinimumSize(QtCore.QSize(500, 300))
        MapLap.setMaximumSize(QtCore.QSize(screen_w, screen_h))
        MapLap.setAutoFillBackground(False)
        MapLap.setStyleSheet("background-color: rgb(180, 200, 200);")
        self.central_widget = QtWidgets.QWidget(MapLap)
        self.central_widget.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred
        )
        sizePolicy.setHorizontalStretch(100)
        sizePolicy.setVerticalStretch(100)
        sizePolicy.setHeightForWidth(self.central_widget.sizePolicy().hasHeightForWidth())
        self.central_widget.setSizePolicy(sizePolicy)
        self.central_widget.setMaximumSize(QtCore.QSize(screen_w, screen_h))
        self.central_widget.setFocusPolicy(QtCore.Qt.NoFocus)
        self.central_widget.setObjectName("central_widget")
        self.gridLayout = QtWidgets.QGridLayout(self.central_widget)
        self.gridLayout.setSizeConstraint(QtWidgets.QLayout.SetMaximumSize)
        self.gridLayout.setObjectName("gridLayout")
        self.picture_in = QtWidgets.QLabel(self.central_widget)
        self.picture_in.setText("")
        self.picture_in.setObjectName("picture_in")
        self.gridLayout.addWidget(self.picture_in, 0, 3, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        self.gridLayout.addItem(spacerItem, 0, 8, 1, 1)
        self.line = QtWidgets.QFrame(self.central_widget)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.gridLayout.addWidget(self.line, 0, 1, 1, 1)
        self.line_picture = QtWidgets.QFrame(self.central_widget)
        self.line_picture.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_picture.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_picture.setObjectName("line_picture")
        self.gridLayout.addWidget(self.line_picture, 0, 5, 1, 1)
        self.picture_out = QtWidgets.QLabel(self.central_widget)
        self.picture_out.setText("")
        self.picture_out.setObjectName("picture_out")
        self.gridLayout.addWidget(self.picture_out, 0, 7, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        self.gridLayout.addItem(spacerItem1, 0, 6, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        self.gridLayout.addItem(spacerItem2, 0, 4, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum
        )
        self.gridLayout.addItem(spacerItem3, 0, 2, 1, 1)
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
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.panel_tab)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.painting = QtWidgets.QHBoxLayout()
        self.painting.setObjectName("painting")
        self.pencil = QtWidgets.QPushButton(self.panel_tab)
        self.pencil.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(C.PENSIL), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pencil.setIcon(icon)
        self.pencil.setObjectName("pencil")
        self.painting.addWidget(self.pencil)
        self.eraser = QtWidgets.QPushButton(self.panel_tab)
        self.eraser.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(C.ERASER), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.eraser.setIcon(icon1)
        self.eraser.setObjectName("eraser")
        self.painting.addWidget(self.eraser)
        self.verticalLayout_2.addLayout(self.painting)
        self.cropping = QtWidgets.QPushButton(self.panel_tab)
        self.cropping.setObjectName("cropping")
        self.verticalLayout_2.addWidget(self.cropping)
        self.select_area = QtWidgets.QPushButton(self.panel_tab)
        self.select_area.setObjectName("select_area")
        self.verticalLayout_2.addWidget(self.select_area)
        self.choose_file = QtWidgets.QPushButton(self.panel_tab)
        self.choose_file.setObjectName("choose_file")
        self.verticalLayout_2.addWidget(self.choose_file)
        self.save_tex = QtWidgets.QPushButton(self.panel_tab)
        self.save_tex.setObjectName("save_tex")
        self.verticalLayout_2.addWidget(self.save_tex)
        self.save_pdf = QtWidgets.QPushButton(self.panel_tab)
        self.save_pdf.setObjectName("save_pdf")
        self.verticalLayout_2.addWidget(self.save_pdf)
        self.rotate = QtWidgets.QPushButton(self.panel_tab)
        self.rotate.setObjectName("rotate")
        self.verticalLayout_2.addWidget(self.rotate)
        self.panel_settings.addTab(self.panel_tab, "")
        self.settings_tab = QtWidgets.QWidget()
        self.settings_tab.setStyleSheet("palette")
        self.settings_tab.setObjectName("settings_tab")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.settings_tab)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.box_block_size = QtWidgets.QGroupBox(self.settings_tab)
        self.box_block_size.setEnabled(True)
        self.box_block_size.setMouseTracking(False)
        self.box_block_size.setStyleSheet(
            "border: 1px solid black; border-radius: 5px; margin-top: 10px;"
        )
        self.box_block_size.setFlat(False)
        self.box_block_size.setCheckable(False)
        self.box_block_size.setObjectName("box_block_size")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.box_block_size)
        self.horizontalLayout_6.setContentsMargins(3, 12, 3, -1)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.spin_block_size = QtWidgets.QSpinBox(self.box_block_size)
        self.spin_block_size.setMinimumSize(QtCore.QSize(30, 15))
        self.spin_block_size.setMaximumSize(QtCore.QSize(30, 15))
        self.spin_block_size.setStyleSheet("border-color: green; margin-top: 0px;")
        self.spin_block_size.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.spin_block_size.setKeyboardTracking(True)
        self.spin_block_size.setMinimum(11)
        self.spin_block_size.setMaximum(501)
        self.spin_block_size.setSingleStep(1)
        self.spin_block_size.setDisplayIntegerBase(10)
        self.spin_block_size.setObjectName("spin_block_size")
        self.horizontalLayout_6.addWidget(self.spin_block_size)
        self.slider_block_size = QtWidgets.QSlider(self.box_block_size)
        self.slider_block_size.setMinimumSize(QtCore.QSize(0, 15))
        self.slider_block_size.setMaximumSize(QtCore.QSize(16777215, 15))
        self.slider_block_size.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.slider_block_size.setMouseTracking(False)
        self.slider_block_size.setStyleSheet("border: 0px;")
        self.slider_block_size.setMinimum(11)
        self.slider_block_size.setMaximum(501)
        self.slider_block_size.setPageStep(5)
        self.slider_block_size.setOrientation(QtCore.Qt.Horizontal)
        self.slider_block_size.setInvertedAppearance(False)
        self.slider_block_size.setInvertedControls(False)
        self.slider_block_size.setObjectName("slider_block_size")
        self.horizontalLayout_6.addWidget(self.slider_block_size)
        self.verticalLayout_3.addWidget(self.box_block_size)
        self.box_min_line_len = QtWidgets.QGroupBox(self.settings_tab)
        self.box_min_line_len.setEnabled(True)
        self.box_min_line_len.setStyleSheet(
            "border: 1px solid black; border-radius: 5px; margin-top: 10px;"
        )
        self.box_min_line_len.setFlat(False)
        self.box_min_line_len.setCheckable(False)
        self.box_min_line_len.setObjectName("box_min_line_len")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.box_min_line_len)
        self.horizontalLayout_4.setContentsMargins(3, 12, 3, -1)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.spin_min_line_len = QtWidgets.QSpinBox(self.box_min_line_len)
        self.spin_min_line_len.setMinimumSize(QtCore.QSize(30, 15))
        self.spin_min_line_len.setMaximumSize(QtCore.QSize(30, 15))
        self.spin_min_line_len.setStyleSheet("border-color: green; margin-top: 0px;")
        self.spin_min_line_len.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.spin_min_line_len.setKeyboardTracking(True)
        self.spin_min_line_len.setMinimum(1)
        self.spin_min_line_len.setMaximum(150)
        self.spin_min_line_len.setSingleStep(1)
        self.spin_min_line_len.setDisplayIntegerBase(10)
        self.spin_min_line_len.setObjectName("spin_min_line_len")
        self.horizontalLayout_4.addWidget(self.spin_min_line_len)
        self.slider_min_line_len = QtWidgets.QSlider(self.box_min_line_len)
        self.slider_min_line_len.setMinimumSize(QtCore.QSize(0, 15))
        self.slider_min_line_len.setMaximumSize(QtCore.QSize(16777215, 15))
        self.slider_min_line_len.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.slider_min_line_len.setMouseTracking(False)
        self.slider_min_line_len.setStyleSheet("border: 0px;")
        self.slider_min_line_len.setMinimum(1)
        self.slider_min_line_len.setMaximum(150)
        self.slider_min_line_len.setPageStep(2)
        self.slider_min_line_len.setOrientation(QtCore.Qt.Horizontal)
        self.slider_min_line_len.setObjectName("slider_min_line_len")
        self.horizontalLayout_4.addWidget(self.slider_min_line_len)
        self.verticalLayout_3.addWidget(self.box_min_line_len)
        self.box_max_thick = QtWidgets.QGroupBox(self.settings_tab)
        self.box_max_thick.setEnabled(True)
        self.box_max_thick.setStyleSheet(
            "border: 1px solid black; border-radius: 5px; margin-top: 10px;"
        )
        self.box_max_thick.setFlat(False)
        self.box_max_thick.setCheckable(False)
        self.box_max_thick.setObjectName("box_max_thick")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.box_max_thick)
        self.horizontalLayout_3.setContentsMargins(3, 12, 3, -1)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.spin_max_thick = QtWidgets.QSpinBox(self.box_max_thick)
        self.spin_max_thick.setMinimumSize(QtCore.QSize(30, 15))
        self.spin_max_thick.setMaximumSize(QtCore.QSize(30, 15))
        self.spin_max_thick.setStyleSheet("border-color: green; margin-top: 0px;")
        self.spin_max_thick.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.spin_max_thick.setKeyboardTracking(True)
        self.spin_max_thick.setMinimum(5)
        self.spin_max_thick.setMaximum(50)
        self.spin_max_thick.setSingleStep(1)
        self.spin_max_thick.setDisplayIntegerBase(10)
        self.spin_max_thick.setObjectName("spin_max_thick")
        self.horizontalLayout_3.addWidget(self.spin_max_thick)
        self.slider_max_thick = QtWidgets.QSlider(self.box_max_thick)
        self.slider_max_thick.setMinimumSize(QtCore.QSize(0, 15))
        self.slider_max_thick.setMaximumSize(QtCore.QSize(16777215, 15))
        self.slider_max_thick.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.slider_max_thick.setMouseTracking(False)
        self.slider_max_thick.setStyleSheet("border: 0px;")
        self.slider_max_thick.setMinimum(5)
        self.slider_max_thick.setMaximum(50)
        self.slider_max_thick.setPageStep(1)
        self.slider_max_thick.setOrientation(QtCore.Qt.Horizontal)
        self.slider_max_thick.setObjectName("slider_max_thick")
        self.horizontalLayout_3.addWidget(self.slider_max_thick)
        self.verticalLayout_3.addWidget(self.box_max_thick)
        self.box_speed_rate = QtWidgets.QGroupBox(self.settings_tab)
        self.box_speed_rate.setEnabled(True)
        self.box_speed_rate.setStyleSheet(
            "border: 1px solid black; border-radius: 5px; margin-top: 10px;"
        )
        self.box_speed_rate.setFlat(False)
        self.box_speed_rate.setCheckable(False)
        self.box_speed_rate.setObjectName("box_speed_rate")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.box_speed_rate)
        self.horizontalLayout_2.setContentsMargins(3, 12, 3, -1)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.spin_speed_rate = QtWidgets.QDoubleSpinBox(self.box_speed_rate)
        self.spin_speed_rate.setMinimumSize(QtCore.QSize(30, 15))
        self.spin_speed_rate.setMaximumSize(QtCore.QSize(30, 15))
        self.spin_speed_rate.setStyleSheet("border-color: green; margin-top: 0px;")
        self.spin_speed_rate.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.spin_speed_rate.setDecimals(1)
        self.spin_speed_rate.setMinimum(1.0)
        self.spin_speed_rate.setMaximum(10.0)
        self.spin_speed_rate.setSingleStep(0.1)
        self.spin_speed_rate.setObjectName("spin_speed_rate")
        self.horizontalLayout_2.addWidget(self.spin_speed_rate)
        self.slider_speed_rate = QtWidgets.QSlider(self.box_speed_rate)
        self.slider_speed_rate.setMinimumSize(QtCore.QSize(0, 15))
        self.slider_speed_rate.setMaximumSize(QtCore.QSize(16777215, 15))
        self.slider_speed_rate.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.slider_speed_rate.setMouseTracking(False)
        self.slider_speed_rate.setStyleSheet("border: 0px;")
        self.slider_speed_rate.setMinimum(10)
        self.slider_speed_rate.setMaximum(100)
        self.slider_speed_rate.setSingleStep(1)
        self.slider_speed_rate.setPageStep(1)
        self.slider_speed_rate.setOrientation(QtCore.Qt.Horizontal)
        self.slider_speed_rate.setObjectName("slider_speed_rate")
        self.horizontalLayout_2.addWidget(self.slider_speed_rate)
        self.verticalLayout_3.addWidget(self.box_speed_rate)
        self.box_min_radius = QtWidgets.QGroupBox(self.settings_tab)
        self.box_min_radius.setEnabled(True)
        self.box_min_radius.setStyleSheet(
            "border: 1px solid black; border-radius: 5px; margin-top: 10px;"
        )
        self.box_min_radius.setFlat(False)
        self.box_min_radius.setCheckable(False)
        self.box_min_radius.setObjectName("box_min_radius")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.box_min_radius)
        self.horizontalLayout.setContentsMargins(3, 12, 3, -1)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.spin_min_radius = QtWidgets.QSpinBox(self.box_min_radius)
        self.spin_min_radius.setMinimumSize(QtCore.QSize(30, 15))
        self.spin_min_radius.setMaximumSize(QtCore.QSize(30, 15))
        self.spin_min_radius.setStyleSheet("border-color: green; margin-top: 0px;")
        self.spin_min_radius.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.spin_min_radius.setKeyboardTracking(True)
        self.spin_min_radius.setMinimum(3)
        self.spin_min_radius.setMaximum(100)
        self.spin_min_radius.setSingleStep(1)
        self.spin_min_radius.setDisplayIntegerBase(10)
        self.spin_min_radius.setObjectName("spin_min_radius")
        self.horizontalLayout.addWidget(self.spin_min_radius)
        self.slider_min_radius = QtWidgets.QSlider(self.box_min_radius)
        self.slider_min_radius.setMinimumSize(QtCore.QSize(0, 15))
        self.slider_min_radius.setMaximumSize(QtCore.QSize(16777215, 15))
        self.slider_min_radius.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.slider_min_radius.setMouseTracking(False)
        self.slider_min_radius.setStyleSheet("border: 0px;")
        self.slider_min_radius.setMinimum(3)
        self.slider_min_radius.setMaximum(100)
        self.slider_min_radius.setSingleStep(1)
        self.slider_min_radius.setPageStep(1)
        self.slider_min_radius.setOrientation(QtCore.Qt.Horizontal)
        self.slider_min_radius.setObjectName("slider_min_radius")
        self.horizontalLayout.addWidget(self.slider_min_radius)
        self.verticalLayout_3.addWidget(self.box_min_radius)
        self.panel_settings.addTab(self.settings_tab, "")
        self.gridLayout.addWidget(self.panel_settings, 0, 0, 1, 1)
        MapLap.setCentralWidget(self.central_widget)
        self.retranslateUi(MapLap)
        self.panel_settings.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MapLap)

    def retranslateUi(self, MapLap):
        """init some"""
        _translate = QtCore.QCoreApplication.translate
        MapLap.setWindowTitle(_translate("MapLap", "MapLap"))
        self.cropping.setText(_translate("MapLap", "cropping"))
        self.select_area.setText(_translate("MapLap", "select area"))
        self.choose_file.setText(_translate("MapLap", "choose file"))
        self.save_tex.setText(_translate("MapLap", "save tex"))
        self.save_pdf.setText(_translate("MapLap", "save pdf"))
        self.rotate.setText(_translate("MapLap", "rotate"))
        self.panel_settings.setTabText(
            self.panel_settings.indexOf(self.panel_tab), _translate("MapLap", "panel")
        )
        self.box_block_size.setTitle(_translate("MapLap", "&Block size"))
        self.box_min_line_len.setTitle(_translate("MapLap", "&Min line length"))
        self.box_max_thick.setTitle(_translate("MapLap", "&Max thickness"))
        self.box_speed_rate.setTitle(_translate("MapLap", "&Speed rate"))
        self.box_min_radius.setTitle(_translate("MapLap", "&Min radius"))
        self.panel_settings.setTabText(
            self.panel_settings.indexOf(self.settings_tab), _translate("MapLap", "settings")
        )
