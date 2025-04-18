from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QGraphicsView, QGraphicsScene, QVBoxLayout, QWidget, QPushButton, QComboBox, QColorDialog,
    QDockWidget, QTreeWidget, QTreeWidgetItem, QHBoxLayout, QLabel, QCheckBox, QToolBar, QAction
)
from PyQt5.QtGui import QColor, QPen, QIcon
from PyQt5.QtCore import Qt, QPointF
from layer_manager import LayerManager  # Import LayerManager

class LayerViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Layer Viewer")
        self.setGeometry(100, 100, 1200, 800)

        # Create a QGraphicsScene
        super().__init__()
        self.setWindowTitle("Layer Viewer")
        self.setGeometry(100, 100, 1200, 800)

        # Initialize variables for drawing
        self.current_layer = "top_copper"  # Default layer for drawing
        self.drawing = False
        self.start_point = QPointF()
        self.drawing_enabled = True  # Toggle for enabling/disabling drawing

        # Create a QGraphicsScene
        self.scene = QGraphicsScene(self)
        self.scene.setSceneRect(0, 0, 1000, 1000)

        # Initialize LayerManager with the scene
        self.layer_manager = LayerManager(self.scene)

        # Create a QGraphicsView to display the scene
        self.view = QGraphicsView(self.scene, self)
        self.setCentralWidget(self.view)

        # Create a dockable widget for layer controls
        self.create_layer_controls()

        # Create a toolbar for drawing tools
        self.create_toolbar()

        # Variables for drawing
        self.current_layer = "top_copper"  # Default layer for drawing
        self.drawing = False
        self.start_point = QPointF()
        self.drawing_enabled = True  # Toggle for enabling/disabling drawing

    def create_layer_controls(self):
        """
        Create a dockable widget for layer selection and controls.
        """
        dock = QDockWidget("Layer Controls", self)
        dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)

        # Create a widget to hold the controls
        dock_widget = QWidget()
        layout = QVBoxLayout()

        # Create a tree widget for layers
        self.layer_tree = QTreeWidget()
        self.layer_tree.setHeaderLabels(["Layer", "Color", "Visible"])
        self.populate_layer_tree()
        layout.addWidget(self.layer_tree)

        # Create a dropdown (QComboBox) for selecting the active layer
        self.layer_selector = QComboBox(self)
        self.layer_selector.addItems(self.layer_manager.layers.keys())  # Add all layer names to the dropdown
        self.layer_selector.currentTextChanged.connect(self.on_layer_selected)
        layout.addWidget(self.layer_selector)

        # Set the layout for the dock widget
        dock_widget.setLayout(layout)
        dock.setWidget(dock_widget)

        # Add the dock to the main window
        self.addDockWidget(Qt.LeftDockWidgetArea, dock)

    def create_toolbar(self):
        """
        Create a toolbar for drawing tools.
        """
        toolbar = QToolBar("Drawing Tools", self)
        self.addToolBar(Qt.TopToolBarArea, toolbar)

        # Toggle drawing mode
        toggle_drawing_action = QAction(QIcon(), "Toggle Drawing", self)
        toggle_drawing_action.setCheckable(True)
        toggle_drawing_action.setChecked(self.drawing_enabled)
        toggle_drawing_action.triggered.connect(self.toggle_drawing_mode)
        toolbar.addAction(toggle_drawing_action)

        # Clear the scene
        clear_scene_action = QAction(QIcon(), "Clear Scene", self)
        clear_scene_action.triggered.connect(self.clear_scene)
        toolbar.addAction(clear_scene_action)

        # Switch to line drawing mode
        line_mode_action = QAction(QIcon(), "Draw Line", self)
        line_mode_action.triggered.connect(lambda: self.set_drawing_mode("line"))
        toolbar.addAction(line_mode_action)

        # Switch to circle drawing mode
        circle_mode_action = QAction(QIcon(), "Draw Circle", self)
        circle_mode_action.triggered.connect(lambda: self.set_drawing_mode("circle"))
        toolbar.addAction(circle_mode_action)

    def set_drawing_mode(self, mode):
        """
        Set the drawing mode (line or circle).
        """
        self.drawing_mode = mode

    def mouseReleaseEvent(self, event):
        """
        Handle mouse release events for drawing.
        """
        if event.button() == Qt.LeftButton and self.drawing and self.drawing_enabled:
            self.drawing = False
            end_point = self.view.mapToScene(event.pos())

            if self.drawing_mode == "line":
                # Draw a line on the current layer
                pen = QPen(self.layer_manager.layers[self.current_layer]["color"])
                line = self.scene.addLine(
                    self.start_point.x(), self.start_point.y(),
                    end_point.x(), end_point.y(),
                    pen
                )
                self.layer_manager.add_item_to_layer(self.current_layer, line)

            elif self.drawing_mode == "circle":
                # Draw a circle on the current layer
                pen = QPen(self.layer_manager.layers[self.current_layer]["color"])
                radius = ((end_point.x() - self.start_point.x()) ** 2 + (end_point.y() - self.start_point.y()) ** 2) ** 0.5
                circle = self.scene.addEllipse(
                    self.start_point.x() - radius, self.start_point.y() - radius,
                    2 * radius, 2 * radius,
                    pen
                )
                self.layer_manager.add_item_to_layer(self.current_layer, circle)
    def populate_layer_tree(self):
        """
        Populate the tree widget with layers and their controls.
        """
        for layer_name, layer_data in self.layer_manager.layers.items():
            # Create a tree item for the layer
            layer_item = QTreeWidgetItem(self.layer_tree)
            layer_item.setText(0, layer_name)

            # Add a color label with a click event to change the color
            color_label = QLabel()
            color_label.setStyleSheet(f"background-color: {layer_data['color'].name()};")
            color_label.mousePressEvent = self.create_color_change_handler(layer_name, color_label)
            self.layer_tree.setItemWidget(layer_item, 1, color_label)

            # Add a visibility checkbox
            visibility_checkbox = QCheckBox()
            visibility_checkbox.setChecked(True)
            visibility_checkbox.stateChanged.connect(lambda state, name=layer_name: self.toggle_layer_visibility(name, state))
            self.layer_tree.setItemWidget(layer_item, 2, visibility_checkbox)
    def create_color_change_handler(self, layer_name, color_label):
        """
        Create a handler for changing the color of a specific layer.
        """
        def handler(event):
            self.change_layer_color(layer_name, color_label)
        return handler
    def change_layer_color(self, layer_name, color_label):
        """
        Open a color dialog to change the color of the selected layer.
        """
        color = QColorDialog.getColor()
        if color.isValid():
            # Update the layer's color
            self.layer_manager.layers[layer_name]["color"] = color

            # Update the color label in the tree
            color_label.setStyleSheet(f"background-color: {color.name()};")

            # Update the color of all items in the layer
            for item in self.layer_manager.layers[layer_name]["items"]:
                if hasattr(item, "setBrush"):  # Check if the item supports setting a brush
                    item.setBrush(color)
                elif hasattr(item, "setPen"):  # Check if the item supports setting a pen
                    pen = item.pen()
                    pen.setColor(color)
                    item.setPen(pen)

    def toggle_layer_visibility(self, layer_name, state):
        """
        Toggle the visibility of a layer.
        """
        visible = state == Qt.Checked
        for item in self.layer_manager.layers[layer_name]["items"]:
            item.setVisible(visible)

    def on_layer_selected(self, layer_name):
        """
        Handle layer selection from the dropdown.
        """
        self.current_layer = layer_name  # Update the current layer for drawing

    def toggle_drawing_mode(self, enabled):
        """
        Enable or disable drawing mode.
        """
        self.drawing_enabled = enabled

    def clear_scene(self):
        """
        Clear all items from the scene.
        """
        self.scene.clear()
        for layer in self.layer_manager.layers.values():
            layer["items"].clear()

    def mousePressEvent(self, event):
        """
        Handle mouse press events for drawing.
        """
        if event.button() == Qt.LeftButton and self.drawing_enabled:
            self.drawing = True
            self.start_point = self.view.mapToScene(event.pos())

    def mouseReleaseEvent(self, event):
        """
        Handle mouse release events for drawing.
        """
        if event.button() == Qt.LeftButton and self.drawing and self.drawing_enabled:
            self.drawing = False
            end_point = self.view.mapToScene(event.pos())

            # Draw a line on the current layer
            pen = QPen(self.layer_manager.layers[self.current_layer]["color"])
            line = self.scene.addLine(
                self.start_point.x(), self.start_point.y(),
                end_point.x(), end_point.y(),
                pen
            )
            self.layer_manager.add_item_to_layer(self.current_layer, line)

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = LayerViewer()
    window.show()
    sys.exit(app.exec_())