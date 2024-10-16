from ui.main_app_ui import *
from db_reader import get_column_from_company
from chart_generator import change_in_stock_chart, sector_comparison_chart, currency_exchange_chart
from PyQt6.QtWidgets import QApplication, QWidget
from datetime import date
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

        # get list of all ui elements that may need to be hidden and hide them
        self.hideable_ui_elements = [self.ui.label_2, self.ui.comboBox_2, self.ui.dateEdit, self.ui.comboBox_3, self.ui.label_4, self.ui.dateEdit_2]

        # populate all comboBoxes
        self.populate_combo_boxes()

        # connect change event to chart_type_comboBox
        # https://stackoverflow.com/questions/44707794/pyqt-combo-box-change-value-of-a-label
        self.ui.chart_type_comboBox.currentTextChanged.connect(self.onChanged)
        
        # connect push event to pushButton
        # https://stackoverflow.com/questions/15080731/calling-a-function-upon-button-press
        self.ui.pushButton.clicked.connect(self.onPushed)

        # set starting ui to default value
        self.onChanged()

        # set dateEdit and dateEdit2 to defaulted dates of today
        # https://www.geeksforgeeks.org/get-current-date-using-python/
        today = date.today()
        self.ui.dateEdit.setDate(today)
        self.ui.dateEdit_2.setDate(today)

    def onChanged(self):
        # create dictionary that contains functions to call when chart_type_comboBox is changed to certain value
        onChanged_actions = {
            "Change in Stock": self.change_to_stock_change,
            "Sector Comparison": self.change_to_sector_comparison,
            "Currency Exchange Rate": self.change_to_currency_exchange
        }
        onChanged_actions[self.ui.chart_type_comboBox.currentText()]()

    def onPushed(self):
        # when the "generate chart" button is pushed, call the corresponding function from chart_generator.py with arguments read from inputs
        curr = self.ui.chart_type_comboBox.currentText()
        if curr == "Change in Stock" and self.ui.dateEdit.date() < self.ui.dateEdit_2.date():
            change_in_stock_chart(self.ui.comboBox_2.currentText(), self.ui.dateEdit.date(), self.ui.dateEdit_2.date(), save_data=self.ui.checkBox.isChecked())
        elif curr == "Sector Comparison":
            sector_comparison_chart(self.ui.dateEdit.date(), save_data=self.ui.checkBox.isChecked())
        else:
            currency_exchange_chart(self.ui.comboBox_3.currentText(), self.currencies, self.ui.dateEdit_2.date(), save_data=self.ui.checkBox.isChecked())

    def change_to_stock_change(self):
        self.hide_hideables()
        self.load_stock_change_elements()

    def change_to_sector_comparison(self):
        self.hide_hideables()
        self.load_sector_comparison_elements()

    def change_to_currency_exchange(self):
        self.hide_hideables()
        self.load_currency_exchange_elements()

    def hide_hideables(self):
        # hide all ui elements (hideables) that are not shared between all ui modes
        for element in self.hideable_ui_elements:
            element.hide()

    def populate_combo_boxes(self):
        # populate chart_type_comboBox
        for item in ["Change in Stock", "Sector Comparison", "Currency Exchange Rate"]:
            self.ui.chart_type_comboBox.addItem(item)
        
        # populate comboBox_3 with common currency types
        self.currencies = ["USD", "EUR", "GBP", "JPY", "CHF", "AUD", "CAD", "CNY", "NZD", "INR", "SEK", "ZAR", "HKD"]
        for item in self.currencies:
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
        self.ui.label_2.setText("Company")
        self.ui.label_3.setText("Start Date")
        self.ui.label_4.setText("End Date")


    def load_sector_comparison_elements(self):
        # show relevant hideables
        self.ui.dateEdit.show()

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