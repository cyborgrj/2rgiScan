# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
##
## Created by: Qt User Interface Compiler version 6.10.2
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
from PySide6.QtWidgets import (QApplication, QComboBox, QDateEdit, QFrame,
    QGroupBox, QHeaderView, QLabel, QLineEdit,
    QMainWindow, QPushButton, QSizePolicy, QStatusBar,
    QTabWidget, QTableWidget, QTableWidgetItem, QWidget)
import resources_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(892, 587)
        MainWindow.setMinimumSize(QSize(892, 587))
        MainWindow.setMaximumSize(QSize(892, 587))
        MainWindow.setStyleSheet(u"background-color: rgb(250, 250, 250);\n"
"\n"
"color: rgb(42, 42, 42);\n"
"\n"
"\n"
"\n"
"QStatusBar{\n"
"\n"
"color: rgb(42, 42, 42);\n"
"\n"
"   \n"
"\n"
"font: 75 10pt \"MS Shell Dlg 2\";\n"
"\n"
"}")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setStyleSheet(u"background-color: rgb(42, 42, 42);\n"
"\n"
"color: rgb(245, 245, 245);")
        self.frame = QFrame(self.centralwidget)
        self.frame.setObjectName(u"frame")
        self.frame.setGeometry(QRect(0, 0, 1091, 559))
        self.frame.setStyleSheet(u"font: 14pt \"MS Shell Dlg 2\";")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.tabWidget = QTabWidget(self.frame)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setGeometry(QRect(-2, 0, 1101, 571))
        self.tabWidget.setAutoFillBackground(False)
        self.tabWidget.setStyleSheet(u"color: rgb(42, 42, 42);\n"
"\n"
"background-color: rgb(245, 245,245);")
        self.tabWidget.setTabPosition(QTabWidget.North)
        self.tabWidget.setTabShape(QTabWidget.Rounded)
        self.tabWidget.setElideMode(Qt.ElideLeft)
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.tab.setStyleSheet(u"QLabel{\n"
"\n"
"background-color: transparent;\n"
"\n"
"}\n"
"\n"
"\n"
"\n"
"QWidget\n"
"\n"
"{\n"
"\n"
"background-color: rgb(42, 42, 42);\n"
"\n"
"color: rgb(245, 245, 245);\n"
"\n"
"}\n"
"\n"
"\n"
"\n"
"QPushButton\n"
"\n"
"{\n"
"\n"
" background-color:rgb(60,60,60);\n"
"\n"
" color:rgb(242,242,242);\n"
"\n"
" border-radius:10px;\n"
"\n"
"}\n"
"\n"
"\n"
"\n"
"QPushButton:Hover\n"
"\n"
"{\n"
"\n"
" background-color:rgb(142,142,142);\n"
"\n"
" border-radius:10px;\n"
"\n"
" color:rgb(42, 42, 42);\n"
"\n"
" border-bottom:2px solid grey;\n"
"\n"
" border-right:2px solid grey;\n"
"\n"
"}\n"
"\n"
"\n"
"\n"
"QPushButton:Pressed\n"
"\n"
"{\n"
"\n"
" color:rgb(242,242,242);\n"
"\n"
" border-radius:10px;\n"
"\n"
" background-color:rgb(42, 42, 42);\n"
"\n"
" border:2px solid grey;\n"
"\n"
" padding: 5px;\n"
"\n"
" font: 75 13pt \"MS Shell Dlg 2\";\n"
"\n"
"}\n"
"\n"
"\n"
"\n"
"QComboBox{\n"
"\n"
"border: 2px solid white;\n"
"\n"
"color: rgb(248, 248, 242);\n"
"\n"
"padding: 10px;\n"
"\n"
"border-radius: 5px\n"
"\n"
"}"
                        "\n"
"\n"
"\n"
"\n"
"QComboBox:drop-down {\n"
"\n"
"border: 0px\n"
"\n"
"}\n"
"\n"
"\n"
"\n"
"QComboBox:down-arrow {\n"
"\n"
"image: url(:/icons/icons/chevron-down.svg);\n"
"\n"
"margin-right:10\n"
"\n"
"}\n"
"\n"
"\n"
"\n"
"QComboBox:on {\n"
"\n"
"border: 2px solid rgb(248, 248, 242);\n"
"\n"
"}\n"
"\n"
"\n"
"\n"
"QComboBox QListView {\n"
"\n"
"border: 2px solid white;\n"
"\n"
"color: rgb(248, 248, 242);\n"
"\n"
"padding: 10px;\n"
"\n"
"border-radius: 5px\n"
"\n"
"}\n"
"\n"
"\n"
"\n"
"QComboBox QListView:item{\n"
"\n"
"padding-left: 10px;\n"
"\n"
"background-color: rgb(40, 42, 54);\n"
"\n"
"}\n"
"\n"
"\n"
"\n"
"QComboBox QListView:item:hover{\n"
"\n"
"background-color: rgb(29, 30, 40);\n"
"\n"
"}\n"
"\n"
"\n"
"\n"
"QComboBox QListView:item:selected{\n"
"\n"
"background-color: rgb(29, 30, 40);\n"
"\n"
"}")
        self.setTrabalhoCB = QComboBox(self.tab)
        self.setTrabalhoCB.addItem("")
        self.setTrabalhoCB.addItem("")
        self.setTrabalhoCB.addItem("")
        self.setTrabalhoCB.addItem("")
        self.setTrabalhoCB.addItem("")
        self.setTrabalhoCB.addItem("")
        self.setTrabalhoCB.setObjectName(u"setTrabalhoCB")
        self.setTrabalhoCB.setGeometry(QRect(280, 150, 341, 41))
        self.setTrabalhoCB.setStyleSheet(u"")
        self.lblTrabalho = QLabel(self.tab)
        self.lblTrabalho.setObjectName(u"lblTrabalho")
        self.lblTrabalho.setGeometry(QRect(20, 90, 871, 31))
        self.lblTrabalho.setStyleSheet(u"background-color: transparent;")
        self.lblTrabalho.setAlignment(Qt.AlignCenter)
        self.lblDocumento = QLabel(self.tab)
        self.lblDocumento.setObjectName(u"lblDocumento")
        self.lblDocumento.setGeometry(QRect(280, 260, 181, 41))
        self.lblDocumento.setStyleSheet(u"background-color: transparent;")
        self.campoNumDocumento = QLineEdit(self.tab)
        self.campoNumDocumento.setObjectName(u"campoNumDocumento")
        self.campoNumDocumento.setGeometry(QRect(470, 260, 101, 41))
        self.campoNumDocumento.setStyleSheet(u"background-color: rgb(42, 42, 42);\n"
"\n"
"color: rgb(245, 245, 245);")
        self.campoNumDocumento.setMaxLength(6)
        self.campoNumDocumento.setAlignment(Qt.AlignCenter)
        self.buttonGravar = QPushButton(self.tab)
        self.buttonGravar.setObjectName(u"buttonGravar")
        self.buttonGravar.setGeometry(QRect(210, 450, 251, 51))
        icon = QIcon()
        icon.addFile(u":/images/cil-save.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.buttonGravar.setIcon(icon)
        self.buttonDigitalizar = QPushButton(self.tab)
        self.buttonDigitalizar.setObjectName(u"buttonDigitalizar")
        self.buttonDigitalizar.setGeometry(QRect(30, 450, 161, 51))
        icon1 = QIcon()
        icon1.addFile(u":/images/cil-print.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.buttonDigitalizar.setIcon(icon1)
        self.buttonLimpar = QPushButton(self.tab)
        self.buttonLimpar.setObjectName(u"buttonLimpar")
        self.buttonLimpar.setGeometry(QRect(710, 450, 151, 51))
        icon2 = QIcon()
        icon2.addFile(u":/icons/icons/x-octagon.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.buttonLimpar.setIcon(icon2)
        self.lblAnoCertidao = QLabel(self.tab)
        self.lblAnoCertidao.setObjectName(u"lblAnoCertidao")
        self.lblAnoCertidao.setGeometry(QRect(190, 260, 141, 41))
        self.lblAnoCertidao.setStyleSheet(u"background-color: transparent;")
        self.campoNumAnoCertidao = QLineEdit(self.tab)
        self.campoNumAnoCertidao.setObjectName(u"campoNumAnoCertidao")
        self.campoNumAnoCertidao.setGeometry(QRect(340, 260, 51, 41))
        self.campoNumAnoCertidao.setStyleSheet(u"background-color: rgb(42, 42, 42);\n"
"\n"
"color: rgb(245, 245, 245);")
        self.campoNumAnoCertidao.setMaxLength(2)
        self.campoNumAnoCertidao.setAlignment(Qt.AlignCenter)
        self.campoNumCertidao = QLineEdit(self.tab)
        self.campoNumCertidao.setObjectName(u"campoNumCertidao")
        self.campoNumCertidao.setGeometry(QRect(560, 260, 101, 41))
        self.campoNumCertidao.setStyleSheet(u"background-color: rgb(42, 42, 42);\n"
"\n"
"color: rgb(245, 245, 245);")
        self.campoNumCertidao.setMaxLength(6)
        self.campoNumCertidao.setAlignment(Qt.AlignCenter)
        self.lblNumCertidao = QLabel(self.tab)
        self.lblNumCertidao.setObjectName(u"lblNumCertidao")
        self.lblNumCertidao.setGeometry(QRect(410, 260, 141, 41))
        self.lblNumCertidao.setStyleSheet(u"background-color: transparent;")
        self.forma_8 = QLabel(self.tab)
        self.forma_8.setObjectName(u"forma_8")
        self.forma_8.setGeometry(QRect(410, -109, 501, 411))
        self.forma_8.setStyleSheet(u"font: 57 500pt \"Marlett\";\n"
"\n"
"color: rgba(248, 248, 248, 3);\n"
"\n"
"background: transparent;")
        self.forma_5 = QLabel(self.tab)
        self.forma_5.setObjectName(u"forma_5")
        self.forma_5.setGeometry(QRect(-60, 9, 611, 521))
        self.forma_5.setStyleSheet(u"font: 700pt \"Wingdings 3\";\n"
"\n"
"color: rgba(248, 248, 248, 10);\n"
"\n"
"background: transparent;\n"
"\n"
"")
        self.forma_6 = QLabel(self.tab)
        self.forma_6.setObjectName(u"forma_6")
        self.forma_6.setGeometry(QRect(20, 59, 971, 541))
        self.forma_6.setStyleSheet(u"font: 57 300pt \"Marlett\";\n"
"\n"
"color: rgba(248, 248, 248, 3);\n"
"\n"
"background:transparent;")
        self.forma_7 = QLabel(self.tab)
        self.forma_7.setObjectName(u"forma_7")
        self.forma_7.setGeometry(QRect(400, -13, 671, 541))
        self.forma_7.setStyleSheet(u"font: 600pt \"Wingdings 3\";\n"
"\n"
"color: rgba(248, 248, 248, 10);\n"
"\n"
"background: transparent;\n"
"\n"
"")
        self.label = QLabel(self.tab)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(0, 0, 891, 51))
        self.label.setStyleSheet(u"font: 75 18pt \"MS Shell Dlg 2\";\n"
"\n"
"text-decoration: underline;")
        self.label.setAlignment(Qt.AlignCenter)
        self.buttonAumentar = QPushButton(self.tab)
        self.buttonAumentar.setObjectName(u"buttonAumentar")
        self.buttonAumentar.setGeometry(QRect(540, 320, 31, 28))
        self.buttonDiminuir = QPushButton(self.tab)
        self.buttonDiminuir.setObjectName(u"buttonDiminuir")
        self.buttonDiminuir.setGeometry(QRect(280, 320, 31, 28))
        self.buttonVerificar = QPushButton(self.tab)
        self.buttonVerificar.setObjectName(u"buttonVerificar")
        self.buttonVerificar.setGeometry(QRect(540, 450, 151, 51))
        icon3 = QIcon()
        icon3.addFile(u":/icons/icons/search.svg", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.buttonVerificar.setIcon(icon3)
        self.buttonConsultarDocumento = QPushButton(self.tab)
        self.buttonConsultarDocumento.setObjectName(u"buttonConsultarDocumento")
        self.buttonConsultarDocumento.setGeometry(QRect(440, 450, 251, 51))
        self.buttonConsultarDocumento.setIcon(icon3)
        self.buttonConferenciaErro = QPushButton(self.tab)
        self.buttonConferenciaErro.setObjectName(u"buttonConferenciaErro")
        self.buttonConferenciaErro.setGeometry(QRect(360, 320, 131, 31))
        self.tabWidget.addTab(self.tab, "")
        self.forma_8.raise_()
        self.forma_7.raise_()
        self.forma_6.raise_()
        self.forma_5.raise_()
        self.setTrabalhoCB.raise_()
        self.lblTrabalho.raise_()
        self.lblDocumento.raise_()
        self.campoNumDocumento.raise_()
        self.buttonGravar.raise_()
        self.buttonDigitalizar.raise_()
        self.buttonLimpar.raise_()
        self.lblAnoCertidao.raise_()
        self.campoNumAnoCertidao.raise_()
        self.campoNumCertidao.raise_()
        self.lblNumCertidao.raise_()
        self.label.raise_()
        self.buttonAumentar.raise_()
        self.buttonDiminuir.raise_()
        self.buttonVerificar.raise_()
        self.buttonConsultarDocumento.raise_()
        self.buttonConferenciaErro.raise_()
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.tab_2.setStyleSheet(u"QLabel{\n"
"\n"
"background-color: transparent;\n"
"\n"
"}\n"
"\n"
"\n"
"\n"
"QWidget\n"
"\n"
"{\n"
"\n"
"background-color: rgb(42, 42, 42);\n"
"\n"
"color: rgb(245, 245, 245);\n"
"\n"
"}\n"
"\n"
"\n"
"\n"
"QPushButton\n"
"\n"
"{\n"
"\n"
" background-color:rgb(60,60,60);\n"
"\n"
" color:rgb(242,242,242);\n"
"\n"
" border-radius:10px;\n"
"\n"
"}\n"
"\n"
"\n"
"\n"
"QPushButton:Hover\n"
"\n"
"{\n"
"\n"
" background-color:rgb(142,142,142);\n"
"\n"
" border-radius:10px;\n"
"\n"
" color:rgb(42, 42, 42);\n"
"\n"
" border-bottom:2px solid grey;\n"
"\n"
" border-right:2px solid grey;\n"
"\n"
"}\n"
"\n"
"\n"
"\n"
"QPushButton:Pressed\n"
"\n"
"{\n"
"\n"
" color:rgb(242,242,242);\n"
"\n"
" border-radius:10px;\n"
"\n"
" background-color:rgb(42, 42, 42);\n"
"\n"
" border:2px solid grey;\n"
"\n"
" padding: 5px;\n"
"\n"
" font: 75 13pt \"MS Shell Dlg 2\";\n"
"\n"
"}\n"
"\n"
"\n"
"\n"
"QComboBox{\n"
"\n"
"border: 2px solid white;\n"
"\n"
"color: rgb(248, 248, 242);\n"
"\n"
"padding: 10px;\n"
"\n"
"border-radius: 5px\n"
"\n"
"}"
                        "\n"
"\n"
"\n"
"\n"
"QComboBox:drop-down {\n"
"\n"
"border: 0px\n"
"\n"
"}\n"
"\n"
"\n"
"\n"
"QComboBox:down-arrow {\n"
"\n"
"image: url(:/icons/icons/chevron-down.svg);\n"
"\n"
"margin-right:10\n"
"\n"
"}\n"
"\n"
"\n"
"\n"
"QComboBox:on {\n"
"\n"
"border: 2px solid rgb(248, 248, 242);\n"
"\n"
"}\n"
"\n"
"\n"
"\n"
"QComboBox QListView {\n"
"\n"
"border: 2px solid white;\n"
"\n"
"color: rgb(248, 248, 242);\n"
"\n"
"padding: 10px;\n"
"\n"
"border-radius: 5px\n"
"\n"
"}\n"
"\n"
"\n"
"\n"
"QComboBox QListView:item{\n"
"\n"
"padding-left: 10px;\n"
"\n"
"background-color: rgb(40, 42, 54);\n"
"\n"
"}\n"
"\n"
"\n"
"\n"
"QComboBox QListView:item:hover{\n"
"\n"
"background-color: rgb(29, 30, 40);\n"
"\n"
"}\n"
"\n"
"\n"
"\n"
"QComboBox QListView:item:selected{\n"
"\n"
"background-color: rgb(29, 30, 40);\n"
"\n"
"}")
        self.labelDigitalizacaoDocumentosSimples = QLabel(self.tab_2)
        self.labelDigitalizacaoDocumentosSimples.setObjectName(u"labelDigitalizacaoDocumentosSimples")
        self.labelDigitalizacaoDocumentosSimples.setGeometry(QRect(0, 0, 891, 51))
        self.labelDigitalizacaoDocumentosSimples.setStyleSheet(u"font: 75 18pt \"MS Shell Dlg 2\";\n"
"\n"
"text-decoration: underline;")
        self.labelDigitalizacaoDocumentosSimples.setAlignment(Qt.AlignCenter)
        self.lblTrabalhoDocumentosSimples = QLabel(self.tab_2)
        self.lblTrabalhoDocumentosSimples.setObjectName(u"lblTrabalhoDocumentosSimples")
        self.lblTrabalhoDocumentosSimples.setGeometry(QRect(10, 70, 871, 31))
        self.lblTrabalhoDocumentosSimples.setStyleSheet(u"background-color: transparent;")
        self.lblTrabalhoDocumentosSimples.setAlignment(Qt.AlignCenter)
        self.comboBoxTipoSimples = QComboBox(self.tab_2)
        self.comboBoxTipoSimples.setObjectName(u"comboBoxTipoSimples")
        self.comboBoxTipoSimples.setGeometry(QRect(270, 130, 341, 41))
        self.comboBoxTipoSimples.setStyleSheet(u"")
        self.buttonGravarDocumentosSimples = QPushButton(self.tab_2)
        self.buttonGravarDocumentosSimples.setObjectName(u"buttonGravarDocumentosSimples")
        self.buttonGravarDocumentosSimples.setGeometry(QRect(330, 430, 251, 51))
        self.buttonGravarDocumentosSimples.setIcon(icon)
        self.buttonLimparDocumentosSimples = QPushButton(self.tab_2)
        self.buttonLimparDocumentosSimples.setObjectName(u"buttonLimparDocumentosSimples")
        self.buttonLimparDocumentosSimples.setGeometry(QRect(620, 430, 151, 51))
        self.buttonLimparDocumentosSimples.setIcon(icon2)
        self.buttonDigitalizarDocumentosSimples = QPushButton(self.tab_2)
        self.buttonDigitalizarDocumentosSimples.setObjectName(u"buttonDigitalizarDocumentosSimples")
        self.buttonDigitalizarDocumentosSimples.setGeometry(QRect(130, 430, 161, 51))
        self.buttonDigitalizarDocumentosSimples.setIcon(icon1)
        self.dateEditDataSimples = QDateEdit(self.tab_2)
        self.dateEditDataSimples.setObjectName(u"dateEditDataSimples")
        self.dateEditDataSimples.setGeometry(QRect(370, 210, 151, 41))
        font = QFont()
        font.setFamilies([u"MS Shell Dlg 2"])
        font.setPointSize(14)
        font.setBold(False)
        font.setItalic(False)
        self.dateEditDataSimples.setFont(font)
        self.lineEditNumeroDocumento = QLineEdit(self.tab_2)
        self.lineEditNumeroDocumento.setObjectName(u"lineEditNumeroDocumento")
        self.lineEditNumeroDocumento.setGeometry(QRect(370, 300, 401, 41))
        self.lineEditNumeroDocumento.setStyleSheet(u"background-color: rgb(42, 42, 42);\n"
"\n"
"color: rgb(245, 245, 245);")
        self.lineEditNumeroDocumento.setMaxLength(60)
        self.lineEditNumeroDocumento.setAlignment(Qt.AlignCenter)
        self.labelNumeroDocumentoSimples = QLabel(self.tab_2)
        self.labelNumeroDocumentoSimples.setObjectName(u"labelNumeroDocumentoSimples")
        self.labelNumeroDocumentoSimples.setGeometry(QRect(130, 300, 241, 41))
        self.labelNumeroDocumentoSimples.setStyleSheet(u"background-color: transparent;")
        self.buttonDocumentInfo = QPushButton(self.tab_2)
        self.buttonDocumentInfo.setObjectName(u"buttonDocumentInfo")
        self.buttonDocumentInfo.setGeometry(QRect(620, 140, 31, 28))
        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QWidget()
        self.tab_3.setObjectName(u"tab_3")
        self.tab_3.setStyleSheet(u"QLabel{\n"
"\n"
"background-color: transparent;\n"
"\n"
"}\n"
"\n"
"\n"
"\n"
"QWidget\n"
"\n"
"{\n"
"\n"
"background-color: rgb(42, 42, 42);\n"
"\n"
"color: rgb(245, 245, 245);\n"
"\n"
"}\n"
"\n"
"\n"
"\n"
"QPushButton\n"
"\n"
"{\n"
"\n"
" background-color:rgb(60,60,60);\n"
"\n"
" color:rgb(242,242,242);\n"
"\n"
" border-radius:10px;\n"
"\n"
"}\n"
"\n"
"\n"
"\n"
"QPushButton:Hover\n"
"\n"
"{\n"
"\n"
" background-color:rgb(142,142,142);\n"
"\n"
" border-radius:10px;\n"
"\n"
" color:rgb(42, 42, 42);\n"
"\n"
" border-bottom:2px solid grey;\n"
"\n"
" border-right:2px solid grey;\n"
"\n"
"}\n"
"\n"
"\n"
"\n"
"QPushButton:Pressed\n"
"\n"
"{\n"
"\n"
" color:rgb(242,242,242);\n"
"\n"
" border-radius:10px;\n"
"\n"
" background-color:rgb(42, 42, 42);\n"
"\n"
" border:2px solid grey;\n"
"\n"
" padding: 5px;\n"
"\n"
" font: 75 13pt \"MS Shell Dlg 2\";\n"
"\n"
"}\n"
"\n"
"\n"
"\n"
"QComboBox{\n"
"\n"
"border: 2px solid white;\n"
"\n"
"color: rgb(248, 248, 242);\n"
"\n"
"padding: 10px;\n"
"\n"
"border-radius: 5px\n"
"\n"
"}"
                        "\n"
"\n"
"\n"
"\n"
"QComboBox:drop-down {\n"
"\n"
"border: 0px\n"
"\n"
"}\n"
"\n"
"\n"
"\n"
"QComboBox:down-arrow {\n"
"\n"
"image: url(:/icons/icons/chevron-down.svg);\n"
"\n"
"margin-right:10\n"
"\n"
"}\n"
"\n"
"\n"
"\n"
"QComboBox:on {\n"
"\n"
"border: 2px solid rgb(248, 248, 242);\n"
"\n"
"}\n"
"\n"
"\n"
"\n"
"QComboBox QListView {\n"
"\n"
"border: 2px solid white;\n"
"\n"
"color: rgb(248, 248, 242);\n"
"\n"
"padding: 10px;\n"
"\n"
"border-radius: 5px\n"
"\n"
"}\n"
"\n"
"\n"
"\n"
"QComboBox QListView:item{\n"
"\n"
"padding-left: 10px;\n"
"\n"
"background-color: rgb(40, 42, 54);\n"
"\n"
"}\n"
"\n"
"\n"
"\n"
"QComboBox QListView:item:hover{\n"
"\n"
"background-color: rgb(29, 30, 40);\n"
"\n"
"}\n"
"\n"
"\n"
"\n"
"QComboBox QListView:item:selected{\n"
"\n"
"background-color: rgb(29, 30, 40);\n"
"\n"
"}")
        self.label_conferencia = QLabel(self.tab_3)
        self.label_conferencia.setObjectName(u"label_conferencia")
        self.label_conferencia.setGeometry(QRect(0, 0, 891, 51))
        self.label_conferencia.setStyleSheet(u"font: 75 18pt \"MS Shell Dlg 2\";\n"
"\n"
"text-decoration: underline;")
        self.label_conferencia.setAlignment(Qt.AlignCenter)
        self.tabela_dinamica_conf = QTableWidget(self.tab_3)
        self.tabela_dinamica_conf.setObjectName(u"tabela_dinamica_conf")
        self.tabela_dinamica_conf.setGeometry(QRect(10, 60, 871, 421))
        self.button_listar_conf = QPushButton(self.tab_3)
        self.button_listar_conf.setObjectName(u"button_listar_conf")
        self.button_listar_conf.setGeometry(QRect(30, 490, 131, 31))
        self.tabWidget.addTab(self.tab_3, "")
        self.tab_4 = QWidget()
        self.tab_4.setObjectName(u"tab_4")
        self.tab_4.setStyleSheet(u"QLabel{\n"
"\n"
"background-color: transparent;\n"
"\n"
"}\n"
"\n"
"\n"
"\n"
"QWidget\n"
"\n"
"{\n"
"\n"
"background-color: rgb(42, 42, 42);\n"
"\n"
"color: rgb(245, 245, 245);\n"
"\n"
"}\n"
"\n"
"\n"
"\n"
"QPushButton\n"
"\n"
"{\n"
"\n"
" background-color:rgb(60,60,60);\n"
"\n"
" color:rgb(242,242,242);\n"
"\n"
" border-radius:10px;\n"
"\n"
"}\n"
"\n"
"\n"
"\n"
"QPushButton:Hover\n"
"\n"
"{\n"
"\n"
" background-color:rgb(142,142,142);\n"
"\n"
" border-radius:10px;\n"
"\n"
" color:rgb(42, 42, 42);\n"
"\n"
" border-bottom:2px solid grey;\n"
"\n"
" border-right:2px solid grey;\n"
"\n"
"}\n"
"\n"
"\n"
"\n"
"QPushButton:Pressed\n"
"\n"
"{\n"
"\n"
" color:rgb(242,242,242);\n"
"\n"
" border-radius:10px;\n"
"\n"
" background-color:rgb(42, 42, 42);\n"
"\n"
" border:2px solid grey;\n"
"\n"
" padding: 5px;\n"
"\n"
" font: 75 13pt \"MS Shell Dlg 2\";\n"
"\n"
"}\n"
"\n"
"\n"
"\n"
"QComboBox{\n"
"\n"
"border: 2px solid white;\n"
"\n"
"color: rgb(248, 248, 242);\n"
"\n"
"padding: 10px;\n"
"\n"
"border-radius: 5px\n"
"\n"
"}"
                        "\n"
"\n"
"\n"
"\n"
"QComboBox:drop-down {\n"
"\n"
"border: 0px\n"
"\n"
"}\n"
"\n"
"\n"
"\n"
"QComboBox:down-arrow {\n"
"\n"
"image: url(:/icons/icons/chevron-down.svg);\n"
"\n"
"margin-right:10\n"
"\n"
"}\n"
"\n"
"\n"
"\n"
"QComboBox:on {\n"
"\n"
"border: 2px solid rgb(248, 248, 242);\n"
"\n"
"}\n"
"\n"
"\n"
"\n"
"QComboBox QListView {\n"
"\n"
"border: 2px solid white;\n"
"\n"
"color: rgb(248, 248, 242);\n"
"\n"
"padding: 10px;\n"
"\n"
"border-radius: 5px\n"
"\n"
"}\n"
"\n"
"\n"
"\n"
"QComboBox QListView:item{\n"
"\n"
"padding-left: 10px;\n"
"\n"
"background-color: rgb(40, 42, 54);\n"
"\n"
"}\n"
"\n"
"\n"
"\n"
"QComboBox QListView:item:hover{\n"
"\n"
"background-color: rgb(29, 30, 40);\n"
"\n"
"}\n"
"\n"
"\n"
"\n"
"QComboBox QListView:item:selected{\n"
"\n"
"background-color: rgb(29, 30, 40);\n"
"\n"
"}")
        self.label_4 = QLabel(self.tab_4)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(0, 0, 891, 51))
        self.label_4.setStyleSheet(u"font: 75 18pt \"MS Shell Dlg 2\";\n"
"\n"
"text-decoration: underline;")
        self.label_4.setAlignment(Qt.AlignCenter)
        self.groupBox = QGroupBox(self.tab_4)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(QRect(10, 60, 881, 81))
        self.comboBoxFiltro = QComboBox(self.groupBox)
        self.comboBoxFiltro.setObjectName(u"comboBoxFiltro")
        self.comboBoxFiltro.setGeometry(QRect(10, 30, 141, 41))
        self.comboBoxDinamica = QComboBox(self.groupBox)
        self.comboBoxDinamica.setObjectName(u"comboBoxDinamica")
        self.comboBoxDinamica.setGeometry(QRect(170, 30, 221, 41))
        self.lineEditAnoCert = QLineEdit(self.groupBox)
        self.lineEditAnoCert.setObjectName(u"lineEditAnoCert")
        self.lineEditAnoCert.setGeometry(QRect(410, 40, 51, 31))
        self.lineEditAnoCert.setStyleSheet(u"")
        self.lineEditAnoCert.setMaxLength(2)
        self.lineEditNumCert = QLineEdit(self.groupBox)
        self.lineEditNumCert.setObjectName(u"lineEditNumCert")
        self.lineEditNumCert.setGeometry(QRect(470, 40, 91, 31))
        self.lineEditNumCert.setMaxLength(6)
        self.dateEditInicio = QDateEdit(self.groupBox)
        self.dateEditInicio.setObjectName(u"dateEditInicio")
        self.dateEditInicio.setGeometry(QRect(570, 39, 141, 31))
        self.label_final = QLabel(self.groupBox)
        self.label_final.setObjectName(u"label_final")
        self.label_final.setGeometry(QRect(570, 17, 141, 21))
        self.label_final.setAlignment(Qt.AlignCenter)
        self.label_7 = QLabel(self.groupBox)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setGeometry(QRect(730, 17, 141, 21))
        self.label_7.setAlignment(Qt.AlignCenter)
        self.dateEditFinal = QDateEdit(self.groupBox)
        self.dateEditFinal.setObjectName(u"dateEditFinal")
        self.dateEditFinal.setGeometry(QRect(730, 40, 141, 31))
        self.lineEditNumDocumento = QLineEdit(self.groupBox)
        self.lineEditNumDocumento.setObjectName(u"lineEditNumDocumento")
        self.lineEditNumDocumento.setGeometry(QRect(410, 40, 151, 31))
        self.lineEditNumDocumento.setMaxLength(6)
        self.label_certidao = QLabel(self.groupBox)
        self.label_certidao.setObjectName(u"label_certidao")
        self.label_certidao.setGeometry(QRect(410, 20, 151, 21))
        self.label_certidao.setAlignment(Qt.AlignCenter)
        self.label_documento = QLabel(self.groupBox)
        self.label_documento.setObjectName(u"label_documento")
        self.label_documento.setGeometry(QRect(410, 20, 151, 21))
        self.label_documento.setAlignment(Qt.AlignCenter)
        self.label_final.raise_()
        self.comboBoxFiltro.raise_()
        self.comboBoxDinamica.raise_()
        self.lineEditAnoCert.raise_()
        self.lineEditNumCert.raise_()
        self.dateEditInicio.raise_()
        self.label_7.raise_()
        self.dateEditFinal.raise_()
        self.lineEditNumDocumento.raise_()
        self.label_certidao.raise_()
        self.label_documento.raise_()
        self.tableWidget = QTableWidget(self.tab_4)
        self.tableWidget.setObjectName(u"tableWidget")
        self.tableWidget.setGeometry(QRect(10, 150, 881, 331))
        self.buttonListar = QPushButton(self.tab_4)
        self.buttonListar.setObjectName(u"buttonListar")
        self.buttonListar.setGeometry(QRect(30, 490, 131, 31))
        self.buttonCancelar = QPushButton(self.tab_4)
        self.buttonCancelar.setObjectName(u"buttonCancelar")
        self.buttonCancelar.setGeometry(QRect(180, 490, 131, 31))
        self.buttonImprimir = QPushButton(self.tab_4)
        self.buttonImprimir.setObjectName(u"buttonImprimir")
        self.buttonImprimir.setGeometry(QRect(590, 490, 131, 31))
        self.buttonSalvar = QPushButton(self.tab_4)
        self.buttonSalvar.setObjectName(u"buttonSalvar")
        self.buttonSalvar.setGeometry(QRect(740, 490, 131, 31))
        self.filtro_listar_documentos = QComboBox(self.tab_4)
        self.filtro_listar_documentos.addItem("")
        self.filtro_listar_documentos.addItem("")
        self.filtro_listar_documentos.addItem("")
        self.filtro_listar_documentos.setObjectName(u"filtro_listar_documentos")
        self.filtro_listar_documentos.setGeometry(QRect(730, 20, 141, 41))
        self.label_listar_documentos = QLabel(self.tab_4)
        self.label_listar_documentos.setObjectName(u"label_listar_documentos")
        self.label_listar_documentos.setGeometry(QRect(569, 20, 161, 41))
        self.tabWidget.addTab(self.tab_4, "")
        self.tab_5 = QWidget()
        self.tab_5.setObjectName(u"tab_5")
        self.tab_5.setStyleSheet(u"QLabel{\n"
"\n"
"background-color: transparent;\n"
"\n"
"}\n"
"\n"
"\n"
"\n"
"Line{\n"
"\n"
"color: rgb(255, 255, 255);\n"
"\n"
"}\n"
"\n"
"\n"
"\n"
"QWidget\n"
"\n"
"{\n"
"\n"
"background-color: rgb(42, 42, 42);\n"
"\n"
"color: rgb(245, 245, 245);\n"
"\n"
"}\n"
"\n"
"\n"
"\n"
"QPushButton\n"
"\n"
"{\n"
"\n"
" background-color:rgb(60,60,60);\n"
"\n"
" color:rgb(242,242,242);\n"
"\n"
" border-radius:10px;\n"
"\n"
"}\n"
"\n"
"\n"
"\n"
"QPushButton:Hover\n"
"\n"
"{\n"
"\n"
" background-color:rgb(142,142,142);\n"
"\n"
" border-radius:10px;\n"
"\n"
" color:rgb(42, 42, 42);\n"
"\n"
" border-bottom:2px solid grey;\n"
"\n"
" border-right:2px solid grey;\n"
"\n"
"}\n"
"\n"
"\n"
"\n"
"QPushButton:Pressed\n"
"\n"
"{\n"
"\n"
" color:rgb(242,242,242);\n"
"\n"
" border-radius:10px;\n"
"\n"
" background-color:rgb(42, 42, 42);\n"
"\n"
" border:2px solid grey;\n"
"\n"
" padding: 5px;\n"
"\n"
" font: 75 13pt \"MS Shell Dlg 2\";\n"
"\n"
"}\n"
"\n"
"\n"
"\n"
"QComboBox{\n"
"\n"
"border: 2px solid white;\n"
"\n"
"color: rgb(248, 2"
                        "48, 242);\n"
"\n"
"padding: 10px;\n"
"\n"
"border-radius: 5px\n"
"\n"
"}\n"
"\n"
"\n"
"\n"
"QComboBox:drop-down {\n"
"\n"
"border: 0px\n"
"\n"
"}\n"
"\n"
"\n"
"\n"
"QComboBox:down-arrow {\n"
"\n"
"image: url(:/icons/icons/chevron-down.svg);\n"
"\n"
"margin-right:10\n"
"\n"
"}\n"
"\n"
"\n"
"\n"
"QComboBox:on {\n"
"\n"
"border: 2px solid rgb(248, 248, 242);\n"
"\n"
"}\n"
"\n"
"\n"
"\n"
"QComboBox QListView {\n"
"\n"
"border: 2px solid white;\n"
"\n"
"color: rgb(248, 248, 242);\n"
"\n"
"padding: 10px;\n"
"\n"
"border-radius: 5px\n"
"\n"
"}\n"
"\n"
"\n"
"\n"
"QComboBox QListView:item{\n"
"\n"
"padding-left: 10px;\n"
"\n"
"background-color: rgb(40, 42, 54);\n"
"\n"
"}\n"
"\n"
"\n"
"\n"
"QComboBox QListView:item:hover{\n"
"\n"
"background-color: rgb(29, 30, 40);\n"
"\n"
"}\n"
"\n"
"\n"
"\n"
"QComboBox QListView:item:selected{\n"
"\n"
"background-color: rgb(29, 30, 40);\n"
"\n"
"}")
        self.label_5 = QLabel(self.tab_5)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(0, 0, 891, 51))
        self.label_5.setStyleSheet(u"font: 75 18pt \"MS Shell Dlg 2\";\n"
"\n"
"text-decoration: underline;")
        self.label_5.setAlignment(Qt.AlignCenter)
        self.config_gerais = QFrame(self.tab_5)
        self.config_gerais.setObjectName(u"config_gerais")
        self.config_gerais.setGeometry(QRect(9, 56, 425, 468))
        self.config_gerais.setInputMethodHints(Qt.ImhNone)
        self.config_gerais.setFrameShape(QFrame.StyledPanel)
        self.config_gerais.setFrameShadow(QFrame.Raised)
        self.Configuracoes_Gerais = QLabel(self.config_gerais)
        self.Configuracoes_Gerais.setObjectName(u"Configuracoes_Gerais")
        self.Configuracoes_Gerais.setGeometry(QRect(0, 0, 421, 41))
        self.Configuracoes_Gerais.setAlignment(Qt.AlignCenter)
        self.label_temp_index = QLabel(self.config_gerais)
        self.label_temp_index.setObjectName(u"label_temp_index")
        self.label_temp_index.setGeometry(QRect(10, 50, 171, 41))
        self.campo_temp_index = QLineEdit(self.config_gerais)
        self.campo_temp_index.setObjectName(u"campo_temp_index")
        self.campo_temp_index.setGeometry(QRect(190, 57, 191, 31))
        self.label_servidor = QLabel(self.config_gerais)
        self.label_servidor.setObjectName(u"label_servidor")
        self.label_servidor.setGeometry(QRect(10, 123, 81, 41))
        self.campo_servidor = QLineEdit(self.config_gerais)
        self.campo_servidor.setObjectName(u"campo_servidor")
        self.campo_servidor.setGeometry(QRect(100, 130, 281, 31))
        self.button_salvar_config = QPushButton(self.config_gerais)
        self.button_salvar_config.setObjectName(u"button_salvar_config")
        self.button_salvar_config.setGeometry(QRect(30, 420, 151, 31))
        self.button_cancelar_config = QPushButton(self.config_gerais)
        self.button_cancelar_config.setObjectName(u"button_cancelar_config")
        self.button_cancelar_config.setGeometry(QRect(240, 420, 151, 31))
        self.campo_caminho_naps2 = QLineEdit(self.config_gerais)
        self.campo_caminho_naps2.setObjectName(u"campo_caminho_naps2")
        self.campo_caminho_naps2.setGeometry(QRect(20, 230, 381, 31))
        self.label_caminho_naps2 = QLabel(self.config_gerais)
        self.label_caminho_naps2.setObjectName(u"label_caminho_naps2")
        self.label_caminho_naps2.setGeometry(QRect(20, 180, 381, 41))
        self.label_caminho_naps2.setAlignment(Qt.AlignCenter)
        self.button_testar_email = QPushButton(self.config_gerais)
        self.button_testar_email.setObjectName(u"button_testar_email")
        self.button_testar_email.setGeometry(QRect(130, 320, 151, 31))
        self.atualiza_usuario = QFrame(self.tab_5)
        self.atualiza_usuario.setObjectName(u"atualiza_usuario")
        self.atualiza_usuario.setGeometry(QRect(443, 56, 445, 468))
        self.atualiza_usuario.setInputMethodHints(Qt.ImhUppercaseOnly)
        self.atualiza_usuario.setFrameShape(QFrame.StyledPanel)
        self.atualiza_usuario.setFrameShadow(QFrame.Raised)
        self.label_3 = QLabel(self.atualiza_usuario)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(-10, 0, 451, 41))
        self.label_3.setAlignment(Qt.AlignCenter)
        self.label_sigla = QLabel(self.atualiza_usuario)
        self.label_sigla.setObjectName(u"label_sigla")
        self.label_sigla.setGeometry(QRect(20, 50, 151, 41))
        self.campo_sigla = QLineEdit(self.atualiza_usuario)
        self.campo_sigla.setObjectName(u"campo_sigla")
        self.campo_sigla.setGeometry(QRect(170, 56, 81, 31))
        self.campo_sigla.setInputMethodHints(Qt.ImhUppercaseOnly)
        self.campo_sigla.setMaxLength(3)
        self.campo_sigla.setClearButtonEnabled(True)
        self.button_verificar_sigla = QPushButton(self.atualiza_usuario)
        self.button_verificar_sigla.setObjectName(u"button_verificar_sigla")
        self.button_verificar_sigla.setGeometry(QRect(290, 56, 111, 31))
        self.label_sigla_2 = QLabel(self.atualiza_usuario)
        self.label_sigla_2.setObjectName(u"label_sigla_2")
        self.label_sigla_2.setGeometry(QRect(20, 100, 151, 41))
        self.campo_nome_usuario = QLineEdit(self.atualiza_usuario)
        self.campo_nome_usuario.setObjectName(u"campo_nome_usuario")
        self.campo_nome_usuario.setGeometry(QRect(20, 140, 401, 31))
        self.campo_nome_usuario.setInputMethodHints(Qt.ImhNone)
        self.label_sigla_3 = QLabel(self.atualiza_usuario)
        self.label_sigla_3.setObjectName(u"label_sigla_3")
        self.label_sigla_3.setGeometry(QRect(20, 180, 171, 41))
        self.combo_acesso_usuario = QComboBox(self.atualiza_usuario)
        self.combo_acesso_usuario.addItem("")
        self.combo_acesso_usuario.addItem("")
        self.combo_acesso_usuario.addItem("")
        self.combo_acesso_usuario.addItem("")
        self.combo_acesso_usuario.addItem("")
        self.combo_acesso_usuario.setObjectName(u"combo_acesso_usuario")
        self.combo_acesso_usuario.setGeometry(QRect(20, 220, 271, 51))
        self.label_sigla_4 = QLabel(self.atualiza_usuario)
        self.label_sigla_4.setObjectName(u"label_sigla_4")
        self.label_sigla_4.setGeometry(QRect(10, 300, 161, 41))
        self.label_sigla_4.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.label_sigla_5 = QLabel(self.atualiza_usuario)
        self.label_sigla_5.setObjectName(u"label_sigla_5")
        self.label_sigla_5.setGeometry(QRect(20, 350, 151, 41))
        self.label_sigla_5.setAlignment(Qt.AlignRight|Qt.AlignTrailing|Qt.AlignVCenter)
        self.campo_senha_usuario = QLineEdit(self.atualiza_usuario)
        self.campo_senha_usuario.setObjectName(u"campo_senha_usuario")
        self.campo_senha_usuario.setGeometry(QRect(180, 310, 241, 31))
        self.campo_senha_usuario.setEchoMode(QLineEdit.Password)
        self.campo_confirma_senha = QLineEdit(self.atualiza_usuario)
        self.campo_confirma_senha.setObjectName(u"campo_confirma_senha")
        self.campo_confirma_senha.setGeometry(QRect(180, 360, 241, 31))
        self.campo_confirma_senha.setEchoMode(QLineEdit.Password)
        self.button_criar_atualizar = QPushButton(self.atualiza_usuario)
        self.button_criar_atualizar.setObjectName(u"button_criar_atualizar")
        self.button_criar_atualizar.setGeometry(QRect(30, 420, 151, 31))
        self.button_cancelar_usuario = QPushButton(self.atualiza_usuario)
        self.button_cancelar_usuario.setObjectName(u"button_cancelar_usuario")
        self.button_cancelar_usuario.setGeometry(QRect(260, 420, 151, 31))
        self.label_6 = QLabel(self.tab_5)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setGeometry(QRect(6, 53, 431, 481))
        self.label_6.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.label_8 = QLabel(self.tab_5)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setGeometry(QRect(440, 53, 451, 481))
        self.label_8.setStyleSheet(u"background-color: rgb(255, 255, 255);")
        self.tabWidget.addTab(self.tab_5, "")
        self.label_8.raise_()
        self.label_6.raise_()
        self.label_5.raise_()
        self.config_gerais.raise_()
        self.atualiza_usuario.raise_()
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        self.statusbar.setSizeGripEnabled(False)
        MainWindow.setStatusBar(self.statusbar)
        QWidget.setTabOrder(self.setTrabalhoCB, self.campoNumAnoCertidao)
        QWidget.setTabOrder(self.campoNumAnoCertidao, self.campoNumDocumento)
        QWidget.setTabOrder(self.campoNumDocumento, self.campoNumCertidao)
        QWidget.setTabOrder(self.campoNumCertidao, self.buttonDiminuir)
        QWidget.setTabOrder(self.buttonDiminuir, self.buttonAumentar)
        QWidget.setTabOrder(self.buttonAumentar, self.buttonDigitalizar)
        QWidget.setTabOrder(self.buttonDigitalizar, self.buttonGravar)
        QWidget.setTabOrder(self.buttonGravar, self.buttonVerificar)
        QWidget.setTabOrder(self.buttonVerificar, self.buttonLimpar)
        QWidget.setTabOrder(self.buttonLimpar, self.tabela_dinamica_conf)
        QWidget.setTabOrder(self.tabela_dinamica_conf, self.button_listar_conf)
        QWidget.setTabOrder(self.button_listar_conf, self.filtro_listar_documentos)
        QWidget.setTabOrder(self.filtro_listar_documentos, self.comboBoxFiltro)
        QWidget.setTabOrder(self.comboBoxFiltro, self.comboBoxDinamica)
        QWidget.setTabOrder(self.comboBoxDinamica, self.lineEditNumDocumento)
        QWidget.setTabOrder(self.lineEditNumDocumento, self.lineEditNumCert)
        QWidget.setTabOrder(self.lineEditNumCert, self.dateEditInicio)
        QWidget.setTabOrder(self.dateEditInicio, self.dateEditFinal)
        QWidget.setTabOrder(self.dateEditFinal, self.tableWidget)
        QWidget.setTabOrder(self.tableWidget, self.buttonListar)
        QWidget.setTabOrder(self.buttonListar, self.buttonCancelar)
        QWidget.setTabOrder(self.buttonCancelar, self.buttonImprimir)
        QWidget.setTabOrder(self.buttonImprimir, self.buttonSalvar)
        QWidget.setTabOrder(self.buttonSalvar, self.campo_temp_index)
        QWidget.setTabOrder(self.campo_temp_index, self.campo_servidor)
        QWidget.setTabOrder(self.campo_servidor, self.campo_caminho_naps2)
        QWidget.setTabOrder(self.campo_caminho_naps2, self.button_testar_email)
        QWidget.setTabOrder(self.button_testar_email, self.button_salvar_config)
        QWidget.setTabOrder(self.button_salvar_config, self.button_cancelar_config)
        QWidget.setTabOrder(self.button_cancelar_config, self.campo_sigla)
        QWidget.setTabOrder(self.campo_sigla, self.button_verificar_sigla)
        QWidget.setTabOrder(self.button_verificar_sigla, self.campo_nome_usuario)
        QWidget.setTabOrder(self.campo_nome_usuario, self.combo_acesso_usuario)
        QWidget.setTabOrder(self.combo_acesso_usuario, self.campo_senha_usuario)
        QWidget.setTabOrder(self.campo_senha_usuario, self.campo_confirma_senha)
        QWidget.setTabOrder(self.campo_confirma_senha, self.button_criar_atualizar)
        QWidget.setTabOrder(self.button_criar_atualizar, self.button_cancelar_usuario)
        QWidget.setTabOrder(self.button_cancelar_usuario, self.tabWidget)
        QWidget.setTabOrder(self.tabWidget, self.lineEditAnoCert)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.setTrabalhoCB.setItemText(0, QCoreApplication.translate("MainWindow", u"1 - MATR\u00cdCULA", None))
        self.setTrabalhoCB.setItemText(1, QCoreApplication.translate("MainWindow", u"2 - PROTOCOLO", None))
        self.setTrabalhoCB.setItemText(2, QCoreApplication.translate("MainWindow", u"3 - CERTID\u00c3O", None))
        self.setTrabalhoCB.setItemText(3, QCoreApplication.translate("MainWindow", u"4 - REGISTRO AUXILIAR", None))
        self.setTrabalhoCB.setItemText(4, QCoreApplication.translate("MainWindow", u"5 - CERTID\u00c3O CANCELADA", None))
        self.setTrabalhoCB.setItemText(5, QCoreApplication.translate("MainWindow", u"6 - PROTOCOLO CANCELADO", None))

        self.lblTrabalho.setText(QCoreApplication.translate("MainWindow", u"TRABALHO ATUAL:", None))
        self.lblDocumento.setText(QCoreApplication.translate("MainWindow", u"N\u00ba DO DOCUMENTO:", None))
        self.buttonGravar.setText(QCoreApplication.translate("MainWindow", u"  Gravar na SERVCOM", None))
        self.buttonDigitalizar.setText(QCoreApplication.translate("MainWindow", u"  Digitalizar", None))
        self.buttonLimpar.setText(QCoreApplication.translate("MainWindow", u"  Cancelar", None))
        self.lblAnoCertidao.setText(QCoreApplication.translate("MainWindow", u"ANO CERTID\u00c3O:", None))
        self.lblNumCertidao.setText(QCoreApplication.translate("MainWindow", u"N\u00ba CERTID\u00c3O:", None))
        self.forma_8.setText(QCoreApplication.translate("MainWindow", u"a", None))
        self.forma_5.setText(QCoreApplication.translate("MainWindow", u"z", None))
        self.forma_6.setText(QCoreApplication.translate("MainWindow", u"y", None))
        self.forma_7.setText(QCoreApplication.translate("MainWindow", u"y", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"DIGITALIZA\u00c7\u00c3O SERVCOM", None))
        self.buttonAumentar.setText(QCoreApplication.translate("MainWindow", u"+", None))
        self.buttonDiminuir.setText(QCoreApplication.translate("MainWindow", u"-", None))
        self.buttonVerificar.setText(QCoreApplication.translate("MainWindow", u"  Verificar", None))
        self.buttonConsultarDocumento.setText(QCoreApplication.translate("MainWindow", u"  Consultar Documento", None))
        self.buttonConferenciaErro.setText(QCoreApplication.translate("MainWindow", u"Confer\u00eancia", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("MainWindow", u"Digitaliza\u00e7\u00e3o SERVCOM", None))
        self.labelDigitalizacaoDocumentosSimples.setText(QCoreApplication.translate("MainWindow", u"DIGITALIZA\u00c7\u00c3O DE DOCUMENTOS", None))
        self.lblTrabalhoDocumentosSimples.setText(QCoreApplication.translate("MainWindow", u"TRABALHO ATUAL:", None))
        self.buttonGravarDocumentosSimples.setText(QCoreApplication.translate("MainWindow", u"  Gravar Digitaliza\u00e7\u00e3o", None))
        self.buttonLimparDocumentosSimples.setText(QCoreApplication.translate("MainWindow", u"  Cancelar", None))
        self.buttonDigitalizarDocumentosSimples.setText(QCoreApplication.translate("MainWindow", u"  Digitalizar", None))
        self.labelNumeroDocumentoSimples.setText(QCoreApplication.translate("MainWindow", u"N\u00daMERO DO DOCUMENTO:", None))
        self.buttonDocumentInfo.setText(QCoreApplication.translate("MainWindow", u"?", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("MainWindow", u"Digitaliza\u00e7\u00e3o de Documentos", None))
        self.label_conferencia.setText(QCoreApplication.translate("MainWindow", u"CONFER\u00caNCIA", None))
        self.button_listar_conf.setText(QCoreApplication.translate("MainWindow", u"Listar", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), QCoreApplication.translate("MainWindow", u"Confer\u00eancia", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"AUDITORIA", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"Filtros", None))
        self.label_final.setText(QCoreApplication.translate("MainWindow", u"In\u00edcio:", None))
        self.label_7.setText(QCoreApplication.translate("MainWindow", u"Final:", None))
        self.label_certidao.setText(QCoreApplication.translate("MainWindow", u"Ano:   N\u00famero:", None))
        self.label_documento.setText(QCoreApplication.translate("MainWindow", u"N\u00famero:", None))
        self.buttonListar.setText(QCoreApplication.translate("MainWindow", u"Listar", None))
        self.buttonCancelar.setText(QCoreApplication.translate("MainWindow", u"Cancelar", None))
        self.buttonImprimir.setText(QCoreApplication.translate("MainWindow", u"Imprimir", None))
        self.buttonSalvar.setText(QCoreApplication.translate("MainWindow", u"Salvar", None))
        self.filtro_listar_documentos.setItemText(0, QCoreApplication.translate("MainWindow", u"Todos", None))
        self.filtro_listar_documentos.setItemText(1, QCoreApplication.translate("MainWindow", u"Corretos", None))
        self.filtro_listar_documentos.setItemText(2, QCoreApplication.translate("MainWindow", u"Incorretos", None))

        self.label_listar_documentos.setText(QCoreApplication.translate("MainWindow", u"Listar documentos:", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), QCoreApplication.translate("MainWindow", u"Auditoria", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"CONFIGURA\u00c7\u00d5ES", None))
        self.Configuracoes_Gerais.setText(QCoreApplication.translate("MainWindow", u"Configura\u00e7\u00f5es Locais", None))
        self.label_temp_index.setText(QCoreApplication.translate("MainWindow", u"Pasta Temp_Index:", None))
        self.label_servidor.setText(QCoreApplication.translate("MainWindow", u"Servidor:", None))
        self.button_salvar_config.setText(QCoreApplication.translate("MainWindow", u"Salvar", None))
        self.button_cancelar_config.setText(QCoreApplication.translate("MainWindow", u"Cancelar", None))
        self.label_caminho_naps2.setText(QCoreApplication.translate("MainWindow", u"Caminho NAPS2", None))
        self.button_testar_email.setText(QCoreApplication.translate("MainWindow", u"Testar E-mail", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Cria\u00e7\u00e3o/Atualiza\u00e7\u00e3o de Usu\u00e1rio", None))
        self.label_sigla.setText(QCoreApplication.translate("MainWindow", u"Sigla do usu\u00e1rio:", None))
        self.button_verificar_sigla.setText(QCoreApplication.translate("MainWindow", u"Verificar", None))
        self.label_sigla_2.setText(QCoreApplication.translate("MainWindow", u"Nome do usu\u00e1rio:", None))
        self.label_sigla_3.setText(QCoreApplication.translate("MainWindow", u"Acesso do usu\u00e1rio:", None))
        self.combo_acesso_usuario.setItemText(0, QCoreApplication.translate("MainWindow", u"Digitaliza\u00e7\u00e3o", None))
        self.combo_acesso_usuario.setItemText(1, QCoreApplication.translate("MainWindow", u"Administrador", None))
        self.combo_acesso_usuario.setItemText(2, QCoreApplication.translate("MainWindow", u"Documentos", None))
        self.combo_acesso_usuario.setItemText(3, QCoreApplication.translate("MainWindow", u"Consulta", None))
        self.combo_acesso_usuario.setItemText(4, QCoreApplication.translate("MainWindow", u"Digitaliza\u00e7\u00e3o Simples", None))

        self.label_sigla_4.setText(QCoreApplication.translate("MainWindow", u"Senha do usu\u00e1rio:", None))
        self.label_sigla_5.setText(QCoreApplication.translate("MainWindow", u"Confirmar senha:", None))
        self.button_criar_atualizar.setText(QCoreApplication.translate("MainWindow", u"Criar/Atualizar", None))
        self.button_cancelar_usuario.setText(QCoreApplication.translate("MainWindow", u"Cancelar", None))
        self.label_6.setText("")
        self.label_8.setText("")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_5), QCoreApplication.translate("MainWindow", u"Configura\u00e7\u00f5es", None))
    # retranslateUi

