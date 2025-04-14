import sys
from PyQt5.QtWidgets import QApplication, QMessageBox
from main_app import main_app
import traceback
def main():
    try:
        app = QApplication(sys.argv)
        pcb_app = main_app()
        pcb_app.showMaximized()
        sys.exit(app.exec_())
    except Exception as e:
        # Show a message box for unhandled exceptions
        error_dialog = QMessageBox()
        error_dialog.setIcon(QMessageBox.Critical)
        error_dialog.setWindowTitle("Fatal Error")
        error_dialog.setText(f"A fatal error occurred: {str(e)}")
        error_dialog.setDetailedText(traceback.format_exc())
        error_dialog.exec_()

if __name__ == '__main__':
    main()
