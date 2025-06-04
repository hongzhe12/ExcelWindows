# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'general_excel.ui'
##
## Created by: Qt User Interface Compiler version 6.9.0
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
from PySide6.QtWidgets import (QApplication, QGridLayout, QHeaderView, QMainWindow,
    QMenuBar, QPushButton, QSizePolicy, QStatusBar,
    QTableWidget, QTableWidgetItem, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(571, 560)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.gridLayout = QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.tableWidget = QTableWidget(self.centralwidget)
        self.tableWidget.setObjectName(u"tableWidget")
        self.tableWidget.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.tableWidget.setStyleSheet(u"/* \u57fa\u7840\u8868\u683c\u6837\u5f0f */\n"
"        QTableWidget {\n"
"            gridline-color: #cccccc;\n"
"            selection-background-color: rgba(173, 216, 230, 150);\n"
"            selection-color: black;\n"
"        }\n"
"\n"
"        \n"
"        /* \u8868\u5934\u6837\u5f0f */\n"
"        QHeaderView::section {\n"
"            background-color: #f0f0f0;\n"
"            border: 1px solid #cccccc;\n"
"            padding: 4px;\n"
"            font-weight: bold;\n"
"        }\n"
"\n"
"        /* \u9009\u4e2d\u5355\u5143\u683c\u6837\u5f0f */\n"
"        QTableWidget::item:selected {\n"
"           background-color: rgba(173, 216, 230, 150);\n"
"            color: black;\n"
"        }\n"
"        \n"
"        /* \u9f20\u6807\u60ac\u505c\u6837\u5f0f */\n"
"        QTableWidget::item:hover {\n"
"            background-color: rgba(220, 230, 241, 100);\n"
"        }")

        self.gridLayout.addWidget(self.tableWidget, 0, 0, 1, 2)

        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setMinimumSize(QSize(0, 30))

        self.gridLayout.addWidget(self.pushButton, 1, 0, 1, 1)

        self.compare = QPushButton(self.centralwidget)
        self.compare.setObjectName(u"compare")
        self.compare.setMinimumSize(QSize(0, 30))

        self.gridLayout.addWidget(self.compare, 1, 1, 1, 1)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 571, 33))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"\u5199\u5165\u6570\u636e\u5e93", None))
        self.compare.setText(QCoreApplication.translate("MainWindow", u"\u5339\u914d", None))
    # retranslateUi

