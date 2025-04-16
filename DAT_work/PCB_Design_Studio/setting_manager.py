import json
import os

class SettingsManager:
    def __init__(self, settings_file="settings.json"):
        """
        Quản lý cài đặt của ứng dụng.
        :param settings_file: Đường dẫn đến file cài đặt.
        """
        self.settings_file = settings_file
        self.settings = {}
        self.load_settings()

    def load_settings(self):
        """
        Tải cài đặt từ file JSON.
        """
        if os.path.exists(self.settings_file):
            with open(self.settings_file, "r") as file:
                self.settings = json.load(file)
        else:
            self.settings = self.default_settings()
            self.save_settings()

    def save_settings(self):
        """
        Lưu cài đặt vào file JSON.
        """
        with open(self.settings_file, "w") as file:
            json.dump(self.settings, file, indent=4)

    def default_settings(self):
        """
        Trả về cài đặt mặc định.
        """
        return {
            "window_size": {"width": 1200, "height": 800},
            "grid_color": "#F0F0F0",
            "pad_color": "#0000FF",
            "track_color": "#FF0000",
            "recent_files": []
        }

    def get_setting(self, key, default=None):
        """
        Lấy giá trị của một cài đặt.
        :param key: Tên cài đặt.
        :param default: Giá trị mặc định nếu cài đặt không tồn tại.
        """
        return self.settings.get(key, default)

    def set_setting(self, key, value):
        """
        Đặt giá trị cho một cài đặt.
        :param key: Tên cài đặt.
        :param value: Giá trị cần đặt.
        """
        self.settings[key] = value
        self.save_settings()