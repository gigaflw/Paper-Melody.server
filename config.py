# -*- coding: utf-8 -*-
# @Author:      HgS_1217_
# @Create Date: 2017/4/19

import os, platform

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

DATABASE_DIR = os.path.join(BASE_DIR, 'database')
DATABASE_PATH = os.path.join(DATABASE_DIR, 'app.db')
DATABASE_SCHEMA_PATH = os.path.join(DATABASE_DIR, 'schema.sql')

UPLOAD_FOLDER = ""
UPLOAD_IMAGE_FOLDER = ""

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
ALLOWED_FILE_EXTENSIONS = set(['m4a', 'mp3', 'mid'])

if platform.system() == "Windows":  # 本地测试使用的文件夹地址
    UPLOAD_FOLDER = 'D:/Computer Science/Github/Paper-Melody.server/uploads/file' 
    UPLOAD_IMAGE_FOLDER = 'D:/Computer Science/Github/Paper-Melody.server/uploads/image' 
else:
    UPLOAD_IMAGE_FOLDER = '/Paper-Melody.server/uploads/image'  #服务器使用的文件夹地址
    UPLOAD_FOLDER = '/Paper-Melody.server/uploads/file'  #服务器使用的文件夹地址
