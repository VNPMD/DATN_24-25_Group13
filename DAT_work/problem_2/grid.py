from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsEllipseItem, QGraphicsLineItem, QGraphicsItem, QMainWindow, QApplication, QLabel, QVBoxLayout, QWidget,QDoubleSpinBox, QComboBox, QHBoxLayout, QLabel

from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtCore import Qt, QPointF
"""
This code creates a grid view with pads and lines, allowing for mouse interaction to display coordinates.

"""
class GridView(QGraphicsView):
    def __init__(self, grid_spacing=0.1, dpi=96, coord_label=None):
        super().__init__()
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        self.grid_spacing_mm = grid_spacing
        self.dpi = dpi
        self.mm_to_pixel = dpi / 25.4  # 1 inch = 25.4 mm
        self.coord_label = coord_label

        self.setRenderHints(QPainter.Antialiasing)
        self.setSceneRect(-5000, -5000, 10000, 10000)  # Big scene for panning
        self.scale(self.mm_to_pixel, self.mm_to_pixel)  # Convert mm to pixels
        self.setMouseTracking(True)

    def drawBackground(self, painter, rect):
        painter.setPen(QPen(Qt.lightGray, 0))
        left = float(rect.left())
        top = float(rect.top())
        right = float(rect.right())
        bottom = float(rect.bottom())

        step = self.grid_spacing_mm
        x = left - (left % step)
        while x < right + step:
            painter.drawLine(QPointF(x, top), QPointF(x, bottom))
            x += step

        y = top - (top % step)
        while y < bottom + step:
            painter.drawLine(QPointF(left, y), QPointF(right, y))
            y += step

    def mouseMoveEvent(self, event):
        # Lấy vị trí chuột trong scene (mm)
        pos = self.mapToScene(event.pos())
        if self.coord_label:
            self.coord_label.setText(f"X: {pos.x():.3f} mm   Y: {pos.y():.3f} mm")
        super().mouseMoveEvent(event)

class PadItem(QGraphicsEllipseItem):
    def __init__(self, x, y, w, h):
        super().__init__(-w/2, -h/2, w, h)  # Tâm pad tại (x, y)
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setPos(x, y)

    def mousePressEvent(self, event):
        print(f"Pad selected at: ({self.pos().x():.2f}, {self.pos().y():.2f}) mm")
        super().mousePressEvent(event)

class DrawingLine(QGraphicsLineItem):
    def __init__(self, x1, y1, x2, y2):
        super().__init__(x1, y1, x2, y2)
        self.setPen(QPen(Qt.blue, 0.2))
        self.setFlag(QGraphicsItem.ItemIsSelectable)

    def mousePressEvent(self, event):
        line = self.line()
        print(f"Line: Start ({line.x1():.2f}, {line.y1():.2f}), "
              f"End ({line.x2():.2f}, {line.y2():.2f})")
        super().mousePressEvent(event)

class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        # Tạo label hiển thị tọa độ
        self.coord_label = QLabel("X: 0.000 mm   Y: 0.000 mm")
        self.coord_label.setStyleSheet("padding: 4px; color: #006; font-weight: bold;")

        # Tạo GridView và truyền label vào
        self.grid_view = GridView(coord_label=self.coord_label)

        # Khung điều khiển bước lưới (ở trên)
        self.grid_spin = QDoubleSpinBox()
        self.grid_spin.setDecimals(3)
        self.grid_spin.setSingleStep(0.01)
        self.grid_spin.setMinimum(0.01)
        self.grid_spin.setMaximum(100)
        self.grid_spin.setValue(self.grid_view.grid_spacing_mm)
        self.grid_spin.valueChanged.connect(self.on_grid_spacing_changed)

        self.grid_unit_combo = QComboBox()
        self.grid_unit_combo.addItems(["mm", "inch"])
        self.grid_unit_combo.currentTextChanged.connect(self.on_unit_changed)
        self.current_unit = "mm"

        grid_ctrl_layout = QHBoxLayout()
        grid_ctrl_layout.addWidget(QLabel("Grid:"))
        grid_ctrl_layout.addWidget(self.grid_spin)
        grid_ctrl_layout.addWidget(self.grid_unit_combo)
        grid_ctrl_layout.addStretch()

        # Khung nhập tọa độ và chọn đơn vị (ở dưới cùng)
        self.x_spin = QDoubleSpinBox()
        self.x_spin.setDecimals(2)
        self.x_spin.setSingleStep(0.01)
        self.x_spin.setRange(-5000, 5000)
        self.x_spin.setPrefix("X: ")
        self.x_spin.setSuffix(" mm")
        self.x_spin.valueChanged.connect(self.on_coord_spin_changed)

        self.y_spin = QDoubleSpinBox()
        self.y_spin.setDecimals(2)
        self.y_spin.setSingleStep(0.01)
        self.y_spin.setRange(-5000, 5000)
        self.y_spin.setPrefix("Y: ")
        self.y_spin.setSuffix(" mm")
        self.y_spin.valueChanged.connect(self.on_coord_spin_changed)

        self.coord_unit_combo = QComboBox()
        self.coord_unit_combo.addItems(["mm", "inch"])
        self.coord_unit_combo.currentTextChanged.connect(self.on_coord_unit_changed)
        self.coord_unit = "mm"

        coord_ctrl_layout = QHBoxLayout()
        coord_ctrl_layout.addWidget(self.x_spin)
        coord_ctrl_layout.addWidget(self.y_spin)
        coord_ctrl_layout.addWidget(self.coord_unit_combo)
        coord_ctrl_layout.addStretch()

        # Layout chính
        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)
        layout.addLayout(grid_ctrl_layout)
        layout.addWidget(self.grid_view)
        layout.addWidget(self.coord_label)
        layout.addLayout(coord_ctrl_layout)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setCentralWidget(central_widget)

        # Add pad and line
        pad = PadItem(0, 0, 1, 1.5)
        line = DrawingLine(0, 0, 5, 0)
        self.grid_view.scene.addItem(pad)
        self.grid_view.scene.addItem(line)

        # Bắt sự kiện click chuột trên lưới để cập nhật spinbox
        self.grid_view.mousePressEvent = self.on_grid_mouse_press

    def on_coord_spin_changed(self):
        # Có thể xử lý khi người dùng nhập tọa độ mới (nếu cần)
        pass

    def on_coord_unit_changed(self, unit):
        old_unit = self.coord_unit
        self.coord_unit = unit
        x = self.x_spin.value()
        y = self.y_spin.value()
        if unit == "mm" and old_unit == "inch":
            self.x_spin.setValue(round(x * 25.4, 2))
            self.y_spin.setValue(round(y * 25.4, 2))
            self.x_spin.setSuffix(" mm")
            self.y_spin.setSuffix(" mm")
        elif unit == "inch" and old_unit == "mm":
            self.x_spin.setValue(round(x / 25.4, 2))
            self.y_spin.setValue(round(y / 25.4, 2))
            self.x_spin.setSuffix(" inch")
            self.y_spin.setSuffix(" inch")

    def on_grid_mouse_press(self, event):
        pos = self.grid_view.mapToScene(event.pos())
        if self.coord_unit == "mm":
            self.x_spin.setValue(round(pos.x(), 2))
            self.y_spin.setValue(round(pos.y(), 2))
        else:
            self.x_spin.setValue(round(pos.x() / 25.4, 2))
            self.y_spin.setValue(round(pos.y() / 25.4, 2))
        QGraphicsView.mousePressEvent(self.grid_view, event)

    def on_grid_spacing_changed(self, value):
        # Đổi bước lưới theo đơn vị hiện tại
        if self.current_unit == "mm":
            self.grid_view.set_grid_spacing(value)
        else:  # inch
            self.grid_view.set_grid_spacing(value * 25.4)

    def on_unit_changed(self, unit):
        old_unit = self.current_unit
        self.current_unit = unit
        val = self.grid_spin.value()
        if unit == "mm" and old_unit == "inch":
            # Chuyển inch -> mm
            new_val = val * 25.4
            self.grid_spin.blockSignals(True)
            self.grid_spin.setValue(round(new_val, 3))
            self.grid_spin.blockSignals(False)
            self.grid_view.set_grid_spacing(new_val)
        elif unit == "inch" and old_unit == "mm":
            # Chuyển mm -> inch
            new_val = val / 25.4
            self.grid_spin.blockSignals(True)
            self.grid_spin.setValue(round(new_val, 3))
            self.grid_spin.blockSignals(False)
            self.grid_view.set_grid_spacing(val)
        # Đảm bảo đơn vị nhỏ nhất là 0.01 mm hoặc 0.01 inch
        self.grid_spin.setMinimum(0.01)
# Thêm vào GridView:
if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    win = MainApp()
    win.resize(800, 600)
    win.show()
    sys.exit(app.exec_())