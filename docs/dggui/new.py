#! /usr/bin/env python3
import sys
from sys import exit

from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QHBoxLayout,
    QVBoxLayout,
    QWidget,
)

from PySide6.QtWidgets import QMenuBar, QMenu, QPushButton
from PySide6.QtWidgets import QToolBar, QStatusBar
from PySide6.QtWidgets import QFileDialog, QMessageBox, QGraphicsItem, QGraphicsLineItem

from PySide6.QtCore import Qt, QPointF, QRectF
from PySide6.QtGui import (
    QColor,
    QPainter,
    QPainterPath,
    QPen,
    QBrush,
    QFont,
    QFontMetrics,
)
from PySide6.QtWidgets import (
    QGraphicsScene,
    QGraphicsView,
    QGraphicsEllipseItem,
    QGraphicsPathItem,
    QGraphicsSimpleTextItem,
    QGraphicsRectItem,
    QGraphicsItemGroup,
)


# ====================================================================

# = Has 3 node classes for Ground/Internal/Source
# = The mouse is now working properly

# = 3个Node class
# = 鼠标可以正常使用
# ====================================================================


class G_Node(QGraphicsEllipseItem):
    def __init__(self, x, y, r):
        super().__init__(0, 0, r, r)
        self.setPos(
            x, y
        )  # Set the position of the Node Item with respect to x-y coordinate

        gold = QColor(
            255, 215, 0
        )  # 金色 代表Current Source  #Gold to Represent Ground Node

        self.setBrush(gold)  # Set the node colour to Teal
        self.setAcceptHoverEvents(
            True
        )  # Make the node accpect the Hover event (让鼠标可以更改指针)

        # ============== Set Some Node Text ================
        self.textItem = QGraphicsSimpleTextItem("0", self)
        rect = self.textItem.boundingRect()
        rect.moveCenter(self.boundingRect().center())
        self.textItem.setPos(rect.topLeft())

    # =============== Set some Node Text ================

    # ================================================================ Mouse Event (鼠标相关) ==========================================================================================
    # mouse hover event
    # # This method is used to change the Cursor when the mouse has been point to the node
    def hoverEnterEvent(self, event):
        # Override cursor shape into Openhand to indicate that drag is allowed, also indicate that you have selected a node (read to move)
        # 如果鼠标变成一个手说明可以准备移动 , 也可以表示你选中了一个节点，可以准备有动作
        app.instance().setOverrideCursor(Qt.OpenHandCursor)

    # # This Method is used to change back the cursor when mouse is not point to the node
    def hoverLeaveEvent(self, event):
        app.instance().restoreOverrideCursor()

    # mouse click event
    def mousePressEvent(self, event):
        pass

    def mouseMoveEvent(self, event):
        # Use to update the mouse position (x,y coordinate)
        orig_cursor_position = (
            event.lastScenePos()
        )  # lastScenePos = last recorded mouse cursor position in scene coordinates //Work together with QPointF 上一次鼠标点击的点
        updated_cursor_position = (
            event.scenePos()
        )  # secnePos = Postion of the cursor new // 现在鼠标的点

        orig_position = self.scenePos()

        # To understand the calculation, check out Coordinate Implementation.pdf
        # 需要了解计算方法的话请看 坐标计算.pdf
        updated_cursor_x = (
            updated_cursor_position.x() - orig_cursor_position.x() + orig_position.x()
        )
        updated_cursor_y = (
            updated_cursor_position.y() - orig_cursor_position.y() + orig_position.y()
        )
        # QPointF = defines a point in the plane using floating point precision
        self.setPos(QPointF(updated_cursor_x, updated_cursor_y))

    def mouseReleaseEvent(self, event):
        # print x,y coordinate when release the mouse (click)
        print("x: {0}, y: {1}".format(self.pos().x(), self.pos().y()))

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
        # deleteaction.triggered.connect()

        # Excute at node Position, so it won't collide with Main windows pop-up menu
        popmenu.exec_(event.screenPos())

    # ====================================================================== 鼠标相关 =========================================================================================


class S_Node(QGraphicsEllipseItem):
    def __init__(self, x, y, r):
        super().__init__(0, 0, r, r)
        self.setPos(
            x, y
        )  # Set the position of the Node Item with respect to x-y coordinate

        teal = QColor(
            0, 128, 128
        )  # 青色 代表Current Source  #Teal to Represent Ground Node

        self.setBrush(teal)  # Set the node colour
        self.setAcceptHoverEvents(
            True
        )  # Make the node accpect the Hover event (让鼠标可以更改指针)

        # Moveable and Selectable
        self.setFlags(QGraphicsItem.ItemIsSelectable | QGraphicsItem.ItemIsMovable)

        # ============== Set Some Node Text ================
        self.textItem = QGraphicsSimpleTextItem("V", self)
        rect = self.textItem.boundingRect()
        rect.moveCenter(self.boundingRect().center())
        self.textItem.setPos(rect.topLeft())

    # =============== Set some Node Text ================

    # ================================================================ Mouse Event (鼠标相关) ==========================================================================================
    # mouse hover event
    # # This method is used to change the Cursor when the mouse has been point to the node
    def hoverEnterEvent(self, event):
        # Override cursor shape into Openhand to indicate that drag is allowed, also indicate that you have selected a node (read to move)
        # 如果鼠标变成一个手说明可以准备移动 , 也可以表示你选中了一个节点，可以准备有动作
        app.instance().setOverrideCursor(Qt.OpenHandCursor)

    # # This Method is used to change back the cursor when mouse is not point to the node
    def hoverLeaveEvent(self, event):
        app.instance().restoreOverrideCursor()

    # mouse click event
    def mousePressEvent(self, event):
        pass

    def mouseMoveEvent(self, event):
        # Use to update the mouse position (x,y coordinate)
        orig_cursor_position = (
            event.lastScenePos()
        )  # lastScenePos = last recorded mouse cursor position in scene coordinates //Work together with QPointF 上一次鼠标点击的点
        updated_cursor_position = (
            event.scenePos()
        )  # secnePos = Postion of the cursor new // 现在鼠标的点

        orig_position = self.scenePos()

        # If you want to understand the calculation, check out Coordinate Implementation.pdf
        # 想了解计算方法的话请看 坐标计算.pdf
        updated_cursor_x = (
            updated_cursor_position.x() - orig_cursor_position.x() + orig_position.x()
        )
        updated_cursor_y = (
            updated_cursor_position.y() - orig_cursor_position.y() + orig_position.y()
        )
        # QPointF = defines a point in the plane using floating point precision
        self.setPos(QPointF(updated_cursor_x, updated_cursor_y))

    def mouseReleaseEvent(self, event):
        # print x,y coordinate when release the mouse (click)
        print("x: {0}, y: {1}".format(self.pos().x(), self.pos().y()))

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
        # deleteaction.triggered.connect()

        # Excute at node Position, so it won't collide with Main windows pop-up menu
        popmenu.exec_(event.screenPos())

    # ====================================================================== 鼠标相关 =========================================================================================


class I_Node(QGraphicsEllipseItem):
    def __init__(self, x, y, r):
        super().__init__(0, 0, r, r)
        self.setPos(
            x, y
        )  # Set the position of the Node Item with respect to x-y coordinate

        pink = QColor(
            231, 84, 128
        )  # 粉色 代表Internal Node  #Pink to represent Internal Node

        self.setBrush(pink)  # Set the node colour
        self.setAcceptHoverEvents(
            True
        )  # Make the node accpect the Hover event (让鼠标可以更改指针)

        # ============== Set Some Node Text ================
        self.textItem = QGraphicsSimpleTextItem("I", self)
        rect = self.textItem.boundingRect()
        rect.moveCenter(self.boundingRect().center())
        self.textItem.setPos(rect.topLeft())

    # =============== Set some Node Text ================

    # ================================================================ Mouse Event (鼠标相关) ==========================================================================================
    # mouse hover event
    # # This method is used to change the Cursor when the mouse has been point to the node
    def hoverEnterEvent(self, event):
        # Override cursor shape into Openhand to indicate that drag is allowed, also indicate that you have selected a node (read to move)
        # 如果鼠标变成一个手说明可以准备移动 , 也可以表示你选中了一个节点，可以准备有动作
        app.instance().setOverrideCursor(Qt.OpenHandCursor)

    # # This Method is used to change back the cursor when mouse is not point to the node
    def hoverLeaveEvent(self, event):
        app.instance().restoreOverrideCursor()

    # mouse click event
    def mousePressEvent(self, event):
        pass

    def mouseMoveEvent(self, event):
        # Use to update the mouse position (x,y coordinate)
        orig_cursor_position = (
            event.lastScenePos()
        )  # lastScenePos = last recorded mouse cursor position in scene coordinates //Work together with QPointF 上一次鼠标点击的点
        updated_cursor_position = (
            event.scenePos()
        )  # secnePos = Postion of the cursor new // 现在鼠标的点

        orig_position = self.scenePos()

        # To understand the calculation, check out Coordinate Implementation.pdf
        # 需要了解计算方法的话请看 坐标计算.pdf
        updated_cursor_x = (
            updated_cursor_position.x() - orig_cursor_position.x() + orig_position.x()
        )
        updated_cursor_y = (
            updated_cursor_position.y() - orig_cursor_position.y() + orig_position.y()
        )
        # QPointF = defines a point in the plane using floating point precision
        self.setPos(QPointF(updated_cursor_x, updated_cursor_y))

    def mouseReleaseEvent(self, event):
        # print x,y coordinate when release the mouse (click)
        print("x: {0}, y: {1}".format(self.pos().x(), self.pos().y()))

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
        # deleteaction.triggered.connect()

        # Excute at node Position, so it won't collide with Main windows pop-up menu
        popmenu.exec_(event.screenPos())

    # ====================================================================== Mouse Event (鼠标相关) =========================================================================================


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("GUI Editor")
        self.mainLayout = QVBoxLayout()

        # ====================================================================================
        #      All from Example.py       but all tiggered is disabled
        # Setup menu bar & File menu
        self.fileMenu = self.menuBar().addMenu("&File")
        self.openMenuAction = self.fileMenu.addAction("&Open")
        # self.openMenuAction.triggered.connect(self.on_open_action)
        self.fileMenu.addSeparator()
        self.fileMenuAction = self.fileMenu.addAction("&Save")
        self.fileMenu.addSeparator()
        self.fileMenuAction = self.fileMenu.addAction("&Save As")
        self.fileMenu.addSeparator()
        self.quitMenuAction = self.fileMenu.addAction("&Quit")
        # self.quitMenuAction.triggered.connect(self.on_quit_action)

        # Setup Tools menu
        self.toolsMenu = self.menuBar().addMenu("&Tools")
        self.preferencesMenuAction = self.toolsMenu.addAction("&Preferences")
        # self.preferencesMenuAction.triggered.connect(self.on_preferences_action)

        # Setup About menu
        self.aboutMenu = self.menuBar().addMenu("&About")
        self.aboutMenuAction = self.aboutMenu.addAction("&About")
        # self.aboutMenuAction.triggered.connect(self.on_about_action)

        # Create main toolbar
        self.mainToolBar = QToolBar()
        self.mainToolBar.setMovable(False)
        self.newToolButton = self.mainToolBar.addAction("New")
        self.newToolButton = self.mainToolBar.addAction("Insert")
        self.newToolButton = self.mainToolBar.addAction("Zoom In")
        self.newToolButton = self.mainToolBar.addAction("Zoom Out")
        # self.openToolButton.triggered.connect(self.on_open_action)
        # self.openToolButton.triggered.connect(self.on_insert_action)
        # self.openToolButton.triggered.connect(self.on_insert_action)
        self.addToolBar(self.mainToolBar)
        self.mainLayout.addWidget(self.mainToolBar)

        # =======================================================================================

        self.graphicsscene = QGraphicsScene(0, 0, 500, 500, self)

        # ==================================
        # Add items here

        groundnode = G_Node(
            120, 120, 40
        )  # x , y , r Create a node with radius 40 and at (120,120)
        self.graphicsscene.addItem(groundnode)  # additem to add the node into the scene

        internalnode1 = I_Node(200, 200, 40)
        self.graphicsscene.addItem(internalnode1)

        sourcenode1 = S_Node(300, 300, 40)
        self.graphicsscene.addItem(sourcenode1)

        # ==================================

        # Initialise QGraphicsView ()
        self.graphicsView = QGraphicsView(self.graphicsscene)
        self.mainLayout.addWidget(self.graphicsView)
        self.mainWidget = QWidget()
        self.mainWidget.setLayout(self.mainLayout)
        self.setCentralWidget(self.mainWidget)
        self.graphicsView.setRenderHints(QPainter.Antialiasing)

        # Right click the blank Area to give some options for better interafce with User
        # Might not needed 可能不需要

    def contextMenuEvent(self, event):
        contextmenu = QMenu(self)
        newAction = contextmenu.addAction("New")
        openAction = contextmenu.addAction("Open")
        quirAction = contextmenu.addAction("Save")
        quirAction = contextmenu.addAction("Copy")
        quirAction = contextmenu.addAction("Past")
        quirAction = contextmenu.addAction("Help...")

        action = contextmenu.exec_(self.mapToGlobal(event.pos()))


if __name__ == "__main__":
    app = QApplication(sys.argv)  # app.instance can be used for the hover event
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
