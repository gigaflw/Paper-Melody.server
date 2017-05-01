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

    def select(self, name, pw):
        cmd = "SELECT USERNAME, PASSWORD FROM USERS"
        map_value = self._db.execute(cmd)
        dic = dict(map_value)
        if name in dic.keys():
            result = dic.get(name, "")
            if result == pw:
                dic = {"name": name, "password": pw}
                return dic, 1
            else:
                return None, 0
        return None, -1

    def insert(self, name, pw):
        cmd = "SELECT USERNAME, PASSWORD FROM USERS"
        map_value = self._db.execute(cmd)
        dic = dict(map_value)
        if name in dic.keys():
            return 0
        cmd = "INSERT INTO USERS (USERNAME, PASSWORD) VALUES ('" + name + "', '" + pw + "')"
        self._db.execute(cmd)
        self._db.commit()
        return 1

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

