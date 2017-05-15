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
        for ind, name, author, date, link in online_musics:
            dic = {"name": name, "author": author, "date": date, "link": link}
            musics.append(dic)
        return musics

    def music_insert(self, name, author, create_time, link):
        cmd = "SELECT NAME FROM ONLINEMUSICS"
        names = self._db.execute(cmd)
        if name in names:
            return 1
        cmd = "INSERT INTO ONLINEMUSICS (NAME, AUTHOR, CREATETIME, MUSICLINK) VALUES ('" + name + "', '" + author + "', '" + create_time + "', '" + link + "')"
        self._db.execute(cmd)
        self._db.commit()
        print('INSERT',name, author, create_time, link)
        return 0

    def get_comment(self,musicID):
        cmd = "SELECT MUSICID, AUTHOR, CREATETIME FROM COMMENTS";
        dic=str(self._db.execute(cmd));
        print(dic)
        return ["this is good","I like it"], 2
    
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
        "VALUES ('{0}', '{1}', '{2}', '{3}', '{4}')".format(commentID, musicID, user, time, comment);
        print(cmd)
        print("*************")
        self._db.execute(cmd)
        self._db.commit()
        return 0

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