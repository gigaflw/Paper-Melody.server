# -*- coding: utf-8 -*-
# @Author: gigaflower
# @Date:   2017-04-19 09:49:55
# @Last Modified by:   gigaflower
# @Last Modified time: 2017-04-19 10:10:13

from flask import Flask, request, jsonify, redirect, url_for, send_from_directory, abort
from database import db
from config import ALLOWED_EXTENSIONS, UPLOAD_IMAGE_FOLDER, UPLOAD_FOLDER, ALLOWED_FILE_EXTENSIONS, UPLOAD_AVATAR_FOLDER
import os, time, platform

app = Flask("PaperMelody")
app.secret_key = "HgS diao"
db.init()


def allowed_img(imgname):
    return '.' in imgname and imgname.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_FILE_EXTENSIONS


def reset_database():
    db.reset_db()
    db.music_insert("四月は君の嘘", "Anonymous User", 0, "default.png", "2017-05-04 11:40:50", "default (1).mp3", "default (1).jpg", "挫けそうになる私を支えてください")
    db.music_insert("River Flows in You", "Anonymous User", 0, "default.png", "2017-04-04 11:40:50", "default (2).mp3", "default (2).jpg", "River Flows in You")
    db.music_insert("天空之城", "Anonymous User", 0, "default.png", "2015-05-04 11:40:50", "default (3).mp3", "default (3).jpg", "天空之城（钢琴版）")
    #db.insert_message("系统消息", 0, 0, "2017-06-15", "欢迎来到Paper Melody!!")



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
    #print (user_dic)

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
    user_dic, reg_result = db.user_insert(name, pw)

    if reg_result == 0:
        dic = {"result": user_dic, "error": 0, "msg": "OK"}
        return jsonify(dic), 200
    elif reg_result == 1:
        dic = {"error": 11, "msg": "Exist such username"}
        return jsonify(dic), 409


@app.route("/user/password", methods=['POST'])
def update_password():
    userID = int(request.form.get('userID'))
    old_pw = request.form.get('oldPassword')
    new_pw = request.form.get('newPassword')
    user_dic, result = db.user_update_password(userID, old_pw, new_pw)

    if result == 0:
        dic = {"result": user_dic, "error": 0, "msg": "OK"}
        return jsonify(dic), 200
    elif result == 1:
        dic = {"error": 1, "msg": "Wrong password"}
        return jsonify(dic), 403


@app.route("/user/nickname", methods=['POST'])
def update_nickname():
    userID = int(request.form.get('userID'))
    nickname = request.form.get('nickname')
    user_dic, result = db.user_update_nickname(userID, nickname)

    if result == 0:
        dic = {"result": user_dic, "error": 0, "msg": "OK"}
        return jsonify(dic), 200
    elif result == 1:
        dic = {"error": 11, "msg": "Exist such username"}
        return jsonify(dic), 409


@app.route("/user/avatar", methods=['POST'])
def update_avatar():
    userID = int(request.form.get('userID'))
    avatar_name = request.form.get('avatarName')
    user_dic, old_name = db.user_update_avatar(userID, avatar_name)
    if platform.system() == "Windows":
        path = UPLOAD_AVATAR_FOLDER + "/" + old_name   # windows系统测试时使用下面语句会出现路径双斜杠的问题
    else:
        path = os.path.join(UPLOAD_AVATAR_FOLDER, old_name)  # 服务器使用
    if os.path.isfile(path):
        os.remove(path)
    dic = {"result": user_dic, "error": 0, "msg": "OK"}
    return jsonify(dic), 200


@app.route("/upload/avatar", methods=['POST'])
def upload_avatar():
    file = request.files['avatar']
    if file and allowed_img(file.filename):
        current_time = time.localtime()
        filename =  time.strftime("%Y%m%d%H%M%S", current_time) + '.' + file.filename.rsplit('.', 1)[1]
        if platform.system() == "Windows":
            path = UPLOAD_AVATAR_FOLDER + "/" + filename   # windows系统测试时使用下面语句会出现路径双斜杠的问题
        else:
            path = os.path.join(UPLOAD_AVATAR_FOLDER, filename)   # 服务器使用
        file.save(path)
        dic = {"fileName": filename, "error": 0, "msg": "Upload file success"}
        return jsonify(dic), 200
    dic = {"error": 31, "msg": "Upload file failure"}
    return jsonify(dic), 404


@app.route("/download/avatar/<fname>", methods=['GET'])
def download_avatar(fname):
    if platform.system() == "Windows":
        path = UPLOAD_AVATAR_FOLDER + "/" + fname   # windows系统测试时使用下面语句会出现路径双斜杠的问题
    else:
        path = os.path.join(UPLOAD_AVATAR_FOLDER, fname)  # 服务器使用
    if os.path.isfile(path):
        return send_from_directory(UPLOAD_AVATAR_FOLDER, fname, as_attachment=True)
    abort(404)


@app.route("/onlinemusics", methods=['GET'])
def onlinemusics():
    order = int(request.args.get("order"))
    list_musics = db.music_get_all()
    if (order == 1):
        list_musics = sorted(list_musics, key = lambda e: e.__getitem__('viewNum')) # 按照热度排序
        #print (list_musics)
    elif (order == 2):
        list_musics = sorted(list_musics, key = lambda e: e.__getitem__('upvoteNum')) # 按照点赞数排序
        #print (list_musics)
    list_musics.reverse()
    #print (order)
    dic_musics = {"count": len(list_musics), "musics": list_musics}
    dic = {"result": dic_musics, "error": 0, "msg": "OK"}
    return jsonify(dic), 200


@app.route("/upload/music", methods=['POST'])
def upload_music():
    name = request.form.get('name')
    author = request.form.get('author')
    authorID = int(request.form.get('authorID'))
    date = request.form.get('date')
    music_name = request.form.get('musicName')
    img_name = request.form.get('imgName')
    info = request.form.get('musicInfo')
    author_avatar = request.form.get('authorAvatarName')

    upload_result = db.music_insert(name, author, authorID, author_avatar, date, music_name, img_name, info)
    if upload_result == 0:
        dic = {"error": 0, "msg": "OK"}
        return jsonify(dic), 200
    elif upload_result == 1:
        dic = {"error": 21, "msg": "Exist the same name"}
        return jsonify(dic), 409


@app.route("/download/music/<fname>", methods=['GET'])
def download_music(fname):
    if platform.system() == "Windows":
        path = UPLOAD_FOLDER + "/" + fname   # windows系统测试时使用下面语句会出现路径双斜杠的问题
    else:
        path = os.path.join(UPLOAD_FOLDER, fname)  # 服务器使用
    if os.path.isfile(path):
        return send_from_directory(UPLOAD_FOLDER, fname, as_attachment=True)
    abort(404)


@app.route("/reset", methods=['GET'])
def reset():
    reset_database()
    dic = {"error": 0, "msg": "OK"}
    return jsonify(dic), 200


@app.route("/download/comment", methods=['GET'])
def get_comment():
    musicID = int(request.args.get("musicID"))
    #print(musicID)
    comments = db.get_comment(musicID)
    dic_musics = {"count": len(comments), "comments": comments}
    dic = {"result": dic_musics, "error": 0, "msg": "OK"}
    #print (dic)
    return jsonify(dic), 200


@app.route("/download/allcomment", methods=['GET'])
def get_all_comment():
    res = db.get_all_comment()
    #print(str(res))
    return res


@app.route("/upload/comment", methods=['POST'])
def upload_comment():
    #print(request.form)
    musicID = int(request.form.get("musicID"))
    user = request.form.get("user")
    userID = int(request.form.get("userID"))
    user_avatar = request.form.get("userAvatarName")
    reply_userID = int(request.form.get("replyUserID"))
    comment = request.form.get("comment")
    time = request.form.get("time")
    db.upload_comment(musicID, user, userID, user_avatar, time, comment)
    if reply_userID > 0:   # 评论回复时该值大于0，需要向被评论者发送通知
        db.insert_message(user, userID, reply_userID, time, comment)
    dic = {"error": 0, "msg": "OK"}
    return jsonify(dic), 200


@app.route("/upload/img", methods=['POST'])
def upload_img():
    file = request.files['image']
    if file and allowed_img(file.filename):
        current_time = time.localtime()
        filename =  time.strftime("%Y%m%d%H%M%S", current_time) + '.' + file.filename.rsplit('.', 1)[1]
        if platform.system() == "Windows":
            path = UPLOAD_IMAGE_FOLDER + "/" + filename   # windows系统测试时使用下面语句会出现路径双斜杠的问题
        else:
            path = os.path.join(UPLOAD_IMAGE_FOLDER, filename)   # 服务器使用
        file.save(path)
        #print ("upload success: " + filename)
        dic = {"fileName": filename, "error": 0, "msg": "Upload file success"}
        return jsonify(dic), 200
    dic = {"error": 31, "msg": "Upload file failure"}
    return jsonify(dic), 404


@app.route("/upload/musicfile", methods=['POST'])
def upload_music_file():
    file = request.files['file']
    if file and allowed_file(file.filename):
        current_time = time.localtime()
        filename =  time.strftime("%Y%m%d%H%M%S", current_time) + '.' + file.filename.rsplit('.', 1)[1]
        if platform.system() == "Windows":
            path = UPLOAD_FOLDER + "/" + filename   # windows系统测试时使用下面语句会出现路径双斜杠的问题
        else:
            path = os.path.join(UPLOAD_FOLDER, filename)   # 服务器使用
        file.save(path)
        #print ("upload success: " + filename)
        dic = {"fileName": filename, "error": 0, "msg": "Upload file success"}
        return jsonify(dic), 200
    dic = {"error": 31, "msg": "Upload file failure"}
    return jsonify(dic), 404


@app.route("/download/img/<img_name>", methods=['GET'])
def get_image(img_name):
    if platform.system() == "Windows":
        path = UPLOAD_IMAGE_FOLDER + "/" + img_name   # windows系统测试时使用下面语句会出现路径双斜杠的问题
    else:
        path = os.path.join(UPLOAD_IMAGE_FOLDER, img_name)  # 服务器使用
    if os.path.isfile(path):
        return send_from_directory(UPLOAD_IMAGE_FOLDER, img_name, as_attachment=True)
    abort(404)


@app.route("/addview", methods=['POST'])
def add_view():
    musicID = request.form.get("musicID")
    db.music_update_num(musicID, 0, 1)
    dic = {"error": 0, "msg": "OK"}
    return jsonify(dic), 200


@app.route("/upvote/status", methods=['GET'])
def get_upvote_status():
    userID = int(request.args.get("userID"))
    musicID = int(request.args.get("musicID"))
    result, status = db.judge_favorites(userID, musicID)
    dic = {"upvoteNum": result.get("upvoteNum"), "viewNum": result.get("viewNum"), "status": status, "error": 0, "msg": "OK"}
    return jsonify(dic), 200


@app.route("/upvote/add", methods=['POST'])
def add_upvote():
    userID = int(request.form.get("userID"))
    musicID = int(request.form.get("musicID"))
    db.add_favorites(userID, musicID)
    db.music_update_num(musicID, 1, 0)
    dic = {"error": 0, "msg": "OK"}
    return jsonify(dic), 200


@app.route("/upvote/cancel", methods=['POST'])
def cancel_upvote():
    userID = int(request.form.get("userID"))
    musicID = int(request.form.get("musicID"))
    db.delete_favorites(userID, musicID)
    db.music_update_num(musicID, -1, 0)
    dic = {"error": 0, "msg": "OK"}
    return jsonify(dic), 200


@app.route("/download/favorites", methods=['GET'])
def get_favorites():
    userID = int(request.args.get("userID"))
    list_musics = db.get_favorites(userID)
    list_musics.reverse()
    #print (list_musics)
    dic_musics = {"count": len(list_musics), "musics": list_musics}
    dic = {"result": dic_musics, "error": 0, "msg": "OK"}
    return jsonify(dic), 200


@app.route("/download/uploadmusics", methods=['GET'])
def get_uploadmusics():
    userID = int(request.args.get("userID"))
    list_musics = db.get_upload_musics(userID)
    list_musics.reverse()
    #print (list_musics)
    dic_musics = {"count": len(list_musics), "musics": list_musics}
    dic = {"result": dic_musics, "error": 0, "msg": "OK"}
    return jsonify(dic), 200


@app.route("/download/messages", methods=['GET'])
def get_messages():
    userID = int(request.args.get("userID"))
    has_read = request.args.get("hasRead") == 'true'
    list_msgs, new_msg = db.get_message(userID, has_read)
    list_msgs.reverse()
    dic_msgs = {"count": len(list_msgs), "newMsgNum": new_msg, "messages": list_msgs}
    dic = {"result": dic_msgs, "error": 0, "msg": "OK"}
    return jsonify(dic), 200


if __name__ == '__main__':
    # db.upload_comment('comment1','music1','tth','2018-2-3-12-23-2','this is great!')
    reset_database()
    app.run(host='0.0.0.0', port=80)
