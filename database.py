# -*- coding: utf-8 -*-
# @Author:      HgS_1217_
# @Create Date: 2017/4/19

import sqlite3, time

from contextlib import closing
from config import DATABASE_PATH, DATABASE_SCHEMA_PATH, SYSTEM_BROADCAST


class DB(object):
    def init(self):
        if not hasattr(self, "_db"):
            setattr(self, "_db", self._connect_db())

    def insert_message(self, user, userID, reply_userID, time, msg):
        cmd ="INSERT INTO MESSAGES (AUTHOR, AUTHORID, REPLYUSERID, CREATETIME, NEWS, MESSAGE)" +\
                "VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}')".format(user, userID, reply_userID, time, 1, msg)
        self._db.execute(cmd)
        self._db.commit()

    def get_message(self, userID, has_read):
        cmd = "SELECT * FROM MESSAGES"
        msg_list = list(self._db.execute(cmd))
        messages = []
        new_msg = 0
        for ind, author, authorID, reply_userID, time, news, msg in msg_list:
            if userID == reply_userID:
                dic = {"author": author, "createTime": time, "message": msg, "isNew": news == 1}
                messages.append(dic)
                if news == 1:
                    new_msg += 1
                    if has_read:
                        cmd = "UPDATE MESSAGES SET NEWS = '{0}' WHERE IND = '{1}'".format(0, ind)
                        self._db.execute(cmd)
                        self._db.commit()
        return messages, new_msg

    def system_broadcast(self, time, msg):
        cmd = "SELECT IND FROM USERS"
        list_value = self._db.execute(cmd)
        for ind in list_value:
            insert_message(SYSTEM_BROADCAST, 0, ind, time, msg)


    def user_select(self, nm, pw):
        cmd = "SELECT * FROM USERS"
        list_value = self._db.execute(cmd)
        for ind, name, nickname, avatar_name, password in list_value:
            if name == nm:
                if password == pw:
                    dic = {"userID": ind, "name": name, "password": password, "nickname": nickname, "avatarName": avatar_name}
                    return dic, 0
                else:
                    return None, 1
        return None, 2

    def user_insert(self, nm, pw):
        cmd = "SELECT USERNAME, PASSWORD FROM USERS"
        map_value = self._db.execute(cmd)
        dic = dict(map_value)
        if nm in dic.keys():
            return None, 1
        cmd = "INSERT INTO USERS (USERNAME, PASSWORD, NICKNAME, AVATARNAME) VALUES ('{0}', '{1}', '{2}', '{3}')".format(nm, pw, nm, "")
        self._db.execute(cmd)
        self._db.commit()
        cmd = "SELECT * FROM USERS"
        list_value = self._db.execute(cmd)
        for ind, name, nickname, avatar_name, password in list_value:
            if name == nm:
                dic = {"userID": ind, "name": name, "password": password, "nickname": nickname, "avatarName": avatar_name}
                current_time = time.localtime()
                str_time =  time.strftime("%Y-%m-%d %H:%M:%S", current_time)
                self.insert_message(SYSTEM_BROADCAST, 0, ind, str_time, "欢迎来到Paper Melody!!")
                return dic, 0
        return None, 1

    def user_update_avatar(self, userID, avatar_name):
        cmd = "SELECT IND, AVATARNAME FROM USERS"
        map_value = self._db.execute(cmd)
        dic = dict(map_value)
        old_name = ""
        if userID in dic.keys():
            old_name = dic[userID]
        cmd = "UPDATE USERS SET AVATARNAME = '{0}' WHERE IND = '{1}'".format(avatar_name, userID)
        self._db.execute(cmd)
        self._db.commit()
        cmd = "SELECT * FROM USERS"
        list_value = self._db.execute(cmd)
        for ind, name, nickname, avatar_name, password in list_value:
            if ind == userID:
                dic = {"userID": ind, "name": name, "password": password, "nickname": nickname, "avatarName": avatar_name}
                return dic, old_name
        return None, old_name

    def user_update_nickname(self, userID, nickname):
        cmd = "UPDATE USERS SET NICKNAME = '{0}' WHERE IND = '{1}'".format(nickname, userID)
        self._db.execute(cmd)
        self._db.commit()
        cmd = "SELECT * FROM USERS"
        list_value = self._db.execute(cmd)
        for ind, name, nickname, avatar_name, password in list_value:
            if ind == userID:
                dic = {"userID": ind, "name": name, "password": password, "nickname": nickname, "avatarName": avatar_name}
                return dic, 0
        return None, 1

    def user_update_password(self, userID, old_pw, new_pw):
        cmd = "SELECT IND, PASSWORD FROM USERS"
        map_value = self._db.execute(cmd)
        dic = dict(map_value)
        if userID in dic.keys():
            if old_pw == dic.get(userID):
                cmd = "UPDATE USERS SET PASSWORD = '{0}' WHERE IND = '{1}'".format(new_pw, userID)
                self._db.execute(cmd)
                self._db.commit()
                cmd = "SELECT * FROM USERS"
                list_value = self._db.execute(cmd)
                for ind, name, nickname, avatar_name, password in list_value:
                    if ind == userID:
                        dic = {"userID": ind, "name": name, "password": password, "nickname": nickname, "avatarName": avatar_name}
                        return dic, 0
        return None, 1

    def music_get_all(self):
        cmd = "SELECT * FROM ONLINEMUSICS"
        online_musics = list(self._db.execute(cmd))
        musics = []
        for ind, name, author, authorID, date, music_name, img_name, up_num, view_num in online_musics:
            dic = {"musicID": ind, "name": name, "author": author, "authorID": authorID, "date": date,\
                 "musicName": music_name, "imgName": img_name, "upvoteNum": up_num, "viewNum": view_num}
            musics.append(dic)
        return musics

    def music_update_num(self, musicID, up_num_differ, view_num_differ):
        cmd = "SELECT * FROM ONLINEMUSICS"
        num_list = list(self._db.execute(cmd))
        upvote = 0
        view = 0
        dic = {}
        for ind, name, author, authorID, date, music_name, img_name, up_num, view_num in num_list:
            if int(musicID) == ind:
                upvote = up_num + up_num_differ
                view = view_num + view_num_differ
                dic = {"musicID": ind, "name": name, "author": author, "authorID": authorID, "date": date,\
                     "musicName": music_name, "imgName": img_name, "upvoteNum": up_num, "viewNum": view_num}
                break
        #print (str(musicID)+"\t"+str(view)+"\t"+str(upvote))
        cmd = "UPDATE ONLINEMUSICS SET UPVOTENUM = '{0}', VIEWNUM = '{1}' WHERE IND = '{2}'".format(upvote, view, musicID)
        self._db.execute(cmd)
        self._db.commit()
        return dic

    def music_insert(self, name, author, authorID, create_time, music_name, img_name):
        cmd = "SELECT NAME FROM ONLINEMUSICS"
        names = self._db.execute(cmd)
        if name in names:
            return 1
        cmd = "INSERT INTO ONLINEMUSICS (NAME, AUTHOR, AUTHORID, CREATETIME, MUSICNAME, IMGNAME, UPVOTENUM, VIEWNUM) "+\
        "VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', '{7}')".format(name, author, authorID, create_time, music_name, img_name, 0, 0)
        self._db.execute(cmd)
        self._db.commit()
        #print('Insert', name, author, authorID, create_time, music_name, img_name)
        return 0

    def get_comment(self, musicID):
        cmd = "SELECT * FROM COMMENTS";
        cmts = list(self._db.execute(cmd))
        comments = []
        for ind, music_id, author, author_id, create_time, cmt in cmts:
            if (musicID == music_id):
                dic = {"musicID": music_id, "author": author, "authorID": author_id, "createTime": create_time, "comment": cmt}
                comments.append(dic)
        #print(comments)
        return comments
        #return ["this is good","I like it"], 2
    
    def get_all_comment(self):
        cmd = "SELECT * FROM COMMENTS"
        all_comments = list(self._db.execute(cmd))
        return str(all_comments)
        
    def upload_comment(self, musicID, user, userID, time, comment):
        cmd ="INSERT INTO COMMENTS (MUSICID, AUTHOR, AUTHORID, CREATETIME, COMMENT)" +\
                "VALUES ('{0}', '{1}', '{2}', '{3}', '{4}')".format(musicID, user, userID, time, comment)
        #print(cmd)
        #print("*************")
        self._db.execute(cmd)
        self._db.commit()

    def get_upload_musics(self, userID):
        cmd = "SELECT * FROM ONLINEMUSICS"
        num_list = list(self._db.execute(cmd))
        musics = []
        for ind, name, author, authorID, date, music_name, img_name, up_num, view_num in num_list:
            if authorID == userID:
                dic = {"musicID": ind, "name": name, "author": author, "authorID": authorID, "date": date,\
                     "musicName": music_name, "imgName": img_name, "upvoteNum": up_num, "viewNum": view_num}
                musics.append(dic)
        return musics

    def judge_favorites(self, userID, musicID):
        cmd = "SELECT AUTHORID, MUSICID FROM FAVORITES"
        map_value = list(self._db.execute(cmd))
        status = False
        for author, music in map_value:
            if author == userID and music == musicID:
                status = True
                break
        cmd = "SELECT AUTHORID, IND, UPVOTENUM, VIEWNUM FROM ONLINEMUSICS"
        num_list = list(self._db.execute(cmd))
        for authorID, music, upvote, view in num_list:
            if music == musicID:
                dic = {"upvoteNum": upvote, "viewNum": view}
                return dic, status
        return None, status

    def add_favorites(self, userID, musicID):
        cmd ="INSERT INTO FAVORITES (AUTHORID, MUSICID) VALUES ('{0}', '{1}')".format(userID, musicID)
        self._db.execute(cmd)
        self._db.commit()

    def get_favorites(self, userID):
        cmd = "SELECT AUTHORID, MUSICID FROM FAVORITES"
        map_value = list(self._db.execute(cmd))
        musicIDs = []
        for author, music in map_value:
            if author == userID:
                musicIDs.append(music)

        cmd = "SELECT * FROM ONLINEMUSICS"
        num_list = list(self._db.execute(cmd))
        musics = []
        for ind, name, author, authorID, date, music_name, img_name, up_num, view_num in num_list:
            if ind in musicIDs:
                dic = {"musicID": ind, "name": name, "author": author, "authorID": authorID, "date": date,\
                     "musicName": music_name, "imgName": img_name, "upvoteNum": up_num, "viewNum": view_num}
                musics.append(dic)
        return musics

    def delete_favorites(self, userID, musicID):
        cmd = "DELETE FROM FAVORITES WHERE AUTHORID = '{0}' AND MUSICID = '{1}'".format(userID, musicID)
        self._db.execute(cmd)
        self._db.commit()

    def get_next_musicid(self):
        cmd = "SELECT IND, NAME FROM ONLINEMUSICS"
        inds = list(self._db.execute(cmd))
        ins = []
        for ind, name in inds:
            ins.append(ind)
        return max(ins) + 1

    @classmethod
    def reset_db(cls):
        with closing(cls._connect_db()) as db:
            with open(DATABASE_SCHEMA_PATH, 'r') as f:
                db.cursor().executescript(f.read())
            db.commit()

    @staticmethod
    def _connect_db():
        return sqlite3.connect(DATABASE_PATH, check_same_thread=False)

    def connect(self):
        self._db = self._connect_db()

    def close(self):
        self._db.close()

db = DB()


if __name__ == '__main__':
    db.init()