import sys

from PySide6.QtWidgets import QApplication

from directedgraph.dggui import GraphEditorMainWindow


class GraphEditor:
    """
    Run
    """

    def __init__(self):
        self.auto_save_interval = "300s"
        self.application = QApplication([])
        self.mainwindow = GraphEditorMainWindow()

    def run(self):
        """
        Run
        """

        print("Running")
        self.mainwindow.show()  # .showMaximized()
        sys.exit(self.application.exec_())

    def run_debug(self):
        """
        Debug
        """
        print("Running Debug Mode")
        self.mainwindow.show()
        sys.exit(self.application.exec_())
