import speech_recognition as sr
from cuss_inspect import predict
import datetime
import pyrebase
import urllib

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

r = sr.Recognizer()

warnings = []

email = input("Enter email to sign in: ")
password = input("Enter password to sign in: ")
formattedemail = email.replace(".", "").replace("@", "")

try:
    auth.sign_in_with_email_and_password(email, password)
    print("Successfully logged in with username: ", email)
except:
    print("Invalid username or password, try again")

name = db.child(formattedemail).get()
name = name.val()
name = name["Name"].lower()

f = open("speechlogfiles/{} - speechlogfile.txt".format(name), "a+")

print("you are now being recorded and your speech is analyzed for abusive language.")

with sr.Microphone() as source:
    while (len(warnings) <= 1):

        f = open("speechlogfiles/{} - speechlogfile.txt".format(name), "a+")
        audio_text = r.listen(source)

        try:
            finaltext = r.recognize_google(audio_text)
            time = datetime.datetime.now()

            print("{} {}: {}".format(time.strftime("[%Y/%m/%d %H:%M:%S]"), name, finaltext))

            f.write("{} {}: {}\n".format(time.strftime("[%Y/%m/%d %H:%M:%S]"), name, finaltext))

            if (predict(finaltext)) == 1 or ("*" in finaltext):
                print('{} Warning issued. {} said: "{}." Can not say this. you have been warned.'.format(
                    time.strftime("[%Y/%m/%d %H:%M:%S]"), name, finaltext))

                f.write('{} Warning issued. {} said: "{}." Can not say this. you have been warned.\n'.format(
                    time.strftime("[%Y/%m/%d %H:%M:%S]"), name, finaltext))
                warnings.append(str(time.strftime("%Y/%m/%d %H:%M:%S")))

            f.close()
            storage.child("{} - speechlogfile.txt".format(name)).put(
                "speechlogfiles/{} - speechlogfile.txt".format(name))

        except:
            print("can not hear anything")





