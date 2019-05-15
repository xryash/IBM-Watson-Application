import logging

from PyQt5.QtWidgets import QMainWindow, QPushButton, QLineEdit

from gui.log_form import LogForm
from gui.plot_form import PlotForm
from utils import safe_cast
import pandas as pd

class MainForm(QMainWindow):
    def __init__(self, logger, watson, repository):
        self.logger = logger
        self.logger.info('.__init__() entered')

        self.watson = watson
        self.repository = repository
        super().__init__()

        self.StepPlotButton = QPushButton(self)
        self.ConnectButton = QPushButton(self)
        self.LoggingButton = QPushButton(self)
        self.dayEdit = QLineEdit(self)
        self.left = 10
        self.top = 10
        self.title = 'PyQt GUI main'
        self.width = 300
        self.height = 250
        self.buttons_width = 200
        self.buttons_height = 40

        self.plot_instance = None
        self.log_instance = LogForm(self.logger)
        self.log_instance.show()

        self.client_connected = False
        self.initUI()

    def initUI(self):
        self.logger.info('.initUI() entered')
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.StepPlotButton.setGeometry(45, 10, self.buttons_width, self.buttons_height)
        self.StepPlotButton.setText("Plot")

        self.dayEdit.setGeometry(45, 60, self.buttons_width, self.buttons_height)

        self.ConnectButton.setGeometry(45, 110, self.buttons_width, self.buttons_height)
        self.ConnectButton.setText("Connect to the service")

        self.LoggingButton.setGeometry(45, 160, self.buttons_width, self.buttons_height)
        self.LoggingButton.setText("Open log")

        self.StepPlotButton.clicked.connect(self.on_StepPlotButton_clicked)
        self.LoggingButton.clicked.connect(self.on_LoggingButton_clicked)
        self.ConnectButton.clicked.connect(self.on_ConnectButton_clicked)

        self.show()


    def get_dataset(self, repository, day):
        events = repository.get_events()
        dataframe = pd.DataFrame(events).filter(items=[2, 4, 5])
        dataframe.columns = ['device', 'date', 'steps']
        dataframe.date = pd.to_datetime(dataframe.date)
        dataframe = dataframe.groupby('date', sort=True)['steps'].sum()
        new_df = pd.DataFrame()
        new_df['date'] = pd.to_datetime(dataframe.keys())
        new_df['steps'] = dataframe.values
        by_day = new_df[new_df['date'].dt.day == day]
        return by_day

    def on_StepPlotButton_clicked(self):
        self.logger.info('.on_StepPlotButton_clicked() entered')
        day = safe_cast(self.dayEdit.text().strip(), int, 0)
        if not (day == 0):
            dataset = self.get_dataset(self.repository, day)
            self.plot_instance = PlotForm(self.logger, dataset)
            self.plot_instance.show()
        else:
            self.logger.error('dayEdit.text is not int value!')



    def on_ConnectButton_clicked(self):
        self.logger.info('.on_ConnectButton_clicked() entered')
        if not self.client_connected:
            # connect watson
            self.watson.connect()
            self.client_connected = True
            self.ConnectButton.setText("Disconnect to the service")
        else:
            # disconnect watson
            self.watson.disconnect()
            self.client_connected = False
            self.ConnectButton.setText("Connect to the service")

    def on_LoggingButton_clicked(self):
        self.logger.info('.on_LoggingButton_clicked() entered')
        self.log_instance = LogForm(self.logger)
        self.log_instance.show()
