from flask import Flask, redirect, url_for, render_template, request, jsonify, abort
from flask_cors import CORS
import json
import pyrebase

app=Flask(__name__)
CORS(app)


@app.route("/login", methods=["POST", "GET"])
def login():
    #try:
        logininfo = request.get_json()
        print(logininfo)
        return logininfo


@app.route("/getinfo", methods=["GET"])
def getInfo():
    centerinfo = request.get_json()
    print(centerinfo)
    return centerinfo

if __name__ == "__main__":
    app.run(debug=True)
