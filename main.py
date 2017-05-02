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


@app.route("/login", methods=['POST'])
def login():
    name = request.form.get('name')
    pw = request.form.get('pw')
    user_dic, select_result = db.select(name, pw)

    if select_result == 1:
        dic = {"error": 0, "msg": "OK", "result": user_dic}
        return jsonify(dic), 200
    elif select_result == 0:
        dic = {"error": 1, "msg": "Wrong password"}
        return jsonify(dic), 403
    elif select_result == -1:
        dic = {"error": 2, "msg": "User not exist"}
        return jsonify(dic), 404


@app.route("/register", methods=['POST'])
def register():
    name = request.form.get('name')
    pw = request.form.get('pw')
    reg_result = db.insert(name, pw)
    user_dic = {"name": name, "password": pw}
    print(reg_result)

    if reg_result == 1:
        dic = {"result": user_dic, "error": 0, "msg": "OK"}
        return jsonify(dic), 201
    elif reg_result == 0:
        dic = {"error": 11, "msg": "Exist such username"}
        return jsonify(dic), 409

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
