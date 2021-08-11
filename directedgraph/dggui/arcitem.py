import random

from PySide6 import QtWidgets
from PySide6.QtCore import Qt, QPointF
from PySide6.QtGui import QAction, QPainterPath
from PySide6.QtWidgets import QMenu, QGraphicsPathItem, QInputDialog


class ArcItem(QGraphicsPathItem):
    def __init__(self, arc_inst, main_window_inst=None):
        random_list = [
            -35,
            -33,
            -30,
            -27,
            -25,
            -23,
            35,
            33,
            30,
            27,
            25,
            23,
        ]
        self.arc = arc_inst
        self.arc.connected_gui = self
        self.arc.connected_window = main_window_inst
        self.connected_window = main_window_inst
        self.curvature = random.choice(random_list)
        # self.curvature = random.randint(-30, -10) * random.randint(1)
        # print(self.curvature)

        self.start_point = QPointF()
        self.start_point.setX(self.arc.nodes[0].position[0])
        self.start_point.setY(self.arc.nodes[0].position[1])

        self.mid_point = QPointF()
        self.mid_point.setX(
            (self.arc.nodes[0].position[0] + self.arc.nodes[1].position[0]) / 2
            - self.curvature * 6
        )
        self.mid_point.setY(
            (self.arc.nodes[0].position[1] + self.arc.nodes[1].position[1]) / 2
            - self.curvature * 6
        )

        self.end_point = QPointF()
        self.end_point.setX(self.arc.nodes[1].position[0])
        self.end_point.setY(self.arc.nodes[1].position[1])

        self.arc_PainterPath = QPainterPath(self.start_point)
        self.arc_PainterPath.quadTo(
            self.mid_point.x(),
            self.mid_point.y(),
            self.end_point.x(),
            self.end_point.y(),
        )

        super().__init__(self.arc_PainterPath)
        self.setZValue(-1)
        pass

    def paint(self, painter, QStyleOptionGraphicsItem, QWidget_widget=None):
        painter.setPen(Qt.black)
        painter.setBrush(Qt.NoBrush)

        self.start_point.setX(self.arc.nodes[0].position[0])
        self.start_point.setY(self.arc.nodes[0].position[1])

        self.mid_point.setX(
            (self.arc.nodes[0].position[0] + self.arc.nodes[1].position[0]) / 2
            - self.curvature * 4
        )
        self.mid_point.setY(
            (self.arc.nodes[0].position[1] + self.arc.nodes[1].position[1]) / 2
            - self.curvature * 4
        )

        self.end_point.setX(self.arc.nodes[1].position[0])
        self.end_point.setY(self.arc.nodes[1].position[1])

        self.arc_PainterPath = QPainterPath(self.start_point)
        self.arc_PainterPath.quadTo(
            self.mid_point.x(),
            self.mid_point.y(),
            self.end_point.x(),
            self.end_point.y(),
        )
        painter.drawPath(self.arc_PainterPath)

        painter.drawText(
            self.mid_point.x() + self.curvature * 2,
            self.mid_point.y() + self.curvature * 2,
            "    Name: " + self.arc.name,
        )
        painter.drawText(
            self.mid_point.x() + self.curvature * 2 + 14,
            self.mid_point.y() + self.curvature * 2 + 14,
            str(self.arc.user_defined_arc_type)
            + ": "
            + str(self.arc.user_defined_attribute),
        )

    def contextMenuEvent(self, event):
        popmenu = QMenu()

        nameAction = QAction("Edit Name")
        popmenu.addAction(nameAction)
        nameAction.triggered.connect(self.on_name_action)

        typeAction = QAction("Edit Arc Type")
        popmenu.addAction(typeAction)
        typeAction.triggered.connect(self.on_type_action)

        attributeAction = QAction("Edit Arc Attribute")
        popmenu.addAction(attributeAction)
        attributeAction.triggered.connect(self.on_attribute_action)

        popmenu.addSeparator()

        deleteAction = QAction("Delete")
        popmenu.addAction(deleteAction)
        deleteAction.triggered.connect(self.on_delete_action)

        popmenu.exec_(event.screenPos())

    def on_name_action(self):
        text, result = QInputDialog.getText(
            self.connected_window,
            "Input",
            "Enter Name",
            QtWidgets.QLineEdit.Normal,
        )
        if result is True:
            self.arc.name = str(text)

    def on_type_action(self):
        text, result = QInputDialog.getText(
            self.connected_window,
            "Input",
            "Enter Type",
            QtWidgets.QLineEdit.Normal,
        )
        if result is True:
            self.arc.user_defined_arc_type = str(text)

    def on_attribute_action(self):
        text, result = QInputDialog.getText(
            self.connected_window,
            "Input",
            "Enter Attribute",
            QtWidgets.QLineEdit.Normal,
        )
        if result is True:
            self.arc.user_defined_attribute = str(text)

    def on_delete_action(self):
        self.arc.connected_graph.delete_component(self.arc.uid)
        self.connected_window.scene.removeItem(self)
