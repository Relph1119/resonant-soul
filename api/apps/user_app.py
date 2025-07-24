#!/usr/bin/env python
# encoding: utf-8
"""
@author: Datawhale
@file: user_app.py
@time: 2025/7/22 17:12
@project: resonant-soul
@desc: 
"""
from api.db.services.user_service import UserService


def user_register(username, name_nick, password):
    """用户注册"""
    try:
        user = UserService.register(username, name_nick, password)
        if user:
            return {
                "id": user.id,
                "name": user.name_nick,
                "username": user.username,
                "is_admin": user.is_admin
            }
        return None
    except Exception as e:
        print(f"注册错误: {str(e)}")
        return None


def user_login(username, password):
    """用户登录"""
    user = UserService.get_by_username(username)
    if not user:
        return {"error": "用户不存在"}

    # 检查用户状态
    status_ok, message = UserService.check_user_status(user)
    if not status_ok:
        return {"error": message}

    if not UserService.verify_password(user, password):
        return {"error": "密码错误"}

    return {
        "id": user.id,
        "name": user.name_nick,
        "username": user.username,
        "is_admin": user.is_admin
    }


def get_user_info_by_username(username):
    """根据用户名获取用户信息"""
    user = UserService.get_by_username(username)
    if user:
        return {
            "id": user.id,
            "name": user.name_nick,
            "username": user.username,
            "is_admin": user.is_admin
        }
    return None


def get_user_info_by_id(user_id):
    """根据用户ID获取用户信息"""
    user = UserService.get_by_id(user_id)
    if user:
        return {
            "id": user.id,
            "name": user.name_nick,
            "username": user.username,
            "is_admin": user.is_admin,
            "created_at": user.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        }
    return None


def update_password(user_id,new_pwd):
    """更新用户密码"""
    return UserService.update_password(user_id, new_pwd)
