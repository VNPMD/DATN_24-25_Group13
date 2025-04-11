# import json
# import sys
# import traceback
#
# import data
# import self
# from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
#                              QToolBar, QAction, QTabWidget, QGraphicsView, QGraphicsScene,
#                              QGraphicsItem, QDockWidget, QTreeWidget, QTreeWidgetItem,
#                              QGraphicsRectItem, QListWidget, QPushButton, QLabel, QLineEdit,
#                              QComboBox, QGridLayout, QMessageBox, QGraphicsEllipseItem, QFileDialog, QGraphicsLineItem,
#                              QColorDialog)
# from PyQt5.QtGui import QIcon, QPen, QBrush, QColor, QFont, QPainter, QWheelEvent
# from PyQt5.QtCore import Qt, QRectF, QPointF
#
#
# # class ZoomableGraphicsView(QGraphicsView):
# #     def __init__(self, scene):
# #         super().__init__(scene)
# #         self.setRenderHint(QPainter.Antialiasing)
# #         self.setDragMode(QGraphicsView.RubberBandDrag)
# #
# #         # Enable mouse tracking for hover events
# #         self.setMouseTracking(True)
# #
# #         # zoom and pan variables
# #         self.zoom.factor = 1.0
# #         self.is_panning = False
# #         self.last_pan_point = QPointF()
# #     def wheelEvent(self, event: QWheelEvent):
# #         # Zoom functionlity
# #         zoom_in_factor = 1.25
# #         zoom_out_factor = 1/ zoom_in_factor
# #
# #         old_pos = self.mapToScene(event.pos())
# #
# #         if event.angleDelta().y() > 0:
# #             # zoom in
# #              zoom_factor = zoom_in_factor
# #             self.zoom_factor = zoom_in_factor * self.zoom_factor
# #
# #         else:
# #             #zoom out
# #         zoom_factor = zoom_out_factor
# #         self.zoom_factor *= zoom_out_factor
# #
# #         self.zoom_factor = max(0.1, min(self.zoom_factor, 10))
# #         self.resetTransform()
# #         self.scale(self.zoom_factor, self.zoom_factor)
# #
# #         # get the position after scaling
# #         new_pos = self.mapToScene(event.pos())
# #         # move the scene to keep the mouse point constant
# #         delta = new_pos - old_pos
# #         self.translate(delta.x(), delta.y())
# #
# #
# #
#
#
#
#
# class PCBDesignApp(QMainWindow):
#     def __init__(self):
#         try:
#             super().__init__()
#             self.setWindowTitle('PCB Design Studio')
#             self.setGeometry(100, 100, 1200, 800)
#
#             # Initialize UI components
#             self.init_ui()
#         except Exception as e:
#             self.show_error_message("Initialization Error", str(e))
#
#     def init_ui(self):
#         try:
#             # Create main layout components
#             self.create_menu_bar()
#             self.create_toolbar()
#             self.create_left_sidebar()
#             self.create_right_sidebar()
#             self.create_central_canvas()
#             self.create_bottom_panel()
#         except Exception as e:
#             self.show_error_message("UI Creation Error", str(e))
#
#     def create_menu_bar(self):
#         menubar = self.menuBar()
#
#         # File Menu
#         file_menu = menubar.addMenu('File')
#         file_menu.addAction('New Project')
#         file_menu.addAction('Open Project')
#         file_menu.addAction('Save')
#
#         # Edit Menu
#         edit_menu = menubar.addMenu('Edit')
#         edit_menu.addAction('Undo')
#         edit_menu.addAction('Redo')
#
#         # Design Menu
#         design_menu = menubar.addMenu('Design')
#         design_menu.addAction('Create Footprint')
#         design_menu.addAction('Layer Manager')
#
#     def create_toolbar(self):
#         toolbar = QToolBar('Design Tools')
#         self.addToolBar(toolbar)
#
#         tools = [
#             'Select', 'Move', 'Draw',
#             'Place Component', 'Route'
#         ]
#
#         for name in tools:
#             action = toolbar.addAction(name)
#
#     def create_left_sidebar(self):
#         dock = QDockWidget('Component Library', self)
#         dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
#
#         tree = QTreeWidget()
#         tree.setHeaderLabel('Components')
#
#         categories = [
#             ('Passive', ['Resistor', 'Capacitor', 'Inductor']),
#             ('Active', ['Transistor', 'IC', 'Diode']),
#             ('Connectors', ['USB', 'HDMI', 'Pin Header'])
#         ]
#
#         for category, components in categories:
#             cat_item = QTreeWidgetItem(tree, [category])
#             for component in components:
#                 QTreeWidgetItem(cat_item, [component])
#
#         dock.setWidget(tree)
#         self.addDockWidget(Qt.LeftDockWidgetArea, dock)
#
#     def create_right_sidebar(self):
#         dock = QDockWidget('Properties', self)
#         dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
#
#         properties_widget = QWidget()
#         layout = QGridLayout()
#
#         properties = [
#             ('Component Type:', QComboBox()),
#             ('Footprint:', QLineEdit()),
#             ('Value:', QLineEdit()),
#             ('Tolerance:', QComboBox())
#         ]
#
#         for i, (label, widget) in enumerate(properties):
#             layout.addWidget(QLabel(label), i, 0)
#             layout.addWidget(widget, i, 1)
#
#         properties_widget.setLayout(layout)
#         dock.setWidget(properties_widget)
#         self.addDockWidget(Qt.RightDockWidgetArea, dock)
#
#     def create_central_canvas(self):
#         self.canvas_widget = QTabWidget()
#
#         scene = QGraphicsScene(self)
#         scene.setSceneRect(0, 0, 2000, 2000)
#
#         view = QGraphicsView(scene)
#         view.setRenderHint(QPainter.Antialiasing)
#         view.setDragMode(QGraphicsView.RubberBandDrag)
#
#         self.add_grid(scene)
#
#         self.canvas_widget.addTab(view, 'PCB Design')
#         self.setCentralWidget(self.canvas_widget)
#
#     def add_grid(self, scene):
#         grid_color = QColor(240, 240, 240)
#         grid_spacing = 10
#
#         for x in range(0, 2000, grid_spacing):
#             scene.addLine(x, 0, x, 2000, QPen(grid_color))
#
#         for y in range(0, 2000, grid_spacing):
#             scene.addLine(0, y, 2000, y, QPen(grid_color))
#
#     def create_bottom_panel(self):
#         dock = QDockWidget('Messages', self)
#         dock.setAllowedAreas(Qt.BottomDockWidgetArea)
#
#         message_list = QListWidget()
#         message_list.addItems([
#             'Welcome to PCB Design Studio',
#             'Ready to start designing'
#         ])
#
#         dock.setWidget(message_list)
#         self.addDockWidget(Qt.BottomDockWidgetArea, dock)
#
#     def show_error_message(self, title, message):
#         error_dialog = QMessageBox()
#         error_dialog.setIcon(QMessageBox.Critical)
#         error_dialog.setWindowTitle(title)
#         error_dialog.setText(message)
#         error_dialog.setDetailedText(traceback.format_exc())
#         error_dialog.exec_()
#
#
# class DrawingApp(QMainWindow):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("PyQt6 Multi-Layer Drawing")
#         self.setGeometry(100, 100, 800, 600)
#         self.setCentralWidget(self.drawing_window)
#
#         self.init_ui()
#
#     def init_ui(self):
#         toolbar = self.addToolBar("Toolbar")
#
#         draw_line_action = QAction("Draw Line", self)
#         draw_line_action.triggered.connect(lambda: self.set_drawing_mode("line"))
#         toolbar.addAction(draw_line_action)
#
#         draw_rect_action = QAction("Draw Rectangle", self)
#         draw_rect_action.triggered.connect(lambda: self.set_drawing_mode("rect"))
#         toolbar.addAction(draw_rect_action)
#
#         draw_circle_action = QAction("Draw Circle", self)
#         draw_circle_action.triggered.connect(lambda: self.set_drawing_mode("circle"))
#         toolbar.addAction(draw_circle_action)
#
#         color_action = QAction("Choose Color", self)
#         color_action.triggered.connect(self.choose_color)
#         toolbar.addAction(color_action)
#
#         save_action = QAction("Save", self)
#         save_action.triggered.connect(self.save_drawing)
#         toolbar.addAction(save_action)
#
#         load_action = QAction("Load", self)
#         load_action.triggered.connect(self.load_drawing)
#         toolbar.addAction(load_action)
#
#     def set_drawing_mode(self, mode):
#         self.drawing_window.drawing_mode = mode
#
#     def choose_color(self):
#         color = QColorDialog.getColor()
#         if color.isValid():
#             self.drawing_window.selected_color = color
#
#     def save_drawing(self):
#         file_path, _ = QFileDialog.getSaveFileName(self, "Save File", "", "JSON Files (*.json)")
#         if file_path:
#             data = {}
#             for layer, items in self.drawing_window.layers.items():
#                 data[layer] = []
#                 for item in items:
#                     if isinstance(item, QGraphicsLineItem):
#                         data[layer].append(
#                             {"type": "line", "x1": item.line().x1(), "y1": item.line().y1(), "x2": item.line().x2(),
#                              "y2": item.line().y2()})
#                     elif isinstance(item, QGraphicsRectItem):
#                         data[layer].append(
#                             {"type": "rect", "x": item.rect().x(), "y": item.rect().y(), "width": item.rect().width(),
#                              "height": item.rect().height()})
#                     elif isinstance(item, QGraphicsEllipseItem):
#                         data[layer].append(
#                             {"type": "circle", "x": item.rect().x(), "y": item.rect().y(), "width": item.rect().width(),
#                              "height": item.rect().height()})
#             with open(file_path, "w") as f:
#                 json.dump(data, f)
#
#     def load_drawing(self):
#         file_path, _ = QFileDialog.getOpenFileName(self, "Open File", "", "JSON Files (*.json)")
#         if file_path:
#             with open(file_path, "r") as f:
#                 data = json.load(f)
#
#
#
#
# for layer, items in data.items():
#     for item in items:
#         if item["type"] == "line":
#             new_item = QGraphicsLineItem(item["x1"], item["y1"], item["x2"], item["y2"])
#         elif item["type"] == "rect":
#             new_item = QGraphicsRectItem(item["x"], item["y"], item["width"], item["height"])
#         elif item["type"] == "circle":
#             new_item = QGraphicsEllipseItem(item["x"], item["y"], item["width"], item["height"])
#         new_item.setPen(QPen(Qt.GlobalColor.black, 2))
#         self.drawing_window.scene.addItem(new_item)
#         self.drawing_window.layers[int(layer)].append(new_item)
# def main():
#     try:
#         app = QApplication(sys.argv)
#         pcb_app = PCBDesignApp()
#         pcb_app.show()
#         sys.exit(app.exec_())
#     except Exception as e:
#         print(f"Fatal Error: {e}")
#         traceback.print_exc()
#
#
# if __name__ == '__main__':
#     main()


import json
import sys
import traceback
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                             QToolBar, QAction, QTabWidget, QGraphicsView, QGraphicsScene,
                             QGraphicsItem, QDockWidget, QTreeWidget, QTreeWidgetItem,
                             QGraphicsRectItem, QListWidget, QPushButton, QLabel, QLineEdit,
                             QComboBox, QGridLayout, QMessageBox, QGraphicsEllipseItem, QFileDialog, QGraphicsLineItem,
                             QColorDialog, QMenuBar, QMenu, QGroupBox, QCheckBox, QGraphicsPathItem, QDialog)
from PyQt5.QtGui import QIcon, QPen, QBrush, QColor, QFont, QPainter, QPainterPath
from PyQt5.QtCore import Qt, QRectF, QPointF


class ZoomableGraphicsView(QGraphicsView):
    def __init__(self, scene):
        super().__init__(scene)
        self.setRenderHint(QPainter.Antialiasing)
        self.setDragMode(QGraphicsView.RubberBandDrag)

        self.setMouseTracking(True)
        self.zoom_factor = 1.0
        self.is_panning = False
        self.last_pan_point = QPointF()

    def wheelEvent(self, event):
        zoom_in_factor = 1.25
        zoom_out_factor = 1 / zoom_in_factor

        old_pos = self.mapToScene(event.pos())

        if event.angleDelta().y() > 0:
            zoom_factor = zoom_in_factor
            self.zoom_factor *= zoom_in_factor
        else:
            zoom_factor = zoom_out_factor
            self.zoom_factor *= zoom_out_factor

        self.zoom_factor = max(0.1, min(self.zoom_factor, 10))
        self.resetTransform()
        self.scale(self.zoom_factor, self.zoom_factor)

        new_pos = self.mapToScene(event.pos())
        delta = new_pos - old_pos
        self.translate(delta.x(), delta.y())


class DrawingApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt5 Multi-Layer Drawing")
        self.setGeometry(100, 100, 800, 600)

        self.scene = QGraphicsScene()
        self.drawing_window = QGraphicsView(self.scene)
        self.setCentralWidget(self.drawing_window)

        self.drawing_mode = None
        self.selected_color = QColor(Qt.black)
        self.layers = {0: []}

        self.current_item = None
        self.start_point = None

        # Assign event handlers correctly
        self.drawing_window.setMouseTracking(True)  # Enable mouse tracking
        self.drawing_window.viewport().installEventFilter(self)

    def eventFilter(self, source, event):
        if source is self.drawing_window.viewport():
            if event.type() == event.MouseButtonPress:
                self.mouse_press(event)
                return True  # Trả về True để báo hiệu đã xử lý xong sự kiện
            elif event.type() == event.MouseButtonRelease:
                self.mouse_release(event)
                return True
            elif event.type() == event.MouseMove:
                self.mouse_move(event)
                return True
        return super().eventFilter(source, event)  # Không chặn các sự kiện khác

    # Fix the mouse_press method in DrawingApp class
    def mouse_press(self, event):
        if event.button() == Qt.LeftButton:
            self.start_point = self.drawing_window.mapToScene(event.pos())
            if self.drawing_mode == "line":
                # Create a line with proper initialization (from start point to itself initially)
                self.current_item = QGraphicsLineItem(
                    self.start_point.x(), self.start_point.y(),
                    self.start_point.x(), self.start_point.y()
                )
                self.current_item.setPen(QPen(self.selected_color, 2))
                self.scene.addItem(self.current_item)
            elif self.drawing_mode == "rect":
                # Create an empty rectangle at the start point
                self.current_item = QGraphicsRectItem(
                    QRectF(self.start_point.x(), self.start_point.y(), 0, 0)
                )
                self.current_item.setPen(QPen(self.selected_color, 2))
                self.scene.addItem(self.current_item)
            elif self.drawing_mode == "circle":
                # Create an empty ellipse at the start point
                self.current_item = QGraphicsEllipseItem(
                    QRectF(self.start_point.x(), self.start_point.y(), 0, 0)
                )
                self.current_item.setPen(QPen(self.selected_color, 2))
                self.scene.addItem(self.current_item)

    def mouse_release(self, event):
        if self.current_item:
            self.layers[0].append(self.current_item)  # Lưu lại vào danh sách
        self.current_item = None

    def mouse_move(self, event):
        if self.current_item and self.start_point:
            self.end_point = self.drawing_window.mapToScene(event.pos())
            if isinstance(self.current_item, QGraphicsLineItem):
                self.current_item.setLine(self.start_point.x(), self.start_point.y(),
                                          self.end_point.x(), self.end_point.y())
            elif isinstance(self.current_item, QGraphicsRectItem) or isinstance(self.current_item,
                                                                                QGraphicsEllipseItem):
                rect = QRectF(self.start_point, self.end_point).normalized()
                self.current_item.setRect(rect)
        return True

    def choose_color(self):
        color = QColorDialog.getColor(self.selected_color, self, "Choose Color")
        if color.isValid():
            self.selected_color = color


class PadEditor(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Pad Editor")
        self.current_pad = None
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Pad type selection
        type_layout = QHBoxLayout()
        type_layout.addWidget(QLabel("Pad Type:"))
        self.pad_type_combo = QComboBox()
        self.pad_type_combo.addItems(["THT (Through Hole)", "SMD (Surface Mount)", "NPTH (Non-Plated)"])
        self.pad_type_combo.currentIndexChanged.connect(self.update_pad_preview)
        type_layout.addWidget(self.pad_type_combo)
        layout.addLayout(type_layout)

        # Pad shape selection
        shape_layout = QHBoxLayout()
        shape_layout.addWidget(QLabel("Shape:"))
        self.pad_shape_combo = QComboBox()
        self.pad_shape_combo.addItems(["Circle", "Rectangle", "Oval", "Custom"])
        self.pad_shape_combo.currentIndexChanged.connect(self.update_pad_preview)
        shape_layout.addWidget(self.pad_shape_combo)
        layout.addLayout(shape_layout)

        # Dimensions
        dims_group = QGroupBox("Dimensions")
        dims_layout = QGridLayout()

        # Width
        dims_layout.addWidget(QLabel("Width:"), 0, 0)
        self.width_edit = QLineEdit("1.5")
        dims_layout.addWidget(self.width_edit, 0, 1)
        dims_layout.addWidget(QLabel("mm"), 0, 2)

        # Height
        dims_layout.addWidget(QLabel("Height:"), 1, 0)
        self.height_edit = QLineEdit("1.5")
        dims_layout.addWidget(self.height_edit, 1, 1)
        dims_layout.addWidget(QLabel("mm"), 1, 2)

        # Hole diameter (for THT)
        dims_layout.addWidget(QLabel("Hole Diameter:"), 2, 0)
        self.hole_diameter_edit = QLineEdit("0.8")
        dims_layout.addWidget(self.hole_diameter_edit, 2, 1)
        dims_layout.addWidget(QLabel("mm"), 2, 2)

        # Corner radius (for rectangle)
        dims_layout.addWidget(QLabel("Corner Radius:"), 3, 0)
        self.corner_radius_edit = QLineEdit("0")
        dims_layout.addWidget(self.corner_radius_edit, 3, 1)
        dims_layout.addWidget(QLabel("mm"), 3, 2)

        dims_group.setLayout(dims_layout)
        layout.addWidget(dims_group)

        # Layer configuration
        layer_group = QGroupBox("Layers")
        layer_layout = QVBoxLayout()

        # Copper layers
        self.top_copper_check = QCheckBox("Top Copper")
        self.top_copper_check.setChecked(True)
        layer_layout.addWidget(self.top_copper_check)

        self.bottom_copper_check = QCheckBox("Bottom Copper")
        layer_layout.addWidget(self.bottom_copper_check)

        # Mask layers
        self.top_mask_check = QCheckBox("Top Solder Mask")
        self.top_mask_check.setChecked(True)
        layer_layout.addWidget(self.top_mask_check)

        self.bottom_mask_check = QCheckBox("Bottom Solder Mask")
        layer_layout.addWidget(self.bottom_mask_check)

        # Paste layers
        self.top_paste_check = QCheckBox("Top Paste")
        self.top_paste_check.setChecked(True)
        layer_layout.addWidget(self.top_paste_check)

        self.bottom_paste_check = QCheckBox("Bottom Paste")
        layer_layout.addWidget(self.bottom_paste_check)

        layer_group.setLayout(layer_layout)
        layout.addWidget(layer_group)

        # Thermal settings for THT pads
        thermal_group = QGroupBox("Thermal Relief")
        thermal_layout = QGridLayout()

        self.thermal_enabled = QCheckBox("Enable Thermal Relief")
        self.thermal_enabled.setChecked(True)
        thermal_layout.addWidget(self.thermal_enabled, 0, 0, 1, 2)

        thermal_layout.addWidget(QLabel("Spoke Width:"), 1, 0)
        self.thermal_spoke_width = QLineEdit("0.3")
        thermal_layout.addWidget(self.thermal_spoke_width, 1, 1)

        thermal_layout.addWidget(QLabel("Gap Width:"), 2, 0)
        self.thermal_gap_width = QLineEdit("0.2")
        thermal_layout.addWidget(self.thermal_gap_width, 2, 1)

        thermal_group.setLayout(thermal_layout)
        layout.addWidget(thermal_group)

        # Preview area
        preview_group = QGroupBox("Preview")
        preview_layout = QVBoxLayout()
        self.pad_preview_scene = QGraphicsScene()
        self.pad_preview_view = QGraphicsView(self.pad_preview_scene)
        self.pad_preview_view.setMinimumSize(200, 200)
        preview_layout.addWidget(self.pad_preview_view)
        preview_group.setLayout(preview_layout)
        layout.addWidget(preview_group)

        # Buttons
        button_layout = QHBoxLayout()

        self.apply_button = QPushButton("Apply")
        self.apply_button.clicked.connect(self.apply_pad)
        button_layout.addWidget(self.apply_button)

        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.close)
        button_layout.addWidget(self.cancel_button)

        layout.addLayout(button_layout)

        self.setLayout(layout)

        # Connect signals for updating preview
        self.width_edit.textChanged.connect(self.update_pad_preview)
        self.height_edit.textChanged.connect(self.update_pad_preview)
        self.hole_diameter_edit.textChanged.connect(self.update_pad_preview)
        self.corner_radius_edit.textChanged.connect(self.update_pad_preview)

        # Initial preview
        self.update_pad_preview()

    def update_pad_preview(self):
        """Update the pad preview based on current settings"""
        self.pad_preview_scene.clear()

        try:
            width = float(self.width_edit.text()) * 20  # Scale for better visibility
            height = float(self.height_edit.text()) * 20
            hole_diameter = float(self.hole_diameter_edit.text()) * 20
            corner_radius = float(self.corner_radius_edit.text()) * 20
        except ValueError:
            # If any conversion fails, use default values
            width = 30
            height = 30
            hole_diameter = 16
            corner_radius = 0

        pad_type = self.pad_type_combo.currentText()
        pad_shape = self.pad_shape_combo.currentText()

        # Draw pad outline
        if pad_shape == "Circle":
            diameter = max(width, height)
            pad_item = QGraphicsEllipseItem(-diameter / 2, -diameter / 2, diameter, diameter)
        elif pad_shape == "Rectangle":
            if corner_radius > 0:
                # Create rounded rectangle path
                path = QPainterPath()
                path.addRoundedRect(-width / 2, -height / 2, width, height, corner_radius, corner_radius)
                pad_item = QGraphicsPathItem(path)
            else:
                pad_item = QGraphicsRectItem(-width / 2, -height / 2, width, height)
        elif pad_shape == "Oval":
            path = QPainterPath()
            path.addEllipse(-width / 2, -height / 2, width, height)
            pad_item = QGraphicsPathItem(path)
        else:  # Custom - just use rectangle for now
            pad_item = QGraphicsRectItem(-width / 2, -height / 2, width, height)

        # Set pad appearance
        pad_item.setPen(QPen(QColor(0, 128, 0), 1))
        pad_item.setBrush(QBrush(QColor(0, 200, 0, 128)))
        self.pad_preview_scene.addItem(pad_item)

        # Draw hole for THT pads
        if "THT" in pad_type and hole_diameter > 0:
            hole_item = QGraphicsEllipseItem(-hole_diameter / 2, -hole_diameter / 2,
                                             hole_diameter, hole_diameter)
            hole_item.setPen(QPen(QColor(0, 0, 0), 1))
            hole_item.setBrush(QBrush(QColor(255, 255, 255)))
            self.pad_preview_scene.addItem(hole_item)

            # Draw thermal relief if enabled
            if self.thermal_enabled.isChecked():
                try:
                    spoke_width = float(self.thermal_spoke_width.text()) * 20
                    gap_width = float(self.thermal_gap_width.text()) * 20
                except ValueError:
                    spoke_width = 6
                    gap_width = 4

                # Draw thermal relief spokes
                for angle in [0, 90, 180, 270]:
                    # Create a rectangle rotated at the specified angle
                    spoke = QGraphicsRectItem(-width / 2, -spoke_width / 2, width, spoke_width)
                    spoke.setRotation(angle)
                    spoke.setPen(QPen(QColor(0, 128, 0), 1))
                    spoke.setBrush(QBrush(QColor(0, 200, 0, 128)))
                    self.pad_preview_scene.addItem(spoke)

                    # Create cutouts on each side of the spoke
                    gap = QGraphicsRectItem(-hole_diameter / 2 - gap_width, -spoke_width / 2 - gap_width / 2,
                                            gap_width, spoke_width + gap_width)
                    gap.setRotation(angle)
                    gap.setPen(QPen(QColor(0, 0, 0), 1))
                    gap.setBrush(QBrush(QColor(255, 255, 255)))
                    self.pad_preview_scene.addItem(gap)

        # Reset view
        self.pad_preview_view.setScene(self.pad_preview_scene)
        self.pad_preview_view.fitInView(self.pad_preview_scene.itemsBoundingRect(), Qt.KeepAspectRatio)
        self.pad_preview_view.centerOn(0, 0)

    def apply_pad(self):
        """Create a pad with the current settings and return it"""
        pad_data = {
            'type': self.pad_type_combo.currentText(),
            'shape': self.pad_shape_combo.currentText(),
            'width': float(self.width_edit.text()),
            'height': float(self.height_edit.text()),
            'hole_diameter': float(self.hole_diameter_edit.text()),
            'corner_radius': float(self.corner_radius_edit.text()),
            'layers': {
                'top_copper': self.top_copper_check.isChecked(),
                'bottom_copper': self.bottom_copper_check.isChecked(),
                'top_mask': self.top_mask_check.isChecked(),
                'bottom_mask': self.bottom_mask_check.isChecked(),
                'top_paste': self.top_paste_check.isChecked(),
                'bottom_paste': self.bottom_paste_check.isChecked()
            },
            'thermal': {
                'enabled': self.thermal_enabled.isChecked(),
                'spoke_width': float(self.thermal_spoke_width.text()),
                'gap_width': float(self.thermal_gap_width.text())
            }
        }

        # Here you would normally create the pad and add it to your PCB
        # This is a signal that the pad was created successfully
        self.current_pad = pad_data
        self.close()
        return pad_data

    def edit_selected_pad(self):
        """Edit the currently selected pad"""
        selected_items = self.drawing_app.scene.selectedItems()
        for item in selected_items:
            if isinstance(item, Pad):
                # Mở Pad Editor với dữ liệu từ pad đã chọn
                pad_editor = PadEditor(self)

                # Thiết lập dữ liệu hiện tại
                pad_editor.pad_type_combo.setCurrentText(item.pad_data['type'])
                pad_editor.pad_shape_combo.setCurrentText(item.pad_data['shape'])
                pad_editor.width_edit.setText(str(item.pad_data['width']))
                pad_editor.height_edit.setText(str(item.pad_data['height']))
                pad_editor.hole_diameter_edit.setText(str(item.pad_data['hole_diameter']))
                pad_editor.corner_radius_edit.setText(str(item.pad_data['corner_radius']))

                # Thiết lập các checkboxes cho layers
                if 'layers' in item.pad_data:
                    layers = item.pad_data['layers']
                    pad_editor.top_copper_check.setChecked(layers.get('top_copper', True))
                    pad_editor.bottom_copper_check.setChecked(layers.get('bottom_copper', False))
                    pad_editor.top_mask_check.setChecked(layers.get('top_mask', True))
                    pad_editor.bottom_mask_check.setChecked(layers.get('bottom_mask', False))
                    pad_editor.top_paste_check.setChecked(layers.get('top_paste', True))
                    pad_editor.bottom_paste_check.setChecked(layers.get('bottom_paste', False))

                # Thiết lập thermal relief settings
                if 'thermal' in item.pad_data:
                    thermal = item.pad_data['thermal']
                    pad_editor.thermal_enabled.setChecked(thermal.get('enabled', True))
                    pad_editor.thermal_spoke_width.setText(str(thermal.get('spoke_width', 0.3)))
                    pad_editor.thermal_gap_width.setText(str(thermal.get('gap_width', 0.2)))

                # Show dialog
                if pad_editor.exec_() == QDialog.Accepted and pad_editor.current_pad:
                    # Cập nhật pad với dữ liệu mới
                    item.pad_data = pad_editor.current_pad
                    item.update()  # Cập nhật hiển thị
                    self.display_message("Updated pad properties")

                break
class Pad(QGraphicsItem):
    def __init__(self, pad_data, parent=None):
        super().__init__(parent)
        # Create a deep copy to avoid reference issues
        self.pad_data = json.loads(json.dumps(pad_data))

        # Set default values for any missing data
        if 'width' not in self.pad_data or not isinstance(self.pad_data['width'], (int, float)):
            self.pad_data['width'] = 1.5
        if 'height' not in self.pad_data or not isinstance(self.pad_data['height'], (int, float)):
            self.pad_data['height'] = 1.5
        if 'hole_diameter' not in self.pad_data or not isinstance(self.pad_data['hole_diameter'], (int, float)):
            self.pad_data['hole_diameter'] = 0.8
        if 'corner_radius' not in self.pad_data or not isinstance(self.pad_data['corner_radius'], (int, float)):
            self.pad_data['corner_radius'] = 0

        # Ensure layers and thermal data exists
        if 'layers' not in self.pad_data:
            self.pad_data['layers'] = {'top_copper': True, 'bottom_copper': False,
                                       'top_mask': True, 'bottom_mask': False,
                                       'top_paste': True, 'bottom_paste': False}
        if 'thermal' not in self.pad_data:
            self.pad_data['thermal'] = {'enabled': True, 'spoke_width': 0.3, 'gap_width': 0.2}

        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.ItemIsMovable, True)

    def show_error_message(self, title, message):
        error_dialog = QMessageBox()
        error_dialog.setIcon(QMessageBox.Critical)
        error_dialog.setWindowTitle(title)
        error_dialog.setText(message)

        # Get detailed traceback
        tb_str = traceback.format_exc()
        if tb_str != "NoneType: None\n":
            error_dialog.setDetailedText(tb_str)

        # Also print to console for debugging
        print(f"{title}: {message}\n{tb_str}")

        error_dialog.exec_()

    def boundingRect(self):
        width = self.pad_data['width'] * 10  # Scale for better visibility
        height = self.pad_data['height'] * 10
        return QRectF(-width / 2, -height / 2, width, height)

    def paint(self, painter, option, widget):
        width = self.pad_data['width'] * 10
        height = self.pad_data['height'] * 10
        hole_diameter = self.pad_data['hole_diameter'] * 10
        corner_radius = self.pad_data['corner_radius'] * 10

        # Set up the painter
        painter.setPen(QPen(QColor(0, 128, 0), 1))

        # Different fill based on what layers are selected
        if self.pad_data['layers']['top_copper']:
            painter.setBrush(QBrush(QColor(0, 200, 0, 128)))
        else:
            painter.setBrush(QBrush(QColor(0, 100, 0, 64)))

        # Draw pad based on shape
        if self.pad_data['shape'] == "Circle":
            diameter = max(width, height)
            painter.drawEllipse(-diameter / 2, -diameter / 2, diameter, diameter)
        elif self.pad_data['shape'] == "Rectangle":
            if corner_radius > 0:
                painter.drawRoundedRect(-width / 2, -height / 2, width, height, corner_radius, corner_radius)
            else:
                painter.drawRect(-width / 2, -height / 2, width, height)
        elif self.pad_data['shape'] == "Oval":
            painter.drawEllipse(-width / 2, -height / 2, width, height)

        # Draw hole for THT pads
        if "THT" in self.pad_data['type'] and hole_diameter > 0:
            painter.setPen(QPen(QColor(0, 0, 0), 1))
            painter.setBrush(QBrush(QColor(255, 255, 255)))
            painter.drawEllipse(-hole_diameter / 2, -hole_diameter / 2, hole_diameter, hole_diameter)

            # Draw thermal relief if enabled
            if self.pad_data['thermal']['enabled']:
                spoke_width = self.pad_data['thermal']['spoke_width'] * 10
                gap_width = self.pad_data['thermal']['gap_width'] * 10

                # Save current transform
                painter.save()

                # Draw thermal relief spokes
                for angle in [0, 90, 180, 270]:
                    painter.rotate(angle)

                    # Draw spoke
                    painter.setPen(QPen(QColor(0, 128, 0), 1))
                    painter.setBrush(QBrush(QColor(0, 200, 0, 128)))
                    painter.drawRect(-width / 2, -spoke_width / 2, width / 2 - hole_diameter / 2, spoke_width)

                    # Reset rotation for next spoke
                    painter.restore()
                    painter.save()

                painter.restore()

        # If selected, draw a highlight
        if self.isSelected():
            painter.setPen(QPen(QColor(255, 0, 0), 2, Qt.DashLine))
            painter.setBrush(Qt.NoBrush)
            painter.drawRect(self.boundingRect())

    def apply_pad(self):
        """Create a pad with the current settings and return it"""
        try:
            # Validate inputs first
            width = float(self.width_edit.text())
            height = float(self.height_edit.text())
            hole_diameter = float(self.hole_diameter_edit.text())
            corner_radius = float(self.corner_radius_edit.text())
            spoke_width = float(self.thermal_spoke_width.text())
            gap_width = float(self.thermal_gap_width.text())

            pad_data = {
                'type': self.pad_type_combo.currentText(),
                'shape': self.pad_shape_combo.currentText(),
                'width': width,
                'height': height,
                'hole_diameter': hole_diameter,
                'corner_radius': corner_radius,
                'layers': {
                    'top_copper': self.top_copper_check.isChecked(),
                    'bottom_copper': self.bottom_copper_check.isChecked(),
                    'top_mask': self.top_mask_check.isChecked(),
                    'bottom_mask': self.bottom_mask_check.isChecked(),
                    'top_paste': self.top_paste_check.isChecked(),
                    'bottom_paste': self.bottom_paste_check.isChecked()
                },
                'thermal': {
                    'enabled': self.thermal_enabled.isChecked(),
                    'spoke_width': spoke_width,
                    'gap_width': gap_width
                }
            }

            self.current_pad = pad_data
            self.accept()  # Set dialog result to Accepted
            return True
        except ValueError as e:
            QMessageBox.warning(self, "Input Error", "Please enter valid numeric values for all dimensions.")
            return False
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {str(e)}")
            return False
class PCBDesignApp(QMainWindow):
    def __init__(self):
        try:
            super().__init__()
            self.setWindowTitle('PCB Design Studio')
            self.setGeometry(100, 100, 1200, 800)
            self.drawing_app = DrawingApp()  # Create an instance of DrawingApp
            self.init_ui()  # Call init_ui method
        except Exception as e:
            # Fallback error handling
            print(f"Initialization Error: {e}")
            print(traceback.format_exc())
            QMessageBox.critical(None, "Initialization Error", str(e))

    def init_ui(self):
        try:
            # Create main layout components
            self.create_menu_bar()
            self.create_toolbar()
            self.create_left_sidebar()
            self.create_right_sidebar()
            self.create_central_canvas()
            self.create_bottom_panel()
        except Exception as e:
            # Fallback error handling
            print(f"UI Creation Error: {e}")
            print(traceback.format_exc())
            QMessageBox.critical(None, "UI Creation Error", str(e))

    def create_menu_bar(self):
        # Create menubar if it doesn't exist
        if not hasattr(self, 'menubar'):
            self.menubar = self.menuBar()

        # File Menu
        file_menu = self.menubar.addMenu('File')
        new_project_action = QAction('New Project', self)
        open_project_action = QAction('Open Project', self)
        save_action = QAction('Save', self)
        file_menu.addAction(new_project_action)
        file_menu.addAction(open_project_action)
        file_menu.addAction(save_action)

        # Edit Menu
        edit_menu = self.menubar.addMenu('Edit')
        undo_action = QAction('Undo', self)
        redo_action = QAction('Redo', self)
        edit_menu.addAction(undo_action)
        edit_menu.addAction(redo_action)

        # Design Menu
        design_menu = self.menubar.addMenu('Design')
        create_footprint_action = QAction('Create Footprint', self)
        layer_manager_action = QAction('Layer Manager', self)
        design_menu.addAction(create_footprint_action)
        design_menu.addAction(layer_manager_action)

    def create_toolbar(self):
        toolbar = QToolBar('Design Tools')
        self.addToolBar(toolbar)

        # Drawing tools
        draw_line_action = QAction('Draw Line', self)
        draw_line_action.triggered.connect(lambda: self.set_drawing_mode("line"))
        toolbar.addAction(draw_line_action)

        draw_rect_action = QAction('Draw Rectangle', self)
        draw_rect_action.triggered.connect(lambda: self.set_drawing_mode("rect"))
        toolbar.addAction(draw_rect_action)

        draw_circle_action = QAction('Draw Circle', self)
        draw_circle_action.triggered.connect(lambda: self.set_drawing_mode("circle"))
        toolbar.addAction(draw_circle_action)

        color_action = QAction('Choose Color', self)
        color_action.triggered.connect(self.choose_drawing_color)
        toolbar.addAction(color_action)

        toolbar.addSeparator()
        pad_editor_action = QAction('Pad Editor', self)
        pad_editor_action.triggered.connect(self.show_pad_editor)
        toolbar.addAction(pad_editor_action)

    def set_drawing_mode(self, mode):
        print(f"Setting drawing mode to: {mode}")  # Debug print
        if hasattr(self, 'drawing_app'):
            self.drawing_app.drawing_mode = mode
            print(f"Drawing mode set to: {self.drawing_app.drawing_mode}")

    def choose_drawing_color(self):
        if hasattr(self, 'drawing_app'):
            self.drawing_app.choose_color()

    def create_central_canvas(self):
        self.canvas_widget = QTabWidget()

        # Set up the scene for DrawingApp
        scene = QGraphicsScene(self)
        scene.setSceneRect(0, 0, 2000, 2000)
        self.drawing_app.scene = scene
        self.drawing_app.drawing_window.setScene(scene)

        self.add_grid(scene)
        self.canvas_widget.addTab(self.drawing_app.drawing_window, 'PCB Design')
        self.setCentralWidget(self.canvas_widget)

    def add_grid(self, scene):
        grid_color = QColor(240, 240, 240)
        grid_spacing = 10
        for x in range(0, 2000, grid_spacing):
            scene.addLine(x, 0, x, 2000, QPen(grid_color))
        for y in range(0, 2000, grid_spacing):
            scene.addLine(0, y, 2000, y, QPen(grid_color))

    def create_left_sidebar(self):
        dock = QDockWidget('Component Library', self)
        dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        tree = QTreeWidget()
        tree.setHeaderLabel('Components')
        categories = [
            ('Passive', ['Resistor', 'Capacitor', 'Inductor']),
            ('Active', ['Transistor', 'IC', 'Diode']),
            ('Connectors', ['USB', 'HDMI', 'Pin Header'])
        ]
        for category, components in categories:
            cat_item = QTreeWidgetItem(tree, [category])
            for component in components:
                QTreeWidgetItem(cat_item, [component])
        dock.setWidget(tree)
        self.addDockWidget(Qt.LeftDockWidgetArea, dock)

    def create_right_sidebar(self):
        dock = QDockWidget('Properties', self)
        dock.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        properties_widget = QWidget()
        layout = QGridLayout()
        properties = [
            ('Component Type:', QComboBox()),
            ('Footprint:', QLineEdit()),
            ('Value:', QLineEdit()),
            ('Tolerance:', QComboBox())
        ]
        for i, (label, widget) in enumerate(properties):
            layout.addWidget(QLabel(label), i, 0)
            layout.addWidget(widget, i, 1)
        properties_widget.setLayout(layout)
        dock.setWidget(properties_widget)
        self.addDockWidget(Qt.RightDockWidgetArea, dock)

    def create_bottom_panel(self):
        dock = QDockWidget('Messages', self)
        dock.setAllowedAreas(Qt.BottomDockWidgetArea)
        message_list = QListWidget()
        message_list.addItems([
            'Welcome to PCB Design Studio',
            'Ready to start designing'
        ])
        dock.setWidget(message_list)
        self.addDockWidget(Qt.BottomDockWidgetArea, dock)

    def show_error_message(self, title, message):
        error_dialog = QMessageBox()
        error_dialog.setIcon(QMessageBox.Critical)
        error_dialog.setWindowTitle(title)
        error_dialog.setText(message)
        error_dialog.setDetailedText(traceback.format_exc())
        error_dialog.exec_()

    def show_pad_editor(self):
        """Open the pad editor dialog"""
        try:
            pad_editor = PadEditor(self)
            pad_editor.setWindowModality(Qt.ApplicationModal)

            # Use a safe approach to show the dialog
            if pad_editor.exec_() == QDialog.Accepted and pad_editor.current_pad:
                self.add_pad_to_design(pad_editor.current_pad)
        except Exception as e:
            traceback_str = traceback.format_exc()
            print(f"Error in pad editor: {str(e)}\n{traceback_str}")
            self.show_error_message("Pad Editor Error", f"Error in pad editor: {str(e)}")
    def add_pad_to_design(self, pad_data):
        """Add a pad to the PCB design"""
        try:
            pad = Pad(pad_data)
            # Position the pad at the center of the view
            view_center = self.drawing_app.drawing_window.mapToScene(
                self.drawing_app.drawing_window.viewport().rect().center())
            pad.setPos(view_center)

            # Add to scene
            self.drawing_app.scene.addItem(pad)

            # Store in appropriate layer
            if not hasattr(self.drawing_app, 'pads'):
                self.drawing_app.pads = []
            self.drawing_app.pads.append(pad)

            # Select the pad so the user can move it
            pad.setSelected(True)
        except Exception as e:
            self.show_error_message("Pad Creation Error", f"Error creating pad: {str(e)}")

def main():
    try:
        app = QApplication(sys.argv)
        pcb_app = PCBDesignApp()
        pcb_app.show()
        sys.exit(app.exec_())
    except Exception as e:
        print(f"Fatal Error: {e}")
        traceback.print_exc()
        # Show a message box for unhandled exceptions
        error_dialog = QMessageBox()
        error_dialog.setIcon(QMessageBox.Critical)
        error_dialog.setWindowTitle("Fatal Error")
        error_dialog.setText(f"A fatal error occurred: {str(e)}")
        error_dialog.setDetailedText(traceback.format_exc())
        error_dialog.exec_()


if __name__ == '__main__':
    main()