import sys
import math
from pathlib import Path

from PySide6.QtCore import Qt, QRectF
from PySide6.QtGui import QAction, QPainter, QPainterPath, QBrush
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QWidget,
    QLineEdit,
    QPushButton,
    QDialog,
)
from PySide6 import QtWidgets
from PySide6.QtWidgets import QMenu
from PySide6.QtWidgets import QFileDialog, QMessageBox
from PySide6.QtWidgets import (
    QGraphicsScene,
    QGraphicsView,
    QGraphicsEllipseItem,
    QGraphicsRectItem,
)


print("Running" if __name__ == "__main__" else "Importing", Path(__file__).resolve())
CURRENT_DIRECTORY = Path(__file__).absolute()
ROOT_FOLDER = CURRENT_DIRECTORY.parent.parent.parent
sys.path.append(str(ROOT_FOLDER))

from directedgraph.dgcore import Node, GroundNode, SourceNode, Arc, Graph, graph
from directedgraph.dgcore import GroundNodeNumberError
from directedgraph.dgutils import FileManager
from directedgraph.dggui import NodeItem, SourceNodeItem, GroundNodeItem


class ArcItem(QGraphicsEllipseItem):
    def __init__(self, arc_inst, graph=None):
        self.arc_inst = arc_inst
        self.graph = graph
        # 根据两端的uid获取查询所在图中两个node对象
        self.node1 = self.arc_inst.nodes[0]
        self.node2 = self.arc_inst.nodes[1]

        # 再根据两个node对象得到两个node对象的位置
        self.node1_position = self.node1.get_position()
        self.node2_position = self.node2.get_position()

        print("arc", self.arc_inst.name)
        print("node1_position", self.node1.get_position())
        print("node2_position", self.node2.get_position())

        self.arc_fill_brush = QBrush(Qt.black, Qt.SolidPattern)
        if (
            self.node1_position[0] < self.node2_position[0]
            and self.node1_position[1] < self.node2_position[1]
        ):
            bounding_shape = QRectF(
                self.node1_position[0]
                - (self.node2_position[0] - self.node1_position[0]),
                self.node1_position[1],
                2 * (abs(self.node1_position[0] - self.node2_position[0])),
                2 * (abs(self.node1_position[1] - self.node2_position[1]))
                # 2*(abs(self.node1_position[1] - self.node2_position[1])),
            )
        elif (
            self.node1_position[0] > self.node2_position[0]
            and self.node1_position[1] < self.node2_position[1]
        ):
            bounding_shape = QRectF(
                self.node2_position[0],
                self.node2_position[1]
                - abs(self.node2_position[1] - self.node1_position[1]),
                2 * (abs(self.node1_position[0] - self.node2_position[0])),
                2 * (abs(self.node1_position[1] - self.node2_position[1]))
                # 2*(abs(self.node1_position[1] - self.node2_position[1])),
            )
        elif (
            self.node1_position[0] < self.node2_position[0]
            and self.node1_position[1] > self.node2_position[1]
        ):
            bounding_shape = QRectF(
                self.node1_position[0],
                self.node1_position[1]
                - abs(self.node1_position[1] - self.node2_position[1]),
                2 * (abs(self.node2_position[0] - self.node1_position[0])),
                2 * (abs(self.node2_position[1] - self.node1_position[1]))
                # 2*(abs(self.node1_position[1] - self.node2_position[1])),
            )
        elif (
            self.node1_position[0] > self.node2_position[0]
            and self.node1_position[1] > self.node2_position[1]
        ):
            bounding_shape = QRectF(
                self.node2_position[0]
                - (self.node1_position[0] - self.node2_position[0]),
                self.node2_position[1],
                2 * (abs(self.node2_position[0] - self.node1_position[0])),
                2 * (abs(self.node2_position[1] - self.node1_position[1])),
            )
        elif (
            self.node1_position[0] == self.node2_position[0]
            and self.node1_position[1] < self.node2_position[1]
        ):
            bounding_shape = QRectF(
                self.node1_position[0]
                - 0.5 * abs(self.node1_position[1] - self.node2_position[1]),
                self.node1_position[1],
                (abs(self.node2_position[1] - self.node1_position[1])),
                (abs(self.node2_position[1] - self.node1_position[1])),
            )
        elif (
            self.node1_position[0] == self.node2_position[0]
            and self.node1_position[1] > self.node2_position[1]
        ):
            bounding_shape = QRectF(
                self.node2_position[0]
                - 0.5 * abs(self.node1_position[1] - self.node2_position[1]),
                self.node2_position[1],
                (abs(self.node2_position[1] - self.node1_position[1])),
                (abs(self.node2_position[1] - self.node1_position[1])),
            )
        elif (
            self.node1_position[0] > self.node2_position[0]
            and self.node1_position[1] == self.node2_position[1]
        ):
            bounding_shape = QRectF(
                self.node2_position[0],
                self.node2_position[1]
                - 0.5 * abs(self.node2_position[0] - self.node1_position[0]),
                (abs(self.node2_position[0] - self.node1_position[0])),
                (abs(self.node2_position[0] - self.node1_position[0])),
            )
        elif (
            self.node1_position[0] < self.node2_position[0]
            and self.node1_position[1] == self.node2_position[1]
        ):
            bounding_shape = QRectF(
                self.node1_position[0],
                self.node1_position[1]
                - 0.5 * abs(self.node1_position[0] - self.node2_position[0]),
                (abs(self.node2_position[0] - self.node1_position[0])),
                (abs(self.node2_position[0] - self.node1_position[0])),
            )
        # print("bounding_shape:", bounding_shape.center())
        super().__init__(bounding_shape)

        self.setZValue(0)
        self.setBrush(self.arc_fill_brush)

        # Set node attributes
        self.ItemIsSelectable = True
        self.ItemIsMovable = True
        self.ItemSendsGeometryChanges = True
        self.setAcceptHoverEvents(True)  # Make the Node accpect the Hover Event

        # Create selection rectangle shown when node is selected
        self.selectionRectangle = QGraphicsRectItem(self.boundingRect())
        self.selectionRectangle.setVisible(False)

    def paint(self, painter, option, parent):
        self.node1_position = self.node1.get_position()
        self.node2_position = self.node2.get_position()

        # print("node1_position at Arc", self.node1.get_position())

        boundingRect = self.boundingRect()

        if self.selectionRectangle.isVisible():
            # Paint selection rectangle
            painter.setPen(Qt.DashLine)
            painter.setBrush(Qt.NoBrush)
            self.selectionRectangle.setRect(boundingRect)
            painter.drawRect(boundingRect)

        # Paint node circle
        painter.setBrush(self.arc_fill_brush)

        painter.setPen(Qt.black)
        # painter.drawText(boundingRect,Qt.AlignCenter,self.arc_inst.name)
        # painter.drawText(boundingRect, Qt.AlignCenter, self.arc_inst.uid)
        degree1 = (
            math.atan(self.node1_position[1] / self.node1_position[0]) / math.pi
        ) * 180
        degree2 = (
            math.atan(self.node2_position[1] / self.node2_position[0]) / math.pi
        ) * 180

        if (
            self.node1_position[0] < self.node2_position[0]
            and self.node1_position[1] < self.node2_position[1]
        ):
            painter.drawArc(boundingRect, 0, 90 * 16)

        elif (
            self.node1_position[0] > self.node2_position[0]
            and self.node1_position[1] < self.node2_position[1]
        ):
            painter.drawArc(boundingRect, 90 * 16, 90 * 16)

        elif (
            self.node1_position[0] < self.node2_position[0]
            and self.node1_position[1] > self.node2_position[1]
        ):
            painter.drawArc(boundingRect, 180 * 16, -90 * 16)

        elif (
            self.node1_position[0] > self.node2_position[0]
            and self.node1_position[1] > self.node2_position[1]
        ):
            painter.drawArc(boundingRect, 0, 90 * 16)
        elif (
            self.node1_position[0] == self.node2_position[0]
            and self.node1_position[1] < self.node2_position[1]
        ):
            painter.drawArc(boundingRect, 90 * 16, 180 * 16)
        elif (
            self.node1_position[0] == self.node2_position[0]
            and self.node1_position[1] > self.node2_position[1]
        ):
            painter.drawArc(boundingRect, -90 * 16, -180 * 16)
        elif (
            self.node1_position[0] > self.node2_position[0]
            and self.node1_position[1] == self.node2_position[1]
        ):
            painter.drawArc(boundingRect, 0, 180 * 16)
        elif (
            self.node1_position[0] < self.node2_position[0]
            and self.node1_position[1] == self.node2_position[1]
        ):
            painter.drawArc(boundingRect, 180 * 16, -180 * 16)
        return

    def hoverEnterEvent(self, event):
        # 如果鼠标变成一个手说明可以准备移动 , 也可以表示你选中了一个节点，可以准备有动作
        app = QtWidgets.QApplication.instance()  # Obtain the Qapplication instance
        app.instance().setOverrideCursor(Qt.OpenHandCursor)

    def hoverLeaveEvent(self, event):
        # Change back the cursor when mouse is not point to the node
        app = QtWidgets.QApplication.instance()  # Obtain the Qapplication instance
        app.instance().restoreOverrideCursor()

    def mouseReleaseEvent(self, event):
        self.prepareGeometryChange()
        mousePos = event.pos()
        self.selectionRectangle.setVisible(False)
        print("mouseReleaseEvent at ", mousePos.x(), ", ", mousePos.y())
        # self.update()
        return

    def mousePressEvent(self, event):
        # Handler for mousePressEvent
        self.prepareGeometryChange()
        mousePos = event.pos()
        self.selectionRectangle.setVisible(True)
        print("mousePressEvent at", mousePos.x(), ", ", mousePos.y())
        # self.update()
        return

    def mouseMoveEvent(self, event):

        self.prepareGeometryChange()
        scenePosition = event.scenePos()
        self.setPos(scenePosition)
        return

    def mouseDoubleClickEvent(self, event):
        # Handler for mouseDoubleClickEvent
        self.prepareGeometryChange()
        # self.setVisible(False)
        print("mouseDoubleClickEvent")
        # self.update()
        return

    def setPos(self, pos):
        bounding = self.boundingRect()
        offset = bounding.center()
        super().setPos(pos - offset)
        return

    def contextMenuEvent(self, event):
        # Pop up menu for Node
        popmenu = QMenu()

        # Name
        nameaction = QAction("Name")
        popmenu.addAction(nameaction)
        # nameaction.triggered.connect()

        # Colour
        colouraction = QAction("Colour")
        popmenu.addAction(colouraction)
        # colouraction.triggered.connect()

        # Value
        valueaction = QAction("Value")
        popmenu.addAction(valueaction)
        # valueaction.triggered.connect()

        popmenu.addSeparator()

        # Delete
        deleteaction = QAction("Delete")
        popmenu.addAction(deleteaction)
        # deleteaction.triggered.conn ect()

        # Excute at node Position, so it won't collide with Main windows pop-up menu
        popmenu.exec_(event.screenPos())


class InputFormSourceNode(QDialog, QMainWindow):
    def __init__(self, parent=None):
        super(InputFormSourceNode, self).__init__(parent)
        self.setWindowTitle("Input source node value")
        self.edit = QLineEdit(self)
        self.edit.placeholderText()
        self.button = QPushButton("confirm")
        layout = QVBoxLayout()
        layout.addWidget(self.edit)
        layout.addWidget(self.button)
        # Set dialog layout
        self.setLayout(layout)
        # Add button signal to greetings slot
        self.button.clicked.connect(self.confirm)

    def confirm(self):
        try:
            return float(self.edit.text())
        except ValueError:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("You have to enter a number!!")
            msg.show()
            msg.exec_()
            return


class Arc_Input(QDialog, QMainWindow):
    def __init__(self, parent=None):
        super(Arc_Input, self).__init__(parent)
        self.setWindowTitle("Input two linked nodes' uid")
        self.edit1 = QLineEdit(self)
        self.edit1.placeholderText()
        self.edit2 = QLineEdit(self)
        self.edit2.placeholderText()
        self.button = QPushButton("confirm")
        layout = QVBoxLayout()
        layout.addWidget(self.edit1)
        layout.addWidget(self.edit2)
        layout.addWidget(self.button)
        # Set dialog layout
        self.setLayout(layout)
        # Add button signal to greetings slot
        self.button.clicked.connect(self.confirm)

    def confirm(self):
        return [self.edit1.text(), self.edit2.text()]


class GraphEditorMainWindow(QMainWindow, QDialog):
    def __init__(self):
        super().__init__()
        # Title of the Windows
        self.setWindowTitle("Graph Editor")
        self.ground_node_count = 0

        # Initialise the QGraphicScene
        self.scene = QGraphicsScene(0, 0, 1980, 1080, self)
        self.view = QGraphicsView(self.scene)

        # self.view.resize(1000, 1000)
        self.view.setRenderHints(QPainter.Antialiasing)
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.view)
        self.widget = QWidget()
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)

        # Set up the Menu Bar
        self.fileMenu = self.menuBar().addMenu("&File")

        self.openMenuAction = self.fileMenu.addAction("&Open")
        self.openMenuAction.triggered.connect(self.on_open_action)

        self.saveMenuAction = self.fileMenu.addAction("&Save")
        self.saveMenuAction.triggered.connect(self.on_save_action)

        self.saveAsMenuAction = self.fileMenu.addAction("&Save As...")
        self.saveAsMenuAction.triggered.connect(self.on_save_as_action)

        # Setup Graph Component menu
        self.GraphComponentMenu = self.menuBar().addMenu("&Add")

        self.NodeAction = self.GraphComponentMenu.addAction("&Node")
        self.NodeAction.triggered.connect(self.on_node_action)

        self.SourceNodeAction = self.GraphComponentMenu.addAction("&Source Node")
        self.SourceNodeAction.triggered.connect(self.on_sourcenode_action)

        self.GroundNodeAction = self.GraphComponentMenu.addAction("&Ground Node")
        self.GroundNodeAction.triggered.connect(self.on_groundnode_action)

        self.ArcAction = self.GraphComponentMenu.addAction("&Arc")
        self.ArcAction.triggered.connect(self.on_arc_action)

        self.init_graph()

    # Menu =========================================================
    def contextMenuEvent(self, event):
        contextmenu = QMenu(self)

        newaction = QAction("New")
        contextmenu.addAction(newaction)
        # newaction.triggered.connect()

        openaction = QAction("Open")
        contextmenu.addAction(openaction)
        # openaction.triggered.connect()

        saveaction = QAction("Save")
        contextmenu.addAction(saveaction)
        # saveaction.triggered.connect()

        copyaction = QAction("Copy")
        contextmenu.addAction(copyaction)
        # copyaction.triggered.connect()

        pastaction = contextmenu.addAction("Past")
        contextmenu.addAction(pastaction)
        # copyaction.triggered.connect()

        helpaction = QAction("Help...")
        contextmenu.addAction(helpaction)
        # copyaction.triggered.connect()

        # Excute the pop menu at all the graph area, but won't conflit with node pop meun
        action = contextmenu.exec_(self.mapToGlobal(event.pos()))

    # Trigger Fcuntions =========================================================
    def on_open_action(self):
        """Handler for 'Open' action"""
        fileName = QFileDialog.getOpenFileName(self, "Open File", ".", ("*.md"))
        print("opening ", fileName[0])
        return

    def on_save_action(self):
        pass

    def on_save_as_action(self):
        name = QtWidgets.QFileDialog.getSaveFileName(self, "Save File")
        file = open(name[0], "w")
        # 传输xml格式，使用filemanager
        text = "sasd"
        file.write(text)
        file.close()
        return

    def on_preferences_action(self):
        """Handler for 'Preferences' action"""
        print("preferences")
        return

    def on_about_action(self):
        """Handler for 'About' action"""
        QMessageBox.about(
            self,
            "About this program",
            "some about text crediting the people who wrote this",
        )
        return

    def on_node_action(self):
        self.scene.addItem(NodeItem(Node(None, None, "I", None, [500, 300]), self))
        # #TODO

    def on_groundnode_action(self):
        self.ground_node_count += 1
        if self.ground_node_count > 1:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Only one ground_node is allowed!!!")
            msg.show()
            msg.exec_()
            raise GroundNodeNumberError("oops!!")
        else:
            self.scene.addItem(
                GroundNodeItem(GroundNode(None, None, "G1", None, [500, 300]))
            )

    def on_sourcenode_action(self):
        form = InputFormSourceNode()
        form.show()
        form.exec_()
        value = str(form.confirm())
        print("value:", value)
        self.scene.addItem(
            SourceNodeItem(SourceNode(None, None, value, None, [250, 300]))
        )

    def on_arc_action(self):
        input_arc = Arc_Input()
        input_arc.show()
        input_arc.exec_()
        uid1 = input_arc.confirm()[0]
        uid2 = input_arc.confirm()[1]
        graph1 = graph.Graph()
        node1 = graph1.create_component(
            {
                "type": "Node",
                "name": "n1",
                "uid": uid1,
                "position_x": "900",
                "position_y": "800",
            }
        )
        node2 = graph1.create_component(
            {
                "type": "Node",
                "name": "n2",
                "uid": uid2,
                "position_x": "500",
                "position_y": "800",
            }
        )
        arc1 = Arc(graph1, None, "arc1", None, node1, node2, None, None)

        # print(arc1.nodes[0])
        print(node2.get_position())
        self.scene.addItem(ArcItem(arc1, self))
        self.scene.addItem(NodeItem(node1, None))
        self.scene.addItem(NodeItem(node2, None))

    def init_graph(self):
        graph1 = Graph()
        # self.scene.addItem(
        #     NodeItem(
        #         graph1.create_component(
        #             {
        #                 "type": "Node",
        #                 "uid": "7778da",
        #                 "name": "Node 1",
        #                 "colour": "#fd5455",
        #                 "position_x": "300",
        #                 "position_y": "300",
        #             }
        #         ),
        #         self,
        #     )
        # )
        # self.scene.addItem(
        #     NodeItem(
        #         graph1.create_component(
        #             {
        #                 "type": "Node",
        #                 "uid": "b911b2",
        #                 "name": "Node 2",
        #                 "colour": "#fd5455",
        #                 "position_x": "800",
        #                 "position_y": "800",
        #             }
        #         ),
        #         self,
        #     )
        # )
        # self.scene.addItem(
        #     NodeItem(
        #         graph1.create_component(
        #             {
        #                 "type": "Node",
        #                 "uid": "127409",
        #                 "name": "Node 3",
        #                 "colour": "#fd5455",
        #                 "position_x": "1000",
        #                 "position_y": "1000",
        #             }
        #         ),
        #         self,
        #     )
        # )
        # self.scene.addItem(
        #     ArcItem(
        #         graph1.create_component(
        #             {
        #                 "type": "Arc",
        #                 "uid": "9a2812",
        #                 "name": "Arc 1",
        #                 "colour": "#000000",
        #                 "node1_uid": "7778da",
        #                 "node2_uid": "b911b2",
        #                 "user_defined_attribute": "5",
        #                 "user_defined_arc_type": "Resistor",
        #             }
        #         ),
        #         self,
        #     )
        # )
        # self.scene.addItem(
        #     ArcItem(
        #         graph1.create_component(
        #             {
        #                 "type": "Arc",
        #                 "uid": "9a2813",
        #                 "name": "Arc 2",
        #                 "colour": "#000000",
        #                 "node1_uid": "7778da",
        #                 "node2_uid": "127409",
        #                 "user_defined_attribute": "5",
        #                 "user_defined_arc_type": "Resistor",
        #             }
        #         ),
        #         self,
        #     )
        # )
        # self.scene.addItem(
        #     ArcItem(
        #         graph1.create_component(
        #             {
        #                 "type": "Arc",
        #                 "uid": "9a2813",
        #                 "name": "Arc 2",
        #                 "colour": "#000000",
        #                 "node1_uid": "b911b2",
        #                 "node2_uid": "127409",
        #                 "user_defined_attribute": "5",
        #                 "user_defined_arc_type": "Resistor",
        #             }
        #         ),
        #         self,
        #     )
        # )

        # graph1.create_component(
        #     {
        #         "type": "Node",
        #         "uid": "7778da",
        #         "name": "Node 1",
        #         "colour": "#fd5455",
        #         "position_x": "300",
        #         "position_y": "300",
        #     }
        # )
        # graph1.create_component(
        #     {
        #         "type": "Node",
        #         "uid": "b911b2",
        #         "name": "Node 2",
        #         "colour": "#fd5455",
        #         "position_x": "800",
        #         "position_y": "800",
        #     }
        # )
        # graph1.create_component(
        #     {
        #         "type": "Node",
        #         "uid": "127409",
        #         "name": "Node 3",
        #         "colour": "#fd5455",
        #         "position_x": "1000",
        #         "position_y": "1000",
        #     }
        # )

        # graph1.create_component(
        #     {
        #         "type": "Arc",
        #         "uid": "9a2812",
        #         "name": "Arc 1",
        #         "colour": "#000000",
        #         "node1_uid": "7778da",
        #         "node2_uid": "b911b2",
        #         "user_defined_attribute": "5",
        #         "user_defined_arc_type": "Resistor",
        #     }
        # )
        # graph1.create_component(
        #     {
        #         "type": "Arc",
        #         "uid": "9a2813",
        #         "name": "Arc 2",
        #         "colour": "#000000",
        #         "node1_uid": "7778da",
        #         "node2_uid": "127409",
        #         "user_defined_attribute": "5",
        #         "user_defined_arc_type": "Resistor",
        #     }
        # )
        # graph1.create_component(
        #     {
        #         "type": "Arc",
        #         "uid": "9a2813",
        #         "name": "Arc 2",
        #         "colour": "#000000",
        #         "node1_uid": "b911b2",
        #         "node2_uid": "127409",
        #         "user_defined_attribute": "5",
        #         "user_defined_arc_type": "Resistor",
        #     }
        # )
        # graph1.print_graph_details()
        # for component in graph1.components.values():
        #     if type(component) == Node:
        #         self.scene.addItem(NodeItem(component, self))
        #     if type(component) == SourceNode:
        #         self.scene.addItem(SourceNodeItem(component, self))
        #     if type(component) == GroundNode:
        #         self.scene.addItem(GroundNodeItem(component, self))
        #     if type(component) == Arc:
        #         self.scene.addItem(ArcItem(component, self))
        #         print(component.get())

        file_name = QFileDialog.getOpenFileName(self, "Open File", ".", ("*.xml"))
        fm = FileManager()
        graph1 = fm.open_graph(str(file_name[0]))

        for component in graph1.components.values():
            if type(component) == Node:
                self.scene.addItem(NodeItem(component, self))
            if type(component) == SourceNode:
                self.scene.addItem(SourceNodeItem(component, self))
            if type(component) == GroundNode:
                self.scene.addItem(GroundNodeItem(component, self))
            if type(component) == Arc:
                self.scene.addItem(ArcItem(component, self))
                # print(component.get())


class DirectedGraphApplication:
    def __init__(self):
        app = QApplication([])
        mainwindow = GraphEditorMainWindow()
        mainwindow.show()
        sys.exit(app.exec_())

    def main(self):
        pass

    def quit(self):
        pass


if __name__ == "__main__":

    app = DirectedGraphApplication()
