#!/usr/bin/env python
# encoding: utf-8
"""
@author: Datawhale
@file: init_data.py
@time: 2025/7/23 9:52
@project: resonant-soul
@desc: 
"""
from api import settings
from api.apps.admin_app import create_admin_user
from loguru import logger


def init_web_data():
    # 初始化管理员账号
    username = settings.ADMIN_USER['username']
    password = settings.ADMIN_USER['password']
    name_nick = settings.ADMIN_USER['name_nick']
    create_admin_user(username, name_nick, password)
    logger.info(f"管理员账号初始化完成")
