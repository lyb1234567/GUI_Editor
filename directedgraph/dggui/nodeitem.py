import sys
from pathlib import Path

from PySide6 import QtWidgets
from PySide6.QtCore import Qt, QRectF
from PySide6.QtGui import QAction
from PySide6.QtGui import QColor, QBrush
from PySide6.QtWidgets import (
    QApplication,
    QInputDialog,
    QColorDialog,
    QMenu,
    QGraphicsEllipseItem,
    QGraphicsRectItem,
    QMessageBox,
)

print("Running" if __name__ == "__main__" else "Importing", Path(__file__).resolve())
CURRENT_DIRECTORY = Path(__file__).absolute()
ROOT_FOLDER = CURRENT_DIRECTORY.parent.parent.parent
sys.path.append(str(ROOT_FOLDER))


class NodeItem(QGraphicsEllipseItem):
    def __init__(self, node_inst, main_window_inst):
        self.node = node_inst
        self.connected_window = main_window_inst

        self.node_radius = 40.0

        self.node_fill_colour = QColor(
            int(self.node.colour[1:3], 16),
            int(self.node.colour[3:5], 16),
            int(self.node.colour[5:7], 16),
        )

        self.node_fill_brush = QBrush(Qt.black, Qt.SolidPattern)
        self.node_fill_brush.setColor(self.node_fill_colour)

        bounding_shape = QRectF(
            self.node.position[0] - self.node_radius,
            self.node.position[1] - self.node_radius,
            2.0 * self.node_radius,
            2.0 * self.node_radius,
        )

        super().__init__(bounding_shape)

        self.setZValue(10)
        self.setBrush(self.node_fill_brush)

        # Set node attributes
        self.ItemIsSelectable = True
        self.ItemIsMovable = True
        self.ItemSendsGeometryChanges = True
        self.setAcceptHoverEvents(True)  # Make the Node accpect the Hover Event

        # Create selection rectangle shown when node is selected
        self.selectionRectangle = QGraphicsRectItem(self.boundingRect())
        self.selectionRectangle.setVisible(False)

    # ------------------------- paint -------------------------

    # Paint the node instance - called by QGraphicView instance
    def paint(self, painter, option, parent):

        boundingRect = self.boundingRect()

        if self.selectionRectangle.isVisible():
            # Paint selection rectangle
            painter.setPen(Qt.DashLine)
            painter.setBrush(Qt.NoBrush)
            self.selectionRectangle.setRect(boundingRect)
            painter.drawRect(boundingRect)

        # Paint node circle
        self.node_fill_colour = QColor(
            int(self.node.colour[1:3], 16),
            int(self.node.colour[3:5], 16),
            int(self.node.colour[5:7], 16),
        )
        self.node_fill_brush = QBrush(Qt.black, Qt.SolidPattern)
        self.node_fill_brush.setColor(self.node_fill_colour)
        painter.setBrush(self.node_fill_brush)
        painter.drawEllipse(boundingRect)

        # Paint node text
        painter.setPen(Qt.black)
        boundingRect.adjust(0, 20, 0, 20)
        painter.drawText(boundingRect, Qt.AlignCenter, self.node.name)
        boundingRect.adjust(0, -40, 0, -40)
        painter.drawText(boundingRect, Qt.AlignCenter, self.node.uid)

        self.connected_window.scene.update()  # Fixing Arc's dragging issue

        # print("node paint called")

        return

    def setPos(self, pos):
        bounding = self.boundingRect()
        offset = bounding.center()
        super().setPos(pos - offset)
        return

    # ------------------------- Mouse Event -------------------------

    # Override cursor shape into Openhand to indicate that drag is allowed
    # also indicate that you have selected a node (read to move)
    def hoverEnterEvent(self, event):
        app = QApplication.instance()  # Obtain the Q application instance
        app.instance().setOverrideCursor(Qt.OpenHandCursor)
        return

    # This Method is used to change back the cursor when mouse is not point to the node
    def hoverLeaveEvent(self, event):
        app = QApplication.instance()  # Obtain the Q application instance
        app.instance().restoreOverrideCursor()
        return

    # Handler for mousePressEvent
    def mousePressEvent(self, event):
        # mousePos = event.pos()
        # self.selectionRectangle.setVisible(True)
        # print("mousePressEvent at", mousePos.x(), ", ", mousePos.y())
        return

    # Handler for mouseReleaseEvent
    def mouseReleaseEvent(self, event):
        # mousePos = event.pos()
        # self.selectionRectangle.setVisible(False)
        # print("mouseReleaseEvent at ", mousePos.x(), ", ", mousePos.y())
        return

    # Handler for mouseMoveEvent
    def mouseMoveEvent(self, event):
        scenePosition = event.scenePos()

        self.setPos(scenePosition)

        self.node.position[0] = scenePosition.x()
        self.node.position[1] = scenePosition.y()

        # print("NodeItem Position:", self.node.position)
        # print("mouseMoveEvent to", scenePosition.x(), ", ", scenePosition.y())

        return

    # Handler for mouseDoubleClickEvent
    def mouseDoubleClickEvent(self, event):
        # self.setVisible(False)
        # print("mouseDoubleClickEvent")
        return

    # ------------------------- Pop -------------------------

    # Pop Context Menu
    def contextMenuEvent(self, event):
        # Pop up menu for Node
        popmenu = QMenu()

        # Name
        nameAction = QAction("Edit Name")
        popmenu.addAction(nameAction)
        nameAction.triggered.connect(self.on_name_action)

        # Colour
        colourAction = QAction("Edit Colour")
        popmenu.addAction(colourAction)
        colourAction.triggered.connect(self.on_colour_action)

        popmenu.addSeparator()

        # Duplicate
        duplicateAction = QAction("Duplicate")
        popmenu.addAction(duplicateAction)
        duplicateAction.triggered.connect(self.on_duplicate_action)

        # Delete
        deleteAction = QAction("Delete")
        popmenu.addAction(deleteAction)
        deleteAction.triggered.connect(self.on_delete_action)

        # Excute at node Position, so it won't collide with Main windows pop-up menu
        popmenu.exec_(event.screenPos())

    # ------------------------- Action -------------------------

    def on_name_action(self):
        text, result = QInputDialog.getText(
            self.connected_window,
            "Input",
            "Enter Name",
            QtWidgets.QLineEdit.Normal,
        )
        if result is True:
            self.node.name = str(text)

    def on_colour_action(self):
        color = QColorDialog.getColor()
        if (color.red() + color.green() + color.blue()) != 0:
            print("error")
            self.node.colour = (
                "#"
                + str(hex(color.getRgb()[0])[2:4]).zfill(2)
                + str(hex(color.getRgb()[1])[2:4]).zfill(2)
                + str(hex(color.getRgb()[2])[2:4]).zfill(2)
            )
            print(self.node.colour)

    def on_duplicate_action(self):
        self.connected_window.scene.addItem(
            NodeItem(
                self.node.connected_graph.create_component(
                    {
                        "type": "Node",
                        "name": self.node.name + " Copy",
                        "colour": self.node.colour,
                        "position_x": self.node.position[0],
                        "position_y": self.node.position[1],
                    }
                ),
                self.connected_window,
            )
        )

    def on_delete_action(self):
        self.node.connected_graph.update_component_node_arcs()

        if self.node.connected_graph.delete_component(self.node.uid):
            for arc in self.node.arcs:
                arc.connected_window.scene.removeItem(arc.connected_gui)
                self.node.connected_graph.delete_component(arc.uid)
            self.connected_window.scene.removeItem(self)


class SourceNodeItem(NodeItem):
    def __init__(self, node_inst, main_window_inst):
        super().__init__(node_inst, main_window_inst)

    def paint(self, painter, option, parent):
        boundingRect = self.boundingRect()

        if self.selectionRectangle.isVisible():
            painter.setPen(Qt.DashLine)
            painter.setBrush(Qt.NoBrush)
            self.selectionRectangle.setRect(boundingRect)
            painter.drawRect(boundingRect)

        self.node_fill_colour = QColor(
            int(self.node.colour[1:3], 16),
            int(self.node.colour[3:5], 16),
            int(self.node.colour[5:7], 16),
        )
        self.node_fill_brush = QBrush(Qt.black, Qt.SolidPattern)
        self.node_fill_brush.setColor(self.node_fill_colour)
        painter.setBrush(self.node_fill_brush)
        painter.drawEllipse(boundingRect)

        painter.setPen(Qt.black)
        painter.drawText(boundingRect, Qt.AlignCenter, self.node.user_defined_attribute)
        boundingRect.adjust(0, 20, 0, 20)
        painter.drawText(boundingRect, Qt.AlignCenter, self.node.name)
        boundingRect.adjust(0, -40, 0, -40)
        painter.drawText(boundingRect, Qt.AlignCenter, self.node.uid)

    def on_duplicate_action(self):
        self.connected_window.scene.addItem(
            SourceNodeItem(
                self.node.connected_graph.create_component(
                    {
                        "type": "SourceNode",
                        "name": self.node.name + " Copy",
                        "colour": self.node.colour,
                        "position_x": self.node.position[0],
                        "position_y": self.node.position[1],
                        "user_defined_attribute": self.node.user_defined_attribute,
                    }
                ),
                self.connected_window,
            )
        )


class GroundNodeItem(NodeItem):
    def __init__(self, node_inst, main_window_inst):
        super().__init__(node_inst, main_window_inst)

    def on_duplicate_action(self):
        QMessageBox.about(
            self.connected_window,
            "Error",
            "GroundNode cannot Duplicate",
        )
