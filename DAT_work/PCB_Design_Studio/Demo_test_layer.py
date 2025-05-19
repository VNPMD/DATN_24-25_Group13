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

        # Khởi tạo biến vẽ
        self.current_layer = "top_copper"  # Default layer for drawing
        self.drawing = False
        self.start_point = QPointF()
        self.drawing_enabled = True  # Toggle for enabling/disabling drawing
        self.drawing_mode = "line"

        # Create a QGraphicsScene
        self.scene = QGraphicsScene(self)
        self.scene.setSceneRect(0, 0, 1000, 1000)

        # LayerManager
        self.layer_manager = LayerManager(self.scene)

        # QGraphicsView
        self.view = QGraphicsView(self.scene, self)
        self.setCentralWidget(self.view)

        # Layer controls
        self.create_layer_controls()

        # Toolbar
        self.create_toolbar()

    def create_layer_controls(self):
        dock = QDockWidget("Layer Controls", self)
        dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)

        dock_widget = QWidget()
        layout = QVBoxLayout()

        self.layer_tree = QTreeWidget()
        self.layer_tree.setHeaderLabels(["Layer", "Color", "Visible", "Lock"])
        self.layer_tree.setColumnWidth(0, 150)
        self.layer_tree.setColumnWidth(1, 50)
        self.layer_tree.setColumnWidth(2, 50)
        self.layer_tree.setColumnWidth(3, 50)
        self.layer_tree.header().setDefaultAlignment(Qt.AlignCenter)

        self.populate_layer_tree()
        layout.addWidget(self.layer_tree)

        self.layer_selector = QComboBox(self)
        self.layer_selector.addItems(self.layer_manager.layers.keys())
        self.layer_selector.currentTextChanged.connect(self.on_layer_selected)
        layout.addWidget(self.layer_selector)

        dock_widget.setLayout(layout)
        dock.setWidget(dock_widget)
        self.addDockWidget(Qt.LeftDockWidgetArea, dock)

    def create_toolbar(self):
        toolbar = QToolBar("Drawing Tools", self)
        self.addToolBar(Qt.TopToolBarArea, toolbar)

        toggle_drawing_action = QAction(QIcon(), "Toggle Drawing", self)
        toggle_drawing_action.setCheckable(True)
        toggle_drawing_action.setChecked(self.drawing_enabled)
        toggle_drawing_action.triggered.connect(self.toggle_drawing_mode)
        toolbar.addAction(toggle_drawing_action)

        clear_scene_action = QAction(QIcon(), "Clear Scene", self)
        clear_scene_action.triggered.connect(self.clear_scene)
        toolbar.addAction(clear_scene_action)

        line_mode_action = QAction(QIcon(), "Draw Line", self)
        line_mode_action.triggered.connect(lambda: self.set_drawing_mode("line"))
        toolbar.addAction(line_mode_action)

        circle_mode_action = QAction(QIcon(), "Draw Circle", self)
        circle_mode_action.triggered.connect(lambda: self.set_drawing_mode("circle"))
        toolbar.addAction(circle_mode_action)

    def set_drawing_mode(self, mode):
        self.drawing_mode = mode

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and self.drawing_enabled:
            self.drawing = True
            self.start_point = self.view.mapToScene(event.pos())

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton and self.drawing and self.drawing_enabled:
            self.drawing = False
            end_point = self.view.mapToScene(event.pos())

            pen = QPen(self.layer_manager.layers[self.current_layer]["color"])
            if self.drawing_mode == "line":
                line = self.scene.addLine(
                    self.start_point.x(), self.start_point.y(),
                    end_point.x(), end_point.y(),
                    pen
                )
                self.layer_manager.add_item_to_layer(self.current_layer, line)
            elif self.drawing_mode == "circle":
                radius = ((end_point.x() - self.start_point.x()) ** 2 + (end_point.y() - self.start_point.y()) ** 2) ** 0.5
                circle = self.scene.addEllipse(
                    self.start_point.x() - radius, self.start_point.y() - radius,
                    2 * radius, 2 * radius,
                    pen
                )
                self.layer_manager.add_item_to_layer(self.current_layer, circle)

    def populate_layer_tree(self):
        parent_layers = ["Top", "Bottom"]
        child_layers = [
            {"name": "Silk", "color": QColor("lightgray")},
            {"name": "Electric", "color": QColor("blue")},
            {"name": "Route", "color": QColor("green")},
            {"name": "Plane", "color": QColor("cyan")},
            {"name": "PadStack", "color": QColor("yellow")},
            {"name": "ViaStack", "color": QColor("magenta")},
            {"name": "Paste", "color": QColor("orange")},
            {"name": "Solder", "color": QColor("red")},
            {"name": "Assembly", "color": QColor("purple")},
            {"name": "Keepout(Route)", "color": QColor("darkblue")},
            {"name": "Keepout(Drill)", "color": QColor("darkgreen")},
            {"name": "Keepout(Component)", "color": QColor("darkred")},
            {"name": "HeightLimit", "color": QColor("brown")},
            {"name": "DesignRule", "color": QColor("pink")},
            {"name": "Dimension", "color": QColor("gray")},
        ]

        for parent_name in parent_layers:
            parent_item = QTreeWidgetItem(self.layer_tree)
            parent_item.setText(0, parent_name)
            for child in child_layers:
                child_name = child["name"]
                layer_color = child["color"]
                child_item = QTreeWidgetItem(parent_item)
                child_item.setText(0, child_name)

                color_label = QLabel()
                color_label.setStyleSheet(f"background-color: {layer_color.name()};")
                color_label.mousePressEvent = self.create_color_change_handler(child_name, color_label)
                self.layer_tree.setItemWidget(child_item, 1, color_label)

                visibility_widget = QWidget()
                visibility_layout = QHBoxLayout(visibility_widget)
                visibility_layout.setContentsMargins(0, 0, 0, 0)
                visibility_layout.setAlignment(Qt.AlignCenter)
                visibility_checkbox = QCheckBox()
                visibility_checkbox.setChecked(True)
                visibility_checkbox.stateChanged.connect(
                    lambda state, name=child_name: self.toggle_layer_visibility(name, state)
                )
                visibility_layout.addWidget(visibility_checkbox)
                self.layer_tree.setItemWidget(child_item, 2, visibility_widget)

                lock_widget = QWidget()
                lock_layout = QHBoxLayout(lock_widget)
                lock_layout.setContentsMargins(0, 0, 0, 0)
                lock_layout.setAlignment(Qt.AlignCenter)
                lock_checkbox = QCheckBox()
                lock_checkbox.setChecked(False)
                lock_layout.addWidget(lock_checkbox)
                self.layer_tree.setItemWidget(child_item, 3, lock_widget)

    def create_color_change_handler(self, layer_name, color_label):
        def handler(event):
            new_color = QColorDialog.getColor()
            if new_color.isValid():
                color_label.setStyleSheet(f"background-color: {new_color.name()};")
                # Update color in LayerManager if exists
                if layer_name in self.layer_manager.layers:
                    self.layer_manager.layers[layer_name]["color"] = new_color
                    for item in self.layer_manager.layers[layer_name]["items"]:
                        if hasattr(item, "setBrush"):
                            item.setBrush(new_color)
                        elif hasattr(item, "setPen"):
                            pen = item.pen()
                            pen.setColor(new_color)
                            item.setPen(pen)
        return handler

    def toggle_layer_visibility(self, layer_name, state):
        visible = state == Qt.Checked
        if layer_name in self.layer_manager.layers:
            for item in self.layer_manager.layers[layer_name]["items"]:
                item.setVisible(visible)

    def on_layer_selected(self, layer_name):
        self.current_layer = layer_name

    def toggle_drawing_mode(self, enabled):
        self.drawing_enabled = enabled

    def clear_scene(self):
        self.scene.clear()
        for layer in self.layer_manager.layers.values():
            layer["items"].clear()

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = LayerViewer()
    window.show()
    sys.exit(app.exec_())