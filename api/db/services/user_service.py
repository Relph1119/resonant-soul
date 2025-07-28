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
from datetime import datetime

from api.db.db_models import User


class UserService:
    @staticmethod
    def get_by_username(username):
        try:
            return User.get(User.username == username)
        except User.DoesNotExist:
            return None

    @staticmethod
    def verify_password(user, password):
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        return user.password == password_hash

    @staticmethod
    def check_user_status(user):
        """检查用户状态"""
        message = "正常"
        status_ok = True
        if not user.status:
            message = "账号已被禁用，请联系管理员"
            status_ok = False
        return status_ok, message

    @staticmethod
    def register(username, name_nick, password, is_admin=False):
        if UserService.get_by_username(username):
            return None

        # 密码哈希处理
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        current_time = datetime.now()

        # 保存用户数据
        user = User.create(
            username=username,
            password=password_hash,
            name_nick=name_nick,
            is_admin=is_admin,
            status=True,
            created_at=current_time,
            updated_at=current_time
        )
        return user

    @staticmethod
    def register_admin(username, name_nick, password):
        return UserService.register(username, name_nick, password, is_admin=True)

    @staticmethod
    def get_all_users():
        return User.select()

    @staticmethod
    def update_status(user_id, status):
        try:
            user = User.get_by_id(user_id)
            # 防止禁用管理员账号
            if user.is_admin and not status:
                return False
            user.status = status
            user.updated_at = datetime.now()
            user.save()
            return True
        except User.DoesNotExist:
            return False

    @staticmethod
    def delete_user(user_id):
        try:
            user = User.get_by_id(user_id)
            # 防止删除管理员账号
            if user.is_admin:
                return False
            user.delete_instance()
            return True
        except User.DoesNotExist:
            return False

    @classmethod
    def update_password(cls, user_id, new_password):
        user = User.get_by_id(user_id)
        password_hash = hashlib.sha256(new_password.encode()).hexdigest()
        user.password = password_hash
        user.updated_at = datetime.now()
        user.save()
        return True

    @classmethod
    def get_by_id(cls, user_id):
        try:
            return User.get_by_id(user_id)
        except User.DoesNotExist:
            return None
