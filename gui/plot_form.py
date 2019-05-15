import random

from PyQt5.QtWidgets import QWidget, QSizePolicy
from matplotlib import ticker

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class PlotForm(QWidget):
    def __init__(self, logger, dataset):
        self.logger = logger
        self.logger.info('PlotForm.__init__() entered')
        super().__init__()
        self.dataset = dataset
        self.left = 10
        self.top = 10
        self.title = 'PyQt GUI plot'
        self.width = 600
        self.height = 600
        self.initUI()

    def initUI(self):
        self.logger.info('PlotForm.initUI() entered')
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        dpi = 100
        plot_width = int(self.width / dpi)
        plot_height = int(self.height / dpi)
        m = PlotCanvas(logger=self.logger, dataset=self.dataset, width=plot_width, height=plot_height, dpi=dpi, parent=self)
        m.move(0, 0)
        self.show()


class PlotCanvas(FigureCanvas):

    def __init__(self, logger, dataset, width, height, dpi, parent=None):
        self.logger = logger
        self.logger.info('PlotCanvas.__init__() entered')
        self.dataset = dataset
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.plot()

    def plot(self):
        self.logger.info('PlotCanvas.plot() entered')
        print(self.dataset)
        ax = self.figure.add_subplot(111)
        self.dataset.plot( x='date', y='steps', ax=ax, color='r')
        ax.set_xticklabels([pandas_datetime.strftime("%H:%M") for pandas_datetime in self.dataset.date if pandas_datetime.hour % 3 == 0 and pandas_datetime.hour is not 0])
        ax.set_title('Steps graph')
        ax.set_xlabel('Time', fontsize=16)
        ax.set_ylabel('Steps', fontsize=16)

        ax.legend()
        self.draw()
