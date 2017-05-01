# -*- coding: utf-8 -*-
# @Author: gigaflower
# @Date:   2017-04-19 09:49:55
# @Last Modified by:   gigaflower
# @Last Modified time: 2017-04-19 10:10:13

from flask import Flask, request, jsonify
from database import db
import time

app = Flask("PaperMelody")
app.secret_key = "HgS diao"
db.init()

@app.route('/')
def main():
    return '''
        <style>
            h1 {
                font-size:150px;
                color: #ada;
                font-family: cursive;
                text-align: center;
                margin: 70px 30px;
                font-weight: normal;
            }
            p {
                color: #9a9;
                font-size:20px;
                text-align: right;
            }

        </style>
        <h1>Paper<br>Melody</h1>
        <p>%s</p>
        ''' % time.asctime()


@app.route("/login")
def login():
    name = request.args.get('name')
    pw = request.args.get('pw')
    dic, select_result = db.select(name, pw)

    if select_result == 1:
        # success
        return jsonify(dic), 200
    elif select_result == 0:
        string = "Wrong password"
        return jsonify(string), 403
    elif select_result == -1:
        string = "User not exist"
        return jsonify(string), 404


@app.route("/register")
def register():
    name = request.args.get('name')
    pw = request.args.get('pw')
    reg_result = db.insert(name, pw)
    print(reg_result)

    if reg_result == 1:
        dic = {"name": name, "password": pw}
        return jsonify(dic), 201
    elif reg_result == 0:
        string = "Exist such username"
        return jsonify(string), 409

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
