# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'master.ui'
##
## Created by: Qt User Interface Compiler version 6.6.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QLCDNumber, QLabel,
    QLineEdit, QPushButton, QRadioButton, QSizePolicy,
    QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.resize(500, 400)
        Form.setMinimumSize(QSize(500, 400))
        Form.setMaximumSize(QSize(500, 400))
        self.btn1 = QPushButton(Form)
        self.btn1.setObjectName(u"btn1")
        self.btn1.setGeometry(QRect(100, 310, 100, 60))
        self.btn2 = QPushButton(Form)
        self.btn2.setObjectName(u"btn2")
        self.btn2.setGeometry(QRect(300, 310, 100, 60))
        self.btn2.setAutoRepeatInterval(100)
        self.label = QLabel(Form)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(150, 200, 300, 100))
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        font = QFont()
        font.setPointSize(40)
        self.label.setFont(font)
        self.label.setAlignment(Qt.AlignCenter)
        self.label_2 = QLabel(Form)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setEnabled(True)
        self.label_2.setGeometry(QRect(150, 200, 300, 100))
        self.label_2.setFont(font)
        self.label_2.setAutoFillBackground(False)
        self.label_2.setAlignment(Qt.AlignCenter)
        self.lcdNumber = QLCDNumber(Form)
        self.lcdNumber.setObjectName(u"lcdNumber")
        self.lcdNumber.setGeometry(QRect(199, 30, 251, 100))
        self.lcdNumber.setToolTipDuration(-1)
        self.lcdNumber.setSmallDecimalPoint(False)
        self.lcdNumber.setProperty("intValue", 0)
        self.label_3 = QLabel(Form)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(30, 30, 161, 100))
        font1 = QFont()
        font1.setPointSize(26)
        self.label_3.setFont(font1)
        self.label_4 = QLabel(Form)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(60, 210, 85, 80))
        self.label_4.setFocusPolicy(Qt.NoFocus)
        self.label_4.setContextMenuPolicy(Qt.DefaultContextMenu)
        self.label_4.setLayoutDirection(Qt.LeftToRight)
        self.label_4.setAutoFillBackground(False)
        self.label_4.setPixmap(QPixmap(u"img/R.png"))
        self.label_4.setScaledContents(True)
        self.label_5 = QLabel(Form)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(60, 210, 85, 80))
        self.label_5.setPixmap(QPixmap(u"img/G.png"))
        self.label_5.setScaledContents(True)
        self.radioButton = QRadioButton(Form)
        self.radioButton.setObjectName(u"radioButton")
        self.radioButton.setGeometry(QRect(10, 120, 95, 20))
        self.radioButton_2 = QRadioButton(Form)
        self.radioButton_2.setObjectName(u"radioButton_2")
        self.radioButton_2.setGeometry(QRect(10, 150, 95, 20))
        self.lineEdit = QLineEdit(Form)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setGeometry(QRect(70, 150, 81, 20))
        self.comboBox = QComboBox(Form)
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.setObjectName(u"comboBox")
        self.comboBox.setGeometry(QRect(70, 120, 68, 22))
        self.pushButton = QPushButton(Form)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setGeometry(QRect(250, 140, 75, 31))
        self.lineEdit_2 = QLineEdit(Form)
        self.lineEdit_2.setObjectName(u"lineEdit_2")
        self.lineEdit_2.setGeometry(QRect(160, 150, 51, 20))
        self.label_6 = QLabel(Form)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setGeometry(QRect(154, 150, 21, 16))

        self.retranslateUi(Form)
        self.radioButton.pressed.connect(self.lineEdit.hide)
        self.radioButton_2.pressed.connect(self.lineEdit.show)
        self.radioButton.pressed.connect(self.comboBox.show)
        self.radioButton_2.pressed.connect(self.comboBox.hide)
        self.radioButton.pressed.connect(self.label_6.hide)
        self.radioButton.pressed.connect(self.lineEdit_2.hide)
        self.radioButton_2.pressed.connect(self.lineEdit_2.show)
        self.radioButton_2.pressed.connect(self.label_6.show)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"ModbusMaster", None))
        self.btn1.setText(QCoreApplication.translate("Form", u"\u542f\u52a8", None))
        self.btn2.setText(QCoreApplication.translate("Form", u"\u505c\u6b62", None))
        self.label.setText(QCoreApplication.translate("Form", u"Running", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"Stop", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"\u542f\u52a8\u6b21\u6570\uff1a", None))
        self.label_4.setText("")
        self.label_5.setText("")
        self.radioButton.setText(QCoreApplication.translate("Form", u"serial", None))
        self.radioButton_2.setText(QCoreApplication.translate("Form", u"TCP", None))
        self.lineEdit.setText(QCoreApplication.translate("Form", u"127.0.0.1", None))
        self.comboBox.setItemText(0, QCoreApplication.translate("Form", u"com1", None))
        self.comboBox.setItemText(1, QCoreApplication.translate("Form", u"com2", None))
        self.comboBox.setItemText(2, QCoreApplication.translate("Form", u"com3", None))
        self.comboBox.setItemText(3, QCoreApplication.translate("Form", u"com4", None))
        self.comboBox.setItemText(4, QCoreApplication.translate("Form", u"com5", None))
        self.comboBox.setItemText(5, QCoreApplication.translate("Form", u"com6", None))

        self.pushButton.setText(QCoreApplication.translate("Form", u"\u786e\u5b9a", None))
        self.lineEdit_2.setText(QCoreApplication.translate("Form", u"1235", None))
        self.label_6.setText(QCoreApplication.translate("Form", u":", None))
    # retranslateUi

