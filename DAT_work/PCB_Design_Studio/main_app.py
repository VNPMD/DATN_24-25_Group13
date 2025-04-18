import  traceback
from PyQt5.QtWidgets import (
    QMainWindow, QDockWidget, QTreeWidget, QTreeWidgetItem,
    QWidget, QGridLayout, QLabel, QLineEdit, QComboBox, QTabWidget,
    QGraphicsScene, QListWidget, QToolBar, QAction, QMessageBox,
    QDialog, QPushButton, QCheckBox, QVBoxLayout, QHBoxLayout
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPen, QColor

from drawing import DrawingApp
from pad_editor import PadEditor
from pad import Pad
# from layer_manager import LayerManager
# from setting_manager import SettingsManager
# from settings_editor import SettingsEditor

class main_app(QMainWindow):
    def __init__(self):
        try:
            super().__init__()  # Gọi hàm khởi tạo của lớp cha QMainWindow.
            # self.settings_manager = SettingsManager()  # Tạo một instance của lớp SettingsManager để quản lý cài đặt.
            self.setWindowTitle('PCB Design Studio')  # Đặt tiêu đề cho cửa sổ chính.
            self.setGeometry(100, 100, 1200, 800)  # Đặt vị trí và kích thước cửa sổ (x, y, width, height).
            self.drawing_app = DrawingApp()  # Tạo một instance của lớp DrawingApp (ứng dụng vẽ).
            self.init_ui()  # Gọi phương thức khởi tạo giao diện người dùng.
        except Exception as e:
            # Xử lý lỗi nếu xảy ra trong quá trình khởi tạo.
            print(f"Initialization Error: {e}")  # In lỗi ra console.
            print(traceback.format_exc())  # In chi tiết lỗi ra console.
            QMessageBox.critical(None, "Initialization Error", str(e))  # Hiển thị hộp thoại thông báo lỗi.

    def init_ui(self):
        try:
            # Tạo các thành phần giao diện chính
            self.create_menu_bar()  # Tạo thanh menu.
            self.create_toolbar()  # Tạo thanh công cụ.
            self.create_left_sidebar()  # Tạo thanh bên trái.
            self.create_right_sidebar()  # Tạo thanh bên phải.
            self.create_central_canvas()  # Tạo khu vực vẽ chính.
            self.create_bottom_panel()  # Tạo bảng thông báo ở dưới cùng.
        except Exception as e:
            # Xử lý lỗi nếu xảy ra trong quá trình tạo giao diện.
            print(f"UI Creation Error: {e}")  # In lỗi ra console.
            print(traceback.format_exc())  # In chi tiết lỗi ra console.
            QMessageBox.critical(None, "UI Creation Error", str(e))  # Hiển thị hộp thoại thông báo lỗi.
    def create_menu_bar(self):
        if not hasattr(self, 'menubar'):  # Kiểm tra xem menubar đã tồn tại chưa.
            self.menubar = self.menuBar()  # Tạo thanh menu.

        # File Menu
        file_menu = self.menubar.addMenu('File')  # Thêm menu "File".
        new_project_action = QAction('New Project', self)  # Tạo hành động "New Project".
        open_project_action = QAction('Open Project', self)  # Tạo hành động "Open Project".
        save_action = QAction('Save', self)  # Tạo hành động "Save".
        # setting_action = QAction('Settings', self)  # Tạo hành động "Settings".
        # setting_action.triggered.connect(self.show_settings_editor)  # Kết nối hành động với phương thức mở cài đặt.
        
        file_menu.addAction(new_project_action)  # Thêm hành động vào menu "File".
        file_menu.addAction(open_project_action)
        file_menu.addAction(save_action)
        file_menu.addSeparator()  # Thêm một đường phân cách.
        # file_menu.addAction(setting_action)  # Thêm hành động "Settings" vào menu "File".
        # Edit Menu
        edit_menu = self.menubar.addMenu('Edit')  # Thêm menu "Edit".
        undo_action = QAction('Undo', self)  # Tạo hành động "Undo".
        redo_action = QAction('Redo', self)  # Tạo hành động "Redo".
        edit_menu.addAction(undo_action)  # Thêm hành động vào menu "Edit".
        edit_menu.addAction(redo_action)

        # Design Menu
        design_menu = self.menubar.addMenu('Design')  # Thêm menu "Design".
        create_footprint_action = QAction('Create Footprint', self)  # Tạo hành động "Create Footprint".
        layer_manager_action = QAction('Layer Manager', self)  # Tạo hành động "Layer Manager".
        design_menu.addAction(create_footprint_action)  # Thêm hành động vào menu "Design".
        design_menu.addAction(layer_manager_action)
        # Design tootbar 
   
    def create_toolbar(self):
        toolbar = QToolBar('Design Tools')  # Tạo thanh công cụ với tiêu đề "Design Tools".
        self.addToolBar(toolbar)  # Thêm thanh công cụ vào cửa sổ chính.

        # Công cụ vẽ
        draw_line_action = QAction('Draw Line', self)  # Tạo hành động "Draw Line".
        draw_line_action.triggered.connect(lambda: self.set_drawing_mode("line"))  # Kết nối hành động với phương thức.
        toolbar.addAction(draw_line_action)  # Thêm hành động vào thanh công cụ.

        draw_rect_action = QAction('Draw Rectangle', self)  # Tạo hành động "Draw Rectangle".
        draw_rect_action.triggered.connect(lambda: self.set_drawing_mode("rect"))
        toolbar.addAction(draw_rect_action)

        draw_circle_action = QAction('Draw Circle', self)  # Tạo hành động "Draw Circle".
        draw_circle_action.triggered.connect(lambda: self.set_drawing_mode("circle"))
        toolbar.addAction(draw_circle_action)

        # Công cụ chọn màu
        color_action = QAction('Choose Color', self)  # Tạo hành động "Choose Color".
        color_action.triggered.connect(self.choose_drawing_color)  # Kết nối hành động với phương thức.
        toolbar.addAction(color_action)

        toolbar.addSeparator()  # Thêm một đường phân cách.

        # Công cụ chỉnh sửa pad
        pad_editor_action = QAction('Pad Editor', self)  # Tạo hành động "Pad Editor".
        pad_editor_action.triggered.connect(self.show_pad_editor)  # Kết nối hành động với phương thức.
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
        self.canvas_widget = QTabWidget()  # Tạo widget dạng tab để chứa khung vẽ.

        # Thiết lập cảnh cho DrawingApp
        scene = QGraphicsScene(self)  # Tạo một cảnh vẽ.
        scene.setSceneRect(0, 0, 2000, 2000)  # Đặt kích thước cảnh.
        self.drawing_app.scene = scene  # Gán cảnh cho DrawingApp.
        self.drawing_app.drawing_window.setScene(scene)  # Đặt cảnh vào cửa sổ vẽ.

        # # Tạo LayerManager
        # self.layer_manager = LayerManager(scene)

    
        # # Thêm lưới vào layer "Grid"
        # self.add_grid("grid")  # Thêm lưới vào cảnh.
        self.app_grid(scene)  # Thêm lưới vào cảnh.
        
        self.canvas_widget.addTab(self.drawing_app.drawing_window, 'PCB Design')  # Thêm tab với tiêu đề "PCB Design".
        self.setCentralWidget(self.canvas_widget)  # Đặt widget này làm khu vực trung tâm.
    def add_grid(self, scene):
        grid_color = QColor(240, 240, 240)
        grid_spacing = 10
        for x in range(0, 2000, grid_spacing):
            scene.addLine(x, 0, x, 2000, QPen(grid_color))
        for y in range(0, 2000, grid_spacing):
            scene.addLine(0, y, 2000, y, QPen(grid_color))
    # def add_grid(self, layer_name):
    #     """
    #     Thêm lưới vào layer được chỉ định.
    #     :param layer_name: Tên của layer để thêm lưới.
    #     """
    #     grid_color = self.layer_manager.layers[layer_name]["color"]  # Lấy màu từ layer
    #     grid_spacing = 10  # Khoảng cách giữa các đường lưới

    #     # Vẽ các đường dọc
    #     for x in range(0, 2000, grid_spacing):
    #         line = self.layer_manager.scene.addLine(x, 0, x, 2000, QPen(grid_color))
    #         self.layer_manager.add_item_to_layer(layer_name, line)

    #     # Vẽ các đường ngang
    #     for y in range(0, 2000, grid_spacing):
    #         line = self.layer_manager.scene.addLine(0, y, 2000, y, QPen(grid_color))
    #         self.layer_manager.add_item_to_layer(layer_name, line)



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
    # def show_settings_editor(self):
    #     try:
    #         from settings_editor import SettingsEditor  # Import moved inside the method
    #         settings_editor = SettingsEditor(self.settings_manager, self)
    #         settings_editor.exec_()
    #     except Exception as e:
    #         QMessageBox.critical(self, "Error", f"Failed to open Settings Editor: {str(e)}")
    def show_pad_editor(self):
        # Open the pad editor dialog
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
        # Add a pad to the PCB design
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
    def show_layer_count(self):
        layer_count = self.layer_manager.get_layer_count()
        print(f"Số lượng layer hiện tại: {layer_count}")