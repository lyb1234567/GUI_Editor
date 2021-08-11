import sys
from pathlib import Path

from PySide6 import QtCore
from PySide6 import QtGui
from PySide6.QtWidgets import QGraphicsScene

print("Running" if __name__ == "__main__" else "Importing", Path(__file__).resolve())
CURRENT_DIRECTORY = Path(__file__).absolute()
ROOT_FOLDER = CURRENT_DIRECTORY.parent.parent.parent
sys.path.append(str(ROOT_FOLDER))

from directedgraph.dggui import (
    NodeItem,
    SourceNodeItem,
    GroundNodeItem,
)


class GraphEditorScene(QGraphicsScene):
    def __init__(self, parent=None):
        super(GraphEditorScene, self).__init__(0, 0, 1280, 720, parent)
        self.selected_items = []

    def mousePressEvent(self, event):
        if event.modifiers() & QtCore.Qt.ShiftModifier:
            item = self.itemAt(event.scenePos(), QtGui.QTransform())
            if item:
                if type(item) in [NodeItem, SourceNodeItem, GroundNodeItem]:
                    item.selectionRectangle.setVisible(True)
                    if item in self.selected_items:
                        pass
                    else:
                        self.selected_items.append(item)
                        print(self.selected_items)
        else:
            for item in self.selected_items:
                item.selectionRectangle.setVisible(False)
            self.selected_items.clear()

        super(GraphEditorScene, self).mousePressEvent(event)
