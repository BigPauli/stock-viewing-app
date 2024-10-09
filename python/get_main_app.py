from ui.main_app_ui import *
from db_reader import get_column_from_company
from PyQt6.QtWidgets import QApplication, QWidget
import sys
import requests

class Main_Application(QWidget):
    # this code is based off of code I have written in the past.
    # See: https://github.com/BigPauli/atomicrops-map-helper
    def __init__(self):
        # setup UI
        super(Main_Application, self).__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)

        # get user's API key
        with open("../data/api_key.txt", "r") as f:
            self.api_key = f.read()

        # get list of all ui elements that may need to be hidden and hide them
        self.hideable_ui_elements = [self.ui.label_2, self.ui.comboBox_2, self.ui.dateEdit, self.ui.comboBox_3]

        # populate all comboBoxes
        self.populate_combo_boxes()

        # connect change event to chart_type_comboBox
        # https://stackoverflow.com/questions/44707794/pyqt-combo-box-change-value-of-a-label
        self.ui.chart_type_comboBox.currentTextChanged.connect(self.onChanged)
        
        # set starting ui to default value
        self.onChanged()


    def onChanged(self):
        # create dictionary that contains functions to call when chart_type_comboBox is changed to certain value
        onChanged_actions = {
            "Change in Stock": self.change_to_stock_change,
            "Stock Comparison": self.change_to_stock_comparison,
            "Currency Exchange Rate": self.change_to_currency_exchange
        }
        onChanged_actions[self.ui.chart_type_comboBox.currentText()]()

    def change_to_stock_change(self):
        self.hide_hideables()
        self.load_stock_change_elements()

    def change_to_stock_comparison(self):
        self.hide_hideables()
        self.load_stock_comparison_elements()

    def change_to_currency_exchange(self):
        self.hide_hideables()
        self.load_currency_exchange_elements()

    def hide_hideables(self):
        # hide all ui elements (hideables) that are not shared between all ui modes
        for element in self.hideable_ui_elements:
            element.hide()

    def populate_combo_boxes(self):
        # populate chart_type_comboBox
        for item in ["Change in Stock", "Stock Comparison", "Currency Exchange Rate"]:
            self.ui.chart_type_comboBox.addItem(item)
        
        # populate comboBox_3 with common currency types
        for item in ["USD", "EUR", "GBP", "JPY", "CHF", "AUD", "CAD", "CNY", "NZD", "INR", "BZR", "SEK", "ZAR", "HKD"]:
            self.ui.comboBox_3.addItem(item)

        # populate comboBox_2 with all SMP 500 companies from database
        for item in sorted(get_column_from_company("name", flatten=True)):
            self.ui.comboBox_2.addItem(item)
    
    def load_stock_change_elements(self):
        # show relevant hideables
        self.ui.label_2.show()
        self.ui.comboBox_2.show()
        self.ui.dateEdit.show()
        self.ui.label_4.show()
        self.ui.dateEdit_2.show()

        # change labels where appropriate
        self.ui.label_3.setText("Start Date")
        self.ui.label_4.setText("End Date")


    def load_stock_comparison_elements(self):
        # show relevant hideables
        self.ui.label_2.show()
        self.ui.comboBox_2.show()
        self.ui.dateEdit.show()
        self.ui.label_4.show()
        self.ui.dateEdit_2.show()

        # change labels where appropriate
        self.ui.label_3.setText("Date")

    def load_currency_exchange_elements(self):
        # show relevant hideables
        self.ui.label_4.show()
        self.ui.dateEdit_2.show()
        self.ui.comboBox_3.show()

        # change labels where appropriate
        self.ui.label_3.setText("Currency to Convert")
        self.ui.label_4.setText("Date")