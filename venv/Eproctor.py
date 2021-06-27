import sys
import urllib.request

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.uic import loadUi
import pyrebase
import json
import os
import time

import analyzer

currentteacher = ""
currentstudent = ""

firebaseConfig = {
    "apiKey": "AIzaSyAphLwfwVVsyZUwG-GNuChX4VLNL8iR-eM",
    "authDomain": "eproctor-9a9e6.firebaseapp.com",
    "databaseURL": "https://eproctor-9a9e6-default-rtdb.firebaseio.com/",
    "projectId": "eproctor-9a9e6",
    "storageBucket": "eproctor-9a9e6.appspot.com",
    "messagingSenderId": "1094456342195",
    "appId": "1:1094456342195:web:585427d4ba4294654ca2c6",
    "measurementId": "G-Y1SEVKFJQB"
  };

firebase = pyrebase.initialize_app(firebaseConfig)

db = firebase.database()
auth = firebase.auth()
storage = firebase.storage()

datatemplate = {
    "Name": "",
    "TeacherAcc": 0,
    "email address": "",
    "NOstudents": 0,
    "studentList": [""]
}


class Login(QMainWindow):
    def __init__(self):
        super(Login, self).__init__()
        loadUi("uifiles\Login_eproctor.ui", self)
        self.LoginButton1.clicked.connect(self.loginfunction)
        self.EnterPassword1.setEchoMode(QtWidgets.QLineEdit.Password)
        self.SignUp1.clicked.connect(self.gotocreate)
        self.loginmessage.setText("")

    def loginfunction(self):
        email = self.EnterUsername1.text()
        password = self.EnterPassword1.text()

        try:
            auth.sign_in_with_email_and_password(email, password)
            # print("Successfully logged in with username: ", email)
            formattedemail = email.replace(".", "").replace("@", "")

            global currentteacher, currentstudent
            currentteacher = formattedemail

            validate = db.child(formattedemail).get()
            validate = validate.val()

            if (validate["TeacherAcc"] == 0):
                currentstudent = formattedemail
                self.studentview()
            else:
                currentteacher = formattedemail
                self.teacherview()
                
        except:
            self.loginmessage.setText("Invalid username or password, try again")

    def gotocreate(self):
        Signup_eproctor = CreateAcc()
        widget.addWidget(Signup_eproctor)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def teacherview(self):
        teacher_eproctor = TeacherView()
        widget.addWidget(teacher_eproctor)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def studentview(self):
        student_eproctor = StudentView()
        widget.addWidget(student_eproctor)
        widget.setCurrentIndex(widget.currentIndex() + 1)


class CreateAcc(QMainWindow):
    def __init__(self):
        super(CreateAcc, self).__init__()
        loadUi("uifiles\Signup_eproctor.ui", self)
        self.pushButton_1.clicked.connect(self.createaccfunction)
        self.EnterPassword2.setEchoMode(QtWidgets.QLineEdit.Password)
        self.EnterRePassword.setEchoMode(QtWidgets.QLineEdit.Password)
        self.pushButton_2.clicked.connect(self.gotologin)
        self.signinmessage.setText("")

    def createaccfunction(self):
        name = self.EnterName.text()
        email = self.EnterEmail.text()
        # using this cause database cant use email to child
        formattedemail = email.replace(".", "").replace("@", "")

        TeacherAcc = self.TeacherCheckBox.isChecked()

        if self.EnterPassword2.text() == self.EnterRePassword.text():
            password = self.EnterPassword2.text()
            try:
                auth.create_user_with_email_and_password(email, password)
                self.signinmessage.setText("Successfully created an account")
                #print("jhdfgkjgjkdfhg")
                data = datatemplate
                data["Name"] = name
                data["TeacherAcc"] = 1 if TeacherAcc else 0
                data["email address"] = email
                db.child(formattedemail).set(data)
            except:
                self.signinmessage.setText("Something went wrong. Please try again.")

            login = Login()
            widget.addWidget(login)
            widget.setCurrentIndex(widget.currentIndex() + 1)

    def gotologin(self):
        login = Login()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex() - 1)


class TeacherView(QMainWindow):
    def __init__(self):
        super(TeacherView, self).__init__()
        loadUi("uifiles\Teacher_eproctor.ui", self)
        self.pushButton_2.clicked.connect(self.logfunction)
        self.pushButton.clicked.connect(self.homefunction)
        self.pushButton_3.clicked.connect(self.addstudent)

    def logfunction(self):
        studentName = self.StudentName.text()

        global currentteacher
        stulist = db.child(currentteacher).get()
        stulist = stulist.val()

        if (not (studentName in stulist["studentList"])):
            self.textBrowser.setText(
                "This student does not exist under the list of your students. Add them and try again, or check if you spelled the name right and everything is in lower case.")
        else:
            filename = "{} - speechlogfile.txt".format(studentName).lower()

        try:
            url = storage.child("{}".format(filename)).get_url(None)

            unformattedlogtext = r"{}".format(str(urllib.request.urlopen(url).read()))
            logtext = unformattedlogtext.lstrip("b'").rstrip("'")
            logtext = logtext.replace(r'\r\n', '\n')
            self.textBrowser.setText("Speech Log files for {}:".format(studentName))
            self.textBrowser.append(logtext)


        except:
            print("Error on app. This student does not exist")
            self.textBrowser.setText(
                "This student does not exist under the list of your students. Add them and try again, or check if you spelled the name right and everything is in lower case.")

    def homefunction(self):
        login = Login()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex() - 1)

    def addstudent(self):
        studentName = self.lineEdit_2.text()
        global currentteacher
        stucount = db.child(currentteacher).get()
        stucount = stucount.val()
        stucount = stucount["NOstudents"]  # supposed to be 0
        stucount += 1

        db.child(currentteacher).child("studentList").update({stucount - 1: studentName})

        db.child(currentteacher).update({"NOstudents": stucount})

        self.lineEdit_2.clear()
        self.textBrowser.append("student {} successfully added".format(studentName))


class StudentView(QMainWindow):
    def __init__(self):
        super(StudentView, self).__init__()
        loadUi("uifiles\Student_eproctor.ui", self)
        self.thread = studentthread()
        self.thread.start()
        self.textBrowser.clear()
        self.textBrowser.append("you are now being recorded and your speech is analyzed for abusive language.")
        self.homeButton.clicked.connect(self.gotologin)
        self.thread.returnvalue.connect(self.updatefunction)

    def updatefunction(self, val):
        #delete next few comments if anything broken
        # global currentstudent
        # name = db.child(currentstudent).get()
        # name = name.val()
        # name = name["Name"].lower()
        # filename = "{} - speechlogfile.txt".format(name).lower()
        #
        # url = storage.child("{}".format(filename)).get_url(None)
        #
        # unformattedlogtext = r"{}".format(str(urllib.request.urlopen(url).read()))
        # logtext = unformattedlogtext.lstrip("b'").rstrip("'")
        # logtext = logtext.replace(r'\r\n', '\n')
        # self.textBrowser.setText(logtext)
        self.textBrowser.append(val)

    def gotologin(self):
        login = Login()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex() - 1)

class studentthread(QtCore.QThread):
    returnvalue = QtCore.pyqtSignal(str)

    def __init__(self):
        super(studentthread, self).__init__()

    def run(self):

        global currentstudent
        name = db.child(currentstudent).get()
        name = name.val()
        name = name["Name"].lower()

        while True:
            printvalue = analyzer.analyzefunction(name)
            self.returnvalue.emit(printvalue)

app = QApplication(sys.argv)
mainwindow = Login()
widget = QtWidgets.QStackedWidget()
widget.addWidget(mainwindow)
widget.show()
app.exec_()