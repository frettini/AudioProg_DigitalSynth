import PyQt5.QtWidgets


class ExecutiveToy(QtWidget):

    def __init__(self, parent = None):
        super.__init__(parent)
        self.create_UI(parent)