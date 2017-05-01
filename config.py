# -*- coding: utf-8 -*-
# @Author:      HgS_1217_
# @Create Date: 2017/4/19

import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

DATABASE_DIR = os.path.join(BASE_DIR, 'database')
DATABASE_PATH = os.path.join(DATABASE_DIR, 'app.db')
DATABASE_SCHEMA_PATH = os.path.join(DATABASE_DIR, 'schema.sql')