from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QTreeWidget, QTreeWidgetItem, QTabWidget,
    QWidget, QTableWidget, QTableWidgetItem, QPushButton, QLabel, QLineEdit,
    QComboBox, QFrame, QSpinBox
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

# Danh sách vật liệu mặc định
DEFAULT_CONDUCTOR = [
    ("Copper", "59"),
    ("Tin", "7.9"),
    ("Aluminum", "37.4"),
    ("Platinum", "9.4"),
    ("Gold", "45.5"),
    ("Iron", "19.6"),
    ("Silver", "61.4"),
]
DEFAULT_INSULATOR = [
    ("Air", "4.6", "0"),
    ("FR2", "4.6", "0"),
    ("FR3", "4.6", "0"),
    ("FR4", "4.6", "0.018"),
    ("FR5", "4.6", "0"),
    ("G10", "5.2", "0"),
    ("G11", "5.2", "0"),
]
class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.resize(950, 600)

        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(4, 4, 4, 4)
        main_layout.setSpacing(8)

        # ==== LEFT PANEL ====
        left_panel = QVBoxLayout()
        left_panel.setSpacing(8)

        # Combobox Footprint
        self.combo = QComboBox()
        self.combo.addItem("Footprint")
        left_panel.addWidget(self.combo)

        # Tree navigation
        self.tree = QTreeWidget()
        self.tree.setHeaderHidden(True)
        layer_item = QTreeWidgetItem(["Layer"])
        objects_item = QTreeWidgetItem(["Objects"])
        pcb_print_item = QTreeWidgetItem(["PCB Print"])
        self.tree.addTopLevelItem(layer_item)
        self.tree.addTopLevelItem(objects_item)
        self.tree.addTopLevelItem(pcb_print_item)
        self.tree.setMinimumWidth(200)
        left_panel.addWidget(self.tree, 1)

        # Read/Save Settings buttons
        btn_row = QHBoxLayout()
        self.btn_read = QPushButton("Read Settings")
        self.btn_save = QPushButton("Save Settings")
        btn_row.addWidget(self.btn_read)
        btn_row.addWidget(self.btn_save)
        left_panel.addLayout(btn_row)

        # Left panel container
        left_widget = QWidget()
        left_widget.setLayout(left_panel)
        left_widget.setMaximumWidth(250)
        main_layout.addWidget(left_widget)

        # ==== RIGHT PANEL ====
        right_panel = QVBoxLayout()
        right_panel.setSpacing(6)

        # Green title bar
        title_bar = QHBoxLayout()
        lbl_layer = QLabel("Layer")
        lbl_layer.setStyleSheet("background-color: #1fa366; color: white; font-weight: bold; font-size: 16px; padding: 6px 20px; border-top-left-radius: 6px;")
        title_bar.addWidget(lbl_layer)
        title_bar.addStretch()
        lbl_pcb = QLabel("PCB Setting")
        lbl_pcb.setStyleSheet("background-color: #1fa366; color: white; font-weight: bold; font-size: 14px; padding: 6px 20px; border-top-right-radius: 6px;")
        title_bar.addWidget(lbl_pcb)
        title_widget = QWidget()
        title_widget.setLayout(title_bar)
        title_widget.setStyleSheet("background-color: #1fa366; border-radius: 6px;")
        right_panel.addWidget(title_widget)

        # Tabs
        self.tabs = QTabWidget()
        self.tab_physical = QWidget()
        self.tab_layer_settings = QWidget()
        self.tab_display = QWidget()
        self.tabs.addTab(self.tab_physical, "Physical Layer")
        self.tabs.addTab(self.tab_layer_settings, "Layer Settings")
        self.tabs.addTab(self.tab_display, "Display Layer Settings")
        right_panel.addWidget(self.tabs, 1)

        # Physical Layer Tab content
        tab_layout = QVBoxLayout(self.tab_physical)
        self.table = QTableWidget(3, 8)
        self.table.setHorizontalHeaderLabels([
            "Layer", "Thickness", "Type", "Plane layer", "Material",
            "Electric C.", "Dielectric C.", "Dielectric L."
        ])
        data = [
            ["Top", "0.043", "Conductor", "Route", "Copper", "59", "---", "---"],
            ["", "0.2", "Insulator", "Route", "FR4", "---", "4.6", "0.018"],
            ["Bottom", "0.043", "Conductor", "Route", "Copper", "59", "---", "---"]
        ]
        for row, row_data in enumerate(data):
            for col, value in enumerate(row_data):
                self.table.setItem(row, col, QTableWidgetItem(value))
        self.table.setMinimumHeight(180)
        self.refresh_material_comboboxes()
        tab_layout.addWidget(self.table)

          # Danh sách vật liệu
        self.conductor_materials = list(DEFAULT_CONDUCTOR)
        self.insulator_materials = list(DEFAULT_INSULATOR)

        

        # Kết nối nút Material Settings
        self.btn_material.clicked.connect(self.open_material_settings)


        # Nút Add, Delete, Layers, No. Layers, Material Settings
        btn_layout = QHBoxLayout()
        self.btn_add = QPushButton("Add")
        self.btn_delete = QPushButton("Delete")
        self.btn_layers = QPushButton("Layers")
        self.btn_material = QPushButton("Material Settings")
        btn_layout.addWidget(self.btn_add)
        btn_layout.addWidget(self.btn_delete)
        btn_layout.addWidget(self.btn_layers)
        self.spin_num_layers = QSpinBox()
        self.spin_num_layers.setRange(2, 15)
        self.spin_num_layers.setValue(self.count_physical_layers())
        self.spin_num_layers.setPrefix("No. Layers: ")
        btn_layout.addWidget(self.spin_num_layers)
        self.spin_num_layers.valueChanged.connect(self.set_num_layers)
        btn_layout.addStretch()
        btn_layout.addWidget(self.btn_material)
        tab_layout.addLayout(btn_layout)

        # Kết nối nút Add
        self.btn_add.clicked.connect(self.add_physical_layer)
        self.btn_delete.clicked.connect(self.delete_physical_layer)
        # Board/Plating thickness
        bottom_layout = QHBoxLayout()
        bottom_layout.addWidget(QLabel("Board Thickness"))
        self.board_thickness = QLineEdit("1.60")
        self.board_thickness.setMaximumWidth(60)
        bottom_layout.addWidget(self.board_thickness)
        bottom_layout.addWidget(QLabel("Plating Thickness"))
        self.plating_thickness = QLineEdit("0.025")
        self.plating_thickness.setMaximumWidth(60)
        bottom_layout.addWidget(self.plating_thickness)
        bottom_layout.addStretch()
        tab_layout.addLayout(bottom_layout)

        # Logo + OK/Cancel/Apply
        bottom_bar = QHBoxLayout()
        # Logo (dùng QPixmap nếu có file ảnh, ở đây dùng text)
        logo = QLabel()
        logo.setText('<b>NETCHANGER <span style="color:gold">Free</span></b>')
        logo.setStyleSheet("background: #2d2d2d; color: white; padding: 6px 18px; border-radius: 6px;")
        bottom_bar.addWidget(logo)
        bottom_bar.addStretch()
        self.btn_ok = QPushButton("OK")
        self.btn_cancel = QPushButton("Cancel")
        self.btn_apply = QPushButton("Apply")
        bottom_bar.addWidget(self.btn_ok)
        bottom_bar.addWidget(self.btn_cancel)
        bottom_bar.addWidget(self.btn_apply)
        right_panel.addLayout(bottom_bar)

        # Right panel container
        right_widget = QWidget()
        right_widget.setLayout(right_panel)
        main_layout.addWidget(right_widget, 1)
    def refresh_material_comboboxes(self):
        """
        Đặt lại combobox vật liệu cho từng dòng conductor/insulator.
        """
        for row in range(self.table.rowCount()):
            type_item = self.table.item(row, 2)
            if not type_item:
                continue
            if type_item.text() == "Conductor":
                combo = QComboBox()
                for name, _ in self.conductor_materials:
                    combo.addItem(name)
                # Set current value
                current = self.table.item(row, 4).text() if self.table.item(row, 4) else ""
                idx = combo.findText(current)
                if idx >= 0:
                    combo.setCurrentIndex(idx)
                combo.currentTextChanged.connect(lambda text, r=row: self.table.setItem(r, 4, QTableWidgetItem(text)))
                self.table.setCellWidget(row, 4, combo)
            elif type_item.text() == "Insulator":
                combo = QComboBox()
                for name, *_ in self.insulator_materials:
                    combo.addItem(name)
                current = self.table.item(row, 4).text() if self.table.item(row, 4) else ""
                idx = combo.findText(current)
                if idx >= 0:
                    combo.setCurrentIndex(idx)
                combo.currentTextChanged.connect(lambda text, r=row: self.table.setItem(r, 4, QTableWidgetItem(text)))
                self.table.setCellWidget(row, 4, combo)

    def add_physical_layer(self, update_spinbox=True):
        row_count = self.table.rowCount()
        insert_row = row_count - 1 if row_count > 1 else row_count
        conductor_data = ["noname", "0.035", "Conductor", "Route", "Copper", "59", "---", "---"]
        insulator_data = ["", "0.2", "Insulator", "Route", "FR4", "---", "4.6", "0.018"]
        self.table.insertRow(insert_row)
        self.refresh_material_comboboxes()
        for col, value in enumerate(conductor_data):
            item = QTableWidgetItem(value)
            if col == 0:
                item.setFlags(item.flags() | Qt.ItemIsEditable)
            self.table.setItem(insert_row, col, item)
        self.table.insertRow(insert_row + 1)
        for col, value in enumerate(insulator_data):
            item = QTableWidgetItem(value)
            if col == 0:
                item.setFlags(item.flags() | Qt.ItemIsEditable)
            self.table.setItem(insert_row + 1, col, item)
        if update_spinbox:
            self.spin_num_layers.setValue(self.count_physical_layers())
        self.table.editItem(self.table.item(insert_row, 0))
    def count_physical_layers(self):
        # Đếm số conductor (bao gồm cả Top và Bottom)
        count = 0
        for row in range(self.table.rowCount()):
            if self.table.item(row, 2) and self.table.item(row, 2).text() == "Conductor":
                count += 1
        return count
    def set_num_layers(self, num_layers):
        """
        Đặt lại số lớp vật lý conductor/insulator ở giữa Top và Bottom.
        """
        self.refresh_material_comboboxes()
        # Đếm số conductor hiện tại
        current = self.count_physical_layers()
        while current < num_layers:
            self.add_physical_layer()
            current += 1
        while current > num_layers:
            # Xoá cặp conductor/insulator cuối cùng ở giữa
            row_count = self.table.rowCount()
            # Tìm conductor cuối cùng ở giữa
            for row in range(row_count - 2, 0, -1):
                if self.table.item(row, 2) and self.table.item(row, 2).text() == "Conductor":
                    self.table.removeRow(row + 1)  # Xoá insulator sau
                    self.table.removeRow(row)      # Xoá conductor
                    break
            current -= 1   
    def update_num_layers(self):
        """
        Cập nhật số lớp vật lý (không tính Top/Bottom).
        """
        # Số lớp vật lý là tổng số dòng trừ 2 (Top, Bottom)
        num_layers = max(0, self.table.rowCount() - 2)
        self.lbl_num_layers.setText(f"No. Layers: {num_layers}")
    
    def open_material_settings(self):
        dlg = MaterialSettingsDialog(self.conductor_materials, self.insulator_materials, self)
        if dlg.exec_():
            self.conductor_materials, self.insulator_materials = dlg.get_materials()
            self.refresh_material_comboboxes()

    def delete_physical_layer(self):
        """
        Xoá một cặp physical layer (Conductor + Insulator) ở giữa Top và Bottom.
        """
        self.refresh_material_comboboxes()
        selected = self.table.currentRow()
        row_count = self.table.rowCount()
        if selected <= 0 or selected >= row_count - 1:
            # Không cho xoá Top hoặc Bottom
            return

        type_item = self.table.item(selected, 2)
        if type_item is None:
            return

        # Xoá cặp Conductor + Insulator ở giữa
        if type_item.text() == "Conductor":
            # Chỉ xoá nếu phía dưới là Insulator và phía dưới nữa không phải Bottom
            if selected + 1 < row_count - 1 and self.table.item(selected + 1, 2).text() == "Insulator":
                self.table.removeRow(selected + 1)  # Xoá insulator
                self.table.removeRow(selected)      # Xoá conductor
        elif type_item.text() == "Insulator":
            # Chỉ xoá nếu phía trên là Conductor và phía trên nữa không phải Top
            if selected - 1 > 0 and self.table.item(selected - 1, 2).text() == "Conductor":
                self.table.removeRow(selected)      # Xoá insulator
                self.table.removeRow(selected - 1)  # Xoá conductor

        self.update_num_layers()
class MaterialSettingsDialog(QDialog):
        def __init__(self, conductor_materials, insulator_materials, parent=None):
            super().__init__(parent)
            self.setWindowTitle("Material Settings")
            self.resize(600, 300)
            layout = QHBoxLayout(self)

            # Conductor
            self.table_conductor = QTableWidget(len(conductor_materials), 2)
            self.table_conductor.setHorizontalHeaderLabels(["Material Name", "Electric Conductivity"])
            for row, (name, cond) in enumerate(conductor_materials):
                self.table_conductor.setItem(row, 0, QTableWidgetItem(name))
                self.table_conductor.setItem(row, 1, QTableWidgetItem(cond))
            layout.addWidget(self.table_conductor)

            # Insulator
            self.table_insulator = QTableWidget(len(insulator_materials), 3)
            self.table_insulator.setHorizontalHeaderLabels(["Material Name", "Dielectric Constant", "Dielectric Loss Tanger"])
            for row, (name, const, loss) in enumerate(insulator_materials):
                self.table_insulator.setItem(row, 0, QTableWidgetItem(name))
                self.table_insulator.setItem(row, 1, QTableWidgetItem(const))
                self.table_insulator.setItem(row, 2, QTableWidgetItem(loss))
            layout.addWidget(self.table_insulator)

            # OK/Cancel
            btn_layout = QVBoxLayout()
            btn_ok = QPushButton("OK")
            btn_cancel = QPushButton("Cancel")
            btn_ok.clicked.connect(self.accept)
            btn_cancel.clicked.connect(self.reject)
            btn_layout.addWidget(btn_ok)
            btn_layout.addWidget(btn_cancel)
            layout.addLayout(btn_layout)

        def get_materials(self):
            # Lấy lại danh sách vật liệu từ bảng
            conductor = []
            for row in range(self.table_conductor.rowCount()):
                name = self.table_conductor.item(row, 0)
                cond = self.table_conductor.item(row, 1)
                if name and cond:
                    conductor.append((name.text(), cond.text()))
            insulator = []
            for row in range(self.table_insulator.rowCount()):
                name = self.table_insulator.item(row, 0)
                const = self.table_insulator.item(row, 1)
                loss = self.table_insulator.item(row, 2)
                if name and const and loss:
                    insulator.append((name.text(), const.text(), loss.text()))
            return conductor, insulator
if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    import sys
    app = QApplication(sys.argv)
    dlg = SettingsDialog()
    dlg.exec_()