# Form implementation generated from reading ui file 'main_app_ui.ui'
#
# Created by: PyQt6 UI code generator 6.7.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(400, 300)
        self.chart_type_comboBox = QtWidgets.QComboBox(parent=Form)
        self.chart_type_comboBox.setGeometry(QtCore.QRect(20, 50, 151, 22))
        self.chart_type_comboBox.setPlaceholderText("")
        self.chart_type_comboBox.setObjectName("chart_type_comboBox")
        self.label = QtWidgets.QLabel(parent=Form)
        self.label.setGeometry(QtCore.QRect(20, 25, 91, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.pushButton = QtWidgets.QPushButton(parent=Form)
        self.pushButton.setGeometry(QtCore.QRect(150, 260, 91, 23))
        self.pushButton.setObjectName("pushButton")
        self.label_3 = QtWidgets.QLabel(parent=Form)
        self.label_3.setGeometry(QtCore.QRect(20, 160, 121, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.comboBox_3 = QtWidgets.QComboBox(parent=Form)
        self.comboBox_3.setGeometry(QtCore.QRect(20, 190, 151, 22))
        self.comboBox_3.setPlaceholderText("")
        self.comboBox_3.setObjectName("comboBox_3")
        self.label_4 = QtWidgets.QLabel(parent=Form)
        self.label_4.setGeometry(QtCore.QRect(240, 160, 121, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.dateEdit_2 = QtWidgets.QDateEdit(parent=Form)
        self.dateEdit_2.setGeometry(QtCore.QRect(240, 190, 141, 22))
        self.dateEdit_2.setObjectName("dateEdit_2")
        self.label_2 = QtWidgets.QLabel(parent=Form)
        self.label_2.setGeometry(QtCore.QRect(20, 90, 91, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.comboBox_2 = QtWidgets.QComboBox(parent=Form)
        self.comboBox_2.setGeometry(QtCore.QRect(20, 120, 150, 22))
        self.comboBox_2.setPlaceholderText("")
        self.comboBox_2.setObjectName("comboBox_2")
        self.dateEdit = QtWidgets.QDateEdit(parent=Form)
        self.dateEdit.setGeometry(QtCore.QRect(20, 190, 141, 22))
        self.dateEdit.setObjectName("dateEdit")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "Type of Chart"))
        self.pushButton.setText(_translate("Form", "Generate Chart"))
        self.label_3.setText(_translate("Form", "Currency to Convert"))
        self.label_4.setText(_translate("Form", "Date of Conversion"))
        self.label_2.setText(_translate("Form", "Company"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Form = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec())
