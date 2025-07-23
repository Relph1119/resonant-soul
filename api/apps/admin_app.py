#!/usr/bin/env python
# encoding: utf-8
"""
@author: Datawhale
@file: admin_app.py
@time: 2025/7/22 17:12
@project: resonant-soul
@desc:
"""
from loguru import logger

from api.db.services.user_service import UserService


def get_all_users():
    """获取所有用户列表"""
    try:
        users = UserService.get_all_users()
        user_list = []
        for user in users:
            if user.status:
                status_msg = "正常"
            else:
                status_msg = "已禁用"

            user_dict = {
                'id': user.id,
                'username': user.username,
                'name': user.name_nick,
                'status': status_msg,
                'created_at': user.created_at.strftime('%Y-%m-%d %H:%M:%S') if user.created_at else ''
            }
            user_list.append(user_dict)
        return user_list
    except Exception as e:
        logger.error(f"获取用户列表失败: {str(e)}")
        return []


def update_user_status(user_id, status):
    """更新用户状态"""
    try:
        return UserService.update_status(user_id, status)
    except Exception as e:
        logger.error(f"更新用户状态失败: {str(e)}")
        return False


def delete_user(user_id):
    """删除用户"""
    try:
        return UserService.delete_user(user_id)
    except Exception as e:
        logger.error(f"删除用户失败: {str(e)}")
        return False


def create_admin_user(username, name_nick, password):
    """创建管理员账号"""
    try:
        user = UserService.register_admin(username, name_nick, password)
        if user:
            return True, "管理员账号创建成功"
        return False, "创建失败：用户名已存在"
    except Exception as e:
        logger.error(f"创建管理员账号失败: {str(e)}")
        return False, f"创建失败: {str(e)}"
