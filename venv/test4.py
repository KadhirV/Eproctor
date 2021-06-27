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


def analyzefunction(name):
    with sr.Microphone() as source:
        while True:

            f = open("speechlogfiles/{} - speechlogfile.txt".format(name), "a+")
            audio_text = r.listen(source)

            # try:
            finaltext = r.recognize_google(audio_text)
            time = datetime.datetime.now()

            if (predict(finaltext)) == 1 or ("*" in finaltext):
                f.write('{} {}: {}\n{} Warning issued. {} said: "{}." Can not say this. you have been warned.'.format(time.strftime("[%Y/%m/%d %H:%M:%S]"), name, finaltext, time.strftime("[%Y/%m/%d %H:%M:%S]"), name, finaltext))
                warnings.append(str(time.strftime("%Y/%m/%d %H:%M:%S")))

                return ('{} {}: {}\n{} Warning issued. {} said: "{}." Can not say this. you have been warned.'.format(time.strftime("[%Y/%m/%d %H:%M:%S]"), name, finaltext, time.strftime("[%Y/%m/%d %H:%M:%S]"),name, finaltext))

            f.write("{} {}: {}\n".format(time.strftime("[%Y/%m/%d %H:%M:%S]"), name, finaltext))

            f.close()
            storage.child("{} - speechlogfile.txt".format(name)).put("speechlogfiles/{} - speechlogfile.txt".format(name))

            return ("{} {}: {}".format(time.strftime("[%Y/%m/%d %H:%M:%S]"), name, finaltext))

            # except:
            #     return("can not hear anything")






# you know what to do to fix this. remember to switch order of if statement so it checks for shit before it has a chance to return.