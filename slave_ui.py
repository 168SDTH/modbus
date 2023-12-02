# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'slave.ui'
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
from PySide6.QtWidgets import (QApplication, QLCDNumber, QLabel, QSizePolicy,
    QWidget)

class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName(u"Form")
        Form.setWindowModality(Qt.WindowModal)
        Form.setEnabled(True)
        Form.resize(500, 300)
        Form.setMinimumSize(QSize(500, 300))
        Form.setMaximumSize(QSize(500, 300))
        font = QFont()
        font.setPointSize(24)
        Form.setFont(font)
        self.lcdNumber = QLCDNumber(Form)
        self.lcdNumber.setObjectName(u"lcdNumber")
        self.lcdNumber.setGeometry(QRect(200, 30, 250, 100))
        self.lcdNumber.setToolTipDuration(-1)
        self.lcdNumber.setSmallDecimalPoint(False)
        self.lcdNumber.setProperty("intValue", 0)
        self.label = QLabel(Form)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(30, 30, 161, 100))
        font1 = QFont()
        font1.setPointSize(26)
        self.label.setFont(font1)
        self.label_2 = QLabel(Form)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setEnabled(True)
        self.label_2.setGeometry(QRect(150, 150, 300, 100))
        font2 = QFont()
        font2.setPointSize(40)
        self.label_2.setFont(font2)
        self.label_2.setAutoFillBackground(False)
        self.label_2.setAlignment(Qt.AlignCenter)
        self.label_3 = QLabel(Form)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(150, 150, 300, 100))
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setFont(font2)
        self.label_3.setAlignment(Qt.AlignCenter)
        self.label_4 = QLabel(Form)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(60, 160, 85, 80))
        self.label_4.setFocusPolicy(Qt.NoFocus)
        self.label_4.setContextMenuPolicy(Qt.DefaultContextMenu)
        self.label_4.setLayoutDirection(Qt.LeftToRight)
        self.label_4.setAutoFillBackground(False)
        self.label_4.setPixmap(QPixmap(u"img/R.png"))
        self.label_4.setScaledContents(True)
        self.label_5 = QLabel(Form)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(60, 160, 85, 80))
        self.label_5.setPixmap(QPixmap(u"img/G.png"))
        self.label_5.setScaledContents(True)

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)
    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", u"ModbusSlave", None))
        self.label.setText(QCoreApplication.translate("Form", u"\u542f\u52a8\u6b21\u6570\uff1a", None))
        self.label_2.setText(QCoreApplication.translate("Form", u"Stop", None))
        self.label_3.setText(QCoreApplication.translate("Form", u"Running", None))
        self.label_4.setText("")
        self.label_5.setText("")
    # retranslateUi

