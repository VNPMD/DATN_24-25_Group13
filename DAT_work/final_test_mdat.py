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
            
                row_data.append(value)

                # Lưu giá trị bán kính để kiểm tra
                if col == 4:  # Bán kính ngoài
                    outer_radius = value
                if col == 5:  # Bán kính trong
                    inner_radius = value

            data.append(row_data)

            # Kiểm tra điều kiện "bán kính ngoài > bán kính trong"
            if outer_radius is not None and inner_radius is not None:
                if outer_radius <= inner_radius:
                    error_found = True
                    self.table.item(row, 4).setBackground(Qt.red)
                    self.table.item(row, 5).setBackground(Qt.red)
                    print(f"Lỗi: Bán kính ngoài phải lớn hơn bán kính trong (hàng {row+1})!")

        if error_found:
            QMessageBox.warning(self, "Lỗi dữ liệu", "Có lỗi trong dữ liệu! Vui lòng kiểm tra lại.")

        print("Dữ liệu bảng Table (Pad Layer):", data)
        return data
class PCBDesignApp(QMainWindow):
    def __init__(self):
        try:
            super().__init__()
            self.setWindowTitle('PCB Design Studio')
            self.setGeometry(100, 100, 1200, 800)

            # Initialize UI components
            self.init_ui()
        except Exception as e:
            self.show_error_message("Initialization Error", str(e))

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
            self.show_error_message("UI Creation Error", str(e))

    def create_menu_bar(self):
        menubar = self.menuBar()

        # File Menu
        file_menu = menubar.addMenu('File')
        file_menu.addAction('New Project')
        file_menu.addAction('Open Project')
        file_menu.addAction('Save')

        # Edit Menu
        edit_menu = menubar.addMenu('Edit')
        edit_menu.addAction('Undo')
        edit_menu.addAction('Redo')

        # Design Menu
        design_menu = menubar.addMenu('Design')
        create_footprint_action = QAction('Create Footprint', self)
        create_footprint_action.triggered.connect(self.open_footprint_editor)
        design_menu.addAction(create_footprint_action)
        design_menu.addAction('Layer Manager')

    def create_toolbar(self):
        toolbar = QToolBar('Design Tools')
        self.addToolBar(toolbar)

        tools = [
            'Select', 'Move', 'Draw',
            'Place Component', 'Route'
        ]

        for name in tools:
            action = toolbar.addAction(name)

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

    def create_central_canvas(self):
        self.canvas_widget = QTabWidget()

        scene = QGraphicsScene(self)
        scene.setSceneRect(0, 0, 2000, 2000)

        view = QGraphicsView(scene)
        view.setRenderHint(QPainter.Antialiasing)
        view.setDragMode(QGraphicsView.RubberBandDrag)

        self.add_grid(scene)

        self.canvas_widget.addTab(view, 'PCB Design')
        self.setCentralWidget(self.canvas_widget)

    def add_grid(self, scene):
        grid_color = QColor(240, 240, 240)
        grid_spacing = 10

        for x in range(0, 2000, grid_spacing):
            scene.addLine(x, 0, x, 2000, QPen(grid_color))

        for y in range(0, 2000, grid_spacing):
            scene.addLine(0, y, 2000, y, QPen(grid_color))

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
    def open_footprint_editor(self):
        self.pad_editor = PadEditor()
        self.pad_editor.show()
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PCBDesignApp()
    window.showMaximized()
    sys.exit(app.exec())
