from ui.get_api_key_ui import *
from PyQt6.QtWidgets import QApplication, QWidget
import sys
import requests

class Get_API_Application(QWidget):
    # this code is based off of code I have written in the past.
    # See: https://github.com/BigPauli/atomicrops-map-helper
    def __init__(self):
        # setup UI
        super(Get_API_Application, self).__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        # connect button to button_pushed function
        self.ui.pushButton.clicked.connect(self.button_pushed)

    def button_pushed(self):
        # reads user's input API key from plainTextEdit
        api_key = self.ui.plainTextEdit.toPlainText()

        # creates base_url and params for sample API call to make sure that API key is correct
        base_url = "https://api.twelvedata.com/price/"
        example_params = {
            "symbol": "AAPL",
            "apikey": api_key
        }
        response = requests.get(base_url, example_params)
        
        # checks to see if the response is valid, i.e. the user's API key is correct
        if response.json().get("code", 0) >= 400:
            # if not correct, red text appears and tells the user to try again
            self.ui.label_2.setText("Invalid Key. Try again.")
        else:
            # if the API key is correct, write it to the api_key.txt file
            with open("../data/api_key.txt", "w") as file:
                file.write(api_key)
            
            # close the window
            self.close()