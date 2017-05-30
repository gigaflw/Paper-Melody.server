# -*- coding: utf-8 -*-
# @Author: gigaflower
# @Date:   2017-04-19 09:49:55
# @Last Modified by:   gigaflower
# @Last Modified time: 2017-04-19 10:10:13

from flask import Flask, request, jsonify, redirect, url_for, send_from_directory
from database import db
from config import ALLOWED_EXTENSIONS, UPLOAD_IMAGE_FOLDER
import os
import time

app = Flask("PaperMelody")
app.secret_key = "HgS diao"
app.config['UPLOAD_FOLDER'] = '.\\uploaded'
app.config['allowed_ext'] = ['mid']
db.init()


def allowed_img(imgname):
    return '.' in imgname and imgname.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


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
    user_dic, select_result = db.user_select(name, pw)

    if select_result == 0:
        dic = {"error": 0, "msg": "OK", "result": user_dic}
        return jsonify(dic), 200
    elif select_result == 1:
        dic = {"error": 1, "msg": "Wrong password"}
        return jsonify(dic), 403
    elif select_result == 2:
        dic = {"error": 2, "msg": "User not exist"}
        return jsonify(dic), 404


@app.route("/register", methods=['POST'])
def register():
    name = request.form.get('name')
    pw = request.form.get('pw')
    reg_result = db.user_insert(name, pw)
    user_dic = {"name": name, "password": pw}
    print(reg_result)

    if reg_result == 0:
        dic = {"result": user_dic, "error": 0, "msg": "OK"}
        return jsonify(dic), 201
    elif reg_result == 1:
        dic = {"error": 11, "msg": "Exist such username"}
        return jsonify(dic), 409


@app.route("/onlinemusics", methods=['GET'])
def onlinemusics():
    list_musics = db.music_get_all()
    dic_musics = {"count": len(list_musics), "musics": list_musics}
    dic = {"result": dic_musics, "error": 0, "msg": "OK"}
    return jsonify(dic), 200


@app.route("/uploadmusic", methods=['POST'])
def uploadmusic():
    name = request.form.get('name')
    author = request.form.get('author')
    date = request.form.get('date')
    link = request.form.get('link')
    img_link = request.form.get('imglink')

    upload_result = db.music_insert(name, author, date, link, img_link)
    if upload_result == 0:
        dic = {"error": 0, "msg": "OK"}
        return jsonify(dic), 201
    elif upload_result == 1:
        dic = {"error": 21, "msg": "Exist the same name"}
        return jsonify(dic), 409


@app.route("/uploadFile", methods=['POST'])
def uploadFile():
    UPLOAD_FOLDER = app.config['UPLOAD_FOLDER']
    # ALLOWED_EXT = ['mid']
    # if request.method == 'POST':
    file = request.files['userfile']
    if file and file.filename.rsplit('.', 1)[1] in app.config['allowed_ext']:
        file.save(os.path.join(UPLOAD_FOLDER, file.filename))
        dic = {"link": url_for('uploaded_file', filename=file.filename), "error": 0, "msg": "OK"}
        # return dic, 200
        return dic['link'], 202
    else:
        return "error", 410
        # return {"link": '', "error": 1, "msg": "failed"}, 502


@app.route('/uploaded/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


@app.route("/reset", methods=['GET'])
def reset():
    db.reset_db()
    return "reset success", 200


@app.route("/getcomment", methods=['GET'])
def getcomment():
    musicID = request.args.get("musicID")
    while musicID[-1] == '/':
        musicID = musicID[:-1]
    # musicID=request.form.get("id")
    print(musicID)
    comments = db.get_comment(musicID)
    dic_musics = {"count": len(comments), "musics": comments}
    if len(comments) <= 0:
        dic = {"error": 21, "msg": "No such file"}
        return jsonify(dic), 404
    else:
        dic = {"result": dic_musics, "error": 0, "msg": "OK"}
        print (dic)
        return jsonify(dic), 200


@app.route("/getallcomment", methods=['GET'])
def getallcomment():
    res = db.get_all_comment()
    print(str(res))
    return res


@app.route("/uploadcomment", methods=['POST'])
def uploadcomment():
    print(request.form)
    musicID = request.form.get("musicID")
    user = request.form.get("user")
    comment = request.form.get("comment")
    time = request.form.get("time")
    upload_result = db.upload_comment(str(musicID) + str(time), musicID, user, time, comment);
    if upload_result == 0:
        dic = {"error": 0, "msg": "OK"}
        return jsonify(dic), 201
    elif upload_result == 1:
        dic = {"error": 21, "msg": "I dont know why"}
        return jsonify(dic), 409


@app.route("/uploadimg", methods=['POST'])
def uploadimg():
    file = request.files['image']
    if file and allowed_img(file.filename):
        current_time = time.localtime()
        filename =  time.strftime("%Y%m%d%H%M%S", current_time) + '.' + file.filename.rsplit('.', 1)[1]
        link = "/getimage/" + filename
        path = UPLOAD_IMAGE_FOLDER + "/" + filename   # windows系统测试时使用下面语句会出现路径双斜杠的问题
        #path = os.path.join(UPLOAD_IMAGE_FOLDER, filename)   # 服务器使用
        file.save(path)
        print ("upload success: " + filename)
        dic = {"imglink": link, "error": 0, "msg": "Upload img success"}
        return jsonify(dic), 200
    dic = {"error": 31, "msg": "Upload img failure"}
    return jsonify(dic), 409


@app.route("/getimage/<img_name>", methods=['GET'])
def getimage(img_name):
    path = UPLOAD_IMAGE_FOLDER + "/" + img_name   # windows系统测试时使用下面语句会出现路径双斜杠的问题
    print (path)
    if os.path.isfile(path):
    #if os.path.isfile(os.path.join(UPLOAD_IMAGE_FOLDER, img_name)):  # 服务器使用
        return send_from_directory(UPLOAD_IMAGE_FOLDER, img_name, as_attachment=True)
    abort(404)


if __name__ == '__main__':
    # db.upload_comment('comment1','music1','tth','2018-2-3-12-23-2','this is great!')
    db.reset_db()
    db.music_insert("National song", "zb", "2017-05-04", "link1", "")
    db.music_insert("Gongqingtuan", "pyj", "2017-04-04", "link2", "")
    db.music_insert("shaoxiandui", "tth", "2015-05-04", "link3", "")
    app.run(host='0.0.0.0', port=80)
