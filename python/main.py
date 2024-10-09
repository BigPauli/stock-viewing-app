from PyQt6 import QtCore, QtGui, QtWidgets
from get_api_app import Get_API_Application
import sys
from pathlib import Path


def open_api_key_window():
    # if the file ../data/apy_key.txt does not exist, open the window to get the user's API key before allowing them to use the app
    # https://stackoverflow.com/questions/82831/how-do-i-check-whether-a-file-exists-without-exceptions
    api_key = Path("../data/api_key.txt")
    if not api_key.is_file():
        # code borrowed from code automatically generated in get_api_key_ui.py
        app = QtWidgets.QApplication(sys.argv)
        form = Get_API_Application()
        form.show()
        sys.exit(app.exec())

if __name__ == "__main__":
    open_api_key_window()