from PyQt5.QtCore import QDateTime, QDate, QUrl
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import QWebEngineView
import os
from marketDataLib import getMarketData



class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.initUI()

    def initUI(self):
        getMarketData('UBER', '2023-05-31', '2023-06-02', '1d')
        self.setWindowTitle("Live Market Data")
        self.setCentralWidget(QWidget(self))
        self.setMinimumHeight(720)
        self.setMinimumWidth(1280)
        self.showMaximized()
        self.show()

        layout = QGridLayout()
        self.centralWidget().setLayout(layout)

        self.tickersLineEdit = QLineEdit()
        self.tickersLineEdit.setPlaceholderText("Insert ticker")

        self.periodStart = QDateEdit()

        self.periodEnd = QDateEdit()
        self.periodEnd.setDate(QDate.currentDate())

        self.intervalComboBox = QComboBox()
        # [1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo] int
        for interval in ['1m', '2m', '5m', '15m', '30m', '60m', '90m', '1h', '1d', '5d', '1wk', '1mo', '3mo']:
            self.intervalComboBox.addItem(interval)

        self.browser = QWebEngineView()

        self.trackButton = QPushButton("track")
        self.trackButton.clicked.connect(self.track)

        layout.addWidget(self.tickersLineEdit, 1, 0, 1, 6)
        layout.addWidget(QLabel("start date: "), 2, 0)
        layout.addWidget(self.periodStart, 2, 1)
        layout.addWidget(QLabel("end date: "), 2, 2)
        layout.addWidget(self.periodEnd, 2, 3)
        layout.addWidget(QLabel("interval: "), 2, 4)
        layout.addWidget(self.intervalComboBox, 2, 5)
        layout.addWidget(self.trackButton, 3, 0, 1, 1)
        layout.addWidget(self.browser, 4, 0, 1, 6)

        temp_var = self.periodEnd.date()
        var_name = temp_var.toPyDate()

        print(var_name)

    def track(self):
        state = getMarketData(self.tickersLineEdit.text(), self.periodStart.date().toPyDate(), self.periodEnd.date().toPyDate(), self.intervalComboBox.currentText())
        if state:
            file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "marketData.html"))
            local_url = QUrl.fromLocalFile(file_path)
            self.browser.load(local_url)


app = QApplication([])
window = MainWindow()
app.exec_()