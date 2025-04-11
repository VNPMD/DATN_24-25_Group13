from PyQt5.QtWidgets import QMainWindow, QToolBar, QDockWidget, QTreeWidget, QTreeWidgetItem, QGraphicsView, QGraphicsScene, QGraphicsRectItem, QTabWidget, QWidget, QGridLayout, QLabel, QLineEdit, QComboBox, QListWidget, QMessageBox, QAction, QPushButton, QButtonGroup, QCheckBox, QTableWidget, QTableWidgetItem, QColorDialog
from PyQt5.QtGui import QPainter, QPen, QColor
from PyQt5.QtCore import Qt
import sys
import traceback
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QPushButton, QColorDialog, QGraphicsView, QGraphicsScene, QGraphicsRectItem, QGraphicsEllipseItem, QCheckBox, QButtonGroup, QLabel, QWidget,QMessageBox
class PadEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pad Editor")
        self.setGeometry(100, 100, 1000, 600)  # Kích thước cửa sổ
        self.init_ui()

    def init_ui(self):
        # Bảng Table1 (User Layer)
        self.table_1 = QTableWidget(5, 2, self)
        self.table_1.setHorizontalHeaderLabels(["Layout", "Màu"])
        self.table_1.setGeometry(10, 290, 220, 175)  # X, Y, Width, Height
        
        layout_1 = ["User layer 1", "User layer 2", "User layer 3", "User layer 4", "User layer 5"]
        for i, layout in enumerate(layout_1):
            self.table_1.setItem(i, 0, QTableWidgetItem(layout))
            btn_color = QPushButton("Chọn màu", self)
            btn_color.clicked.connect(lambda _, row=i: self.choose_color(row, self.table_1))
            self.table_1.setCellWidget(i, 1, btn_color)

        # Bảng Table (Pad Layer)
        self.table = QTableWidget(7, 6, self)
        self.table.setHorizontalHeaderLabels(["Layout", "Màu", "Dài", "Rộng", "Bán kính ngoài", "Bán kính trong"])
        self.table.setGeometry(10,10, 620, 235)
        
        layouts = ["Top layer", "Bottom layer", "Top solder", "Bottom solder", "Top overlay",
                   "Bottom overlay", "Multilayer"]
        for i, layout in enumerate(layouts):
            self.table.setItem(i, 0, QTableWidgetItem(layout))
            btn_color = QPushButton("Chọn màu", self)
            btn_color.clicked.connect(lambda _, row=i: self.choose_color(row, self.table))
            self.table.setCellWidget(i, 1, btn_color)

        # Khung vẽ Footprint
        self.view = QGraphicsView(self)
        self.view.setGeometry(700, 200, 275, 275)
        self.scene = QGraphicsScene()
        self.view.setScene(self.scene)

        # Nhóm chọn kiểu chân
        self.pin_type_group = QWidget(self)
        self.pin_type_group.setGeometry(370, 320, 200, 100)  # X, Y, Width, Height

        pin_layout_label = QLabel("Chọn kiểu chân:", self.pin_type_group)
        pin_layout_label.move(10, 5)

        self.pin_smd = QCheckBox("Dán", self.pin_type_group)
        self.pin_smd.move(10, 25)

        self.pin_through = QCheckBox("Xuyên", self.pin_type_group)
        self.pin_through.move(10, 45)
        self.pin_square = QCheckBox("Vuông", self.pin_type_group)
        self.pin_square.move(100, 25)

        self.pin_circle = QCheckBox("Tròn", self.pin_type_group)
        self.pin_circle.move(100, 45)

        self.shape_group = QButtonGroup(self)  # Đảm bảo chỉ chọn một loại hình dạng
        self.shape_group.addButton(self.pin_square)
        self.shape_group.addButton(self.pin_circle)

        # Nút tạo footprint
        self.btn_create = QPushButton("Tạo Footprint", self)
        self.btn_create.setGeometry(700, 500, 275, 30)
        self.btn_create.clicked.connect(self.draw_footprint)
       

    def choose_color(self, row, table):
        """ Chọn màu cho bảng tương ứng """
        color = QColorDialog.getColor()
        if color.isValid():
            btn = table.cellWidget(row, 1)
            btn.setStyleSheet(f"background-color: {color.name()}")

    def draw_footprint(self):
        """ Vẽ footprint theo lựa chọn của người dùng """
        self.scene.clear()
        pen = QPen(Qt.black)

        # Lấy dữ liệu từ bảng
        data = self.read_table_data()
        print("Dữ liệu bảng Table (Pad Layer):", data)

        if self.pin_square.isChecked():
            rect = QGraphicsRectItem(50, 50, 40, 40)
            rect.setPen(pen)
            self.scene.addItem(rect)

        elif self.pin_circle.isChecked():
            outer_radius = 30
            inner_radius = 15
            outer_circle = QGraphicsEllipseItem(60, 60, outer_radius * 2, outer_radius * 2)
            inner_circle = QGraphicsEllipseItem(75, 75, inner_radius * 2, inner_radius * 2)
            outer_circle.setPen(pen)
            inner_circle.setPen(pen)
            self.scene.addItem(outer_circle)
            self.scene.addItem(inner_circle)

        if self.pin_smd.isChecked():
            print("Chế độ: Chân dán (SMD)")
        if self.pin_through.isChecked():
            print("Chế độ: Chân xuyên lỗ")
        # """ Đọc dữ liệu từ bảng và kiểm tra lỗi """
    def read_table_data(self):
        data = []
        error_found = False  # Biến kiểm tra lỗi

        for row in range(self.table.rowCount()):
            row_data = []
            outer_radius = None
            inner_radius = None

            for col in range(2, self.table.columnCount()):  # Chỉ lấy cột số
                item = self.table.item(row, col)

                if item is None:  
                    value = None  
                else:
                    text = item.text().strip()  
                    if text:
                        try:
                            value = float(text)  
                            item.setBackground(Qt.white)  # Xóa màu lỗi
                        except ValueError:
                            value = None
                            item.setBackground(Qt.red)  
                            error_found = True
                    else:
                        value = None
app = QApplication(sys.argv)
mainWin = PadEditor()
mainWin.showMaximized()
sys.exit(app.exec_())
