# -*- coding: utf-8 -*-
# @Author:      HgS_1217_
# @Create Date: 2017/4/19

import sqlite3

from contextlib import closing
from config import DATABASE_PATH, DATABASE_SCHEMA_PATH


class DB(object):
    def init(self):
        if not hasattr(self, "_db"):
            setattr(self, "_db", self._connect_db())

    def user_select(self, name, pw):
        cmd = "SELECT USERNAME, PASSWORD FROM USERS"
        map_value = self._db.execute(cmd)
        dic = dict(map_value)
        if name in dic.keys():
            result = dic.get(name, "")
            if result == pw:
                dic = {"name": name, "password": pw}
                return dic, 0
            else:
                return None, 1
        return None, 2

    def user_insert(self, name, pw):
        cmd = "SELECT USERNAME, PASSWORD FROM USERS"
        map_value = self._db.execute(cmd)
        dic = dict(map_value)
        if name in dic.keys():
            return 1
        cmd = "INSERT INTO USERS (USERNAME, PASSWORD) VALUES ('" + name + "', '" + pw + "')"
        self._db.execute(cmd)
        self._db.commit()
        return 0

    def music_get_all(self):
        cmd = "SELECT * FROM ONLINEMUSICS"
        online_musics = list(self._db.execute(cmd))
        musics = []
        for ind, name, author, date, link, img_name, up_num, view_num in online_musics:
            dic = {"musicID": ind, "name": name, "author": author, "date": date, "imgName": img_name, "upvoteNum": up_num, "viewNum": view_num}
            musics.append(dic)
        return musics

    def music_update_num(self, musicID, up_num_differ, view_num_differ):
        cmd = "SELECT * FROM ONLINEMUSICS"
        num_list = list(self._db.execute(cmd))
        upvote = 0
        view = 0
        dic = {}
        for ind, name, author, date, link, img_name, up_num, view_num in num_list:
            if int(musicID) == ind:
                upvote = up_num + up_num_differ
                view = view_num + view_num_differ
                dic = {"musicID": ind, "name": name, "author": author, "date": date, "imgName": img_name, "upvoteNum": upvote, "viewNum": view}
                break
        #print (str(musicID)+"\t"+str(view)+"\t"+str(upvote))
        cmd = "UPDATE ONLINEMUSICS SET UPVOTENUM = '{0}', VIEWNUM = '{1}' WHERE IND = '{2}'".format(upvote, view, musicID)
        self._db.execute(cmd)
        return dic

    def music_insert(self, name, author, create_time, music_link, img_name):
        cmd = "SELECT NAME FROM ONLINEMUSICS"
        names = self._db.execute(cmd)
        if name in names:
            return 1
        cmd = "INSERT INTO ONLINEMUSICS (NAME, AUTHOR, CREATETIME, MUSICLINK, IMGNAME, UPVOTENUM, VIEWNUM) "+\
        "VALUES ('{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}')".format(name, author, create_time, music_link, img_name, 0, 0)
        self._db.execute(cmd)
        self._db.commit()
        print('Insert', name, author, create_time, music_link, img_name)
        return 0

    def get_comment(self,musicID):
        cmd = "SELECT MUSICID, AUTHOR, CREATETIME, COMMENT FROM COMMENTS";
        cmts = list(self._db.execute(cmd))
        comments = []
        for music_id, author, create_time, cmt in cmts:
            dic = {"musicID": music_id, "author": author, "createTime": create_time, "comment": cmt}
            comments.append(dic)
        print(comments)
        return comments
        #return ["this is good","I like it"], 2
    
    def get_all_comment(self):
        cmd = "SELECT * FROM COMMENTS"
        all_comments = list(self._db.execute(cmd))
        return str(all_comments)
        
    def upload_comment(self, commentID, musicID, user, time, comment):
        cmd = "SELECT COMMENTID FROM COMMENTS"
        names = self._db.execute(cmd)
        if commentID in names:
            return 1
        cmd ="INSERT INTO COMMENTS (COMMENTID, MUSICID, AUTHOR, CREATETIME, COMMENT) "+\
        "VALUES ('{0}', '{1}', '{2}', '{3}', '{4}')".format(commentID, musicID, user, time, comment)
        print(cmd)
        print("*************")
        self._db.execute(cmd)
        self._db.commit()
        return 0

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