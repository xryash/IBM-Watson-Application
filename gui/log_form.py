import logging

from PyQt5.QtWidgets import QWidget, QTextEdit, QVBoxLayout


class LogForm(QWidget):
    def __init__(self, logger):
        self.logger = logger
        self.logger.info('.__init__() entered')
        super().__init__()
        self.left = 10
        self.top = 10
        self.title = 'PyQt GUI Logs'
        self.width = 600
        self.height = 400
        self.logger_edit = QTextEdit()
        layout = QVBoxLayout(self)
        layout.addWidget(self.logger_edit)

        self.initUI()

    def initUI(self):
        self.logger.info('.initUI() entered')
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.logger_edit.setReadOnly(True)
        self.logger_edit.show()
        log_handler = logging.Handler()
        log_handler_formatter = logging.Formatter(
            '# [%(asctime)s] %(levelname)-s: %(message)s\n',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        log_handler.emit = lambda record: self.logger_edit.insertPlainText(log_handler_formatter.format(record))
        log_handler.setLevel(logging.INFO)

        self.logger.addHandler(log_handler)
