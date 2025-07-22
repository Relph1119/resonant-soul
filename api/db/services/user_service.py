#!/usr/bin/env python
# encoding: utf-8
"""
@author: Datawhale
@file: user_service.py
@time: 2025/7/22 17:00
@project: resonant-soul
@desc: 用户服务
"""
import hashlib

from api.db.db_models import User


class UserService:
    @classmethod
    def register(cls, username, name_nick, password):
        if cls.get_by_username(username):
            return None

        try:
            hashed_pwd = hashlib.sha256(password.encode()).hexdigest()
            return User.create(
                username=username,
                name_nick=name_nick,
                password=hashed_pwd
            )
        except Exception as e:
            print(f"数据库错误: {str(e)}")
            return None

    @classmethod
    def get_by_username(cls, username):
        try:
            return User.get(User.username == username)
        except User.DoesNotExist:
            return None

    @classmethod
    def verify_password(cls, user, password):
        """用户登录"""
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        return user if user.password == hashed_password else None
