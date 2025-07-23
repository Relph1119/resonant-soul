#!/usr/bin/env python
# encoding: utf-8
"""
@author: Datawhale
@file: models.py
@time: 2025/7/21 14:25
@project: resonant-soul
@desc: 
"""
from datetime import datetime

from peewee import DateTimeField, TextField, IntegerField, Proxy, ForeignKeyField, BooleanField
from peewee import Model
from peewee import SqliteDatabase

db_proxy = Proxy()


class BaseModel(Model):
    id = IntegerField(primary_key=True)

    class Meta:
        database = db_proxy  # 延迟初始化


class User(BaseModel):
    username = TextField(unique=True)  # 用户名，唯一
    name_nick = TextField()  # 昵称
    password = TextField()  # 密码
    status = TextField(default='正常')  # 用户状态
    is_admin = BooleanField(default=False)  # 是否是管理员
    created_at = DateTimeField(default=datetime.now)  # 创建时间
    updated_at = DateTimeField(default=datetime.now)  # 更新时间

    class Meta:
        table_name = 'users'


# 情绪记录模型
class Emotion(BaseModel):
    timestamp = DateTimeField(default=datetime.now)
    emotions = TextField()  # 存储JSON字符串
    user_input = TextField()
    user_id = ForeignKeyField(User, backref='emotions')


# 对话记录模型
class Conversation(BaseModel):
    timestamp = DateTimeField(default=datetime.now)
    user_input = TextField()
    ai_response = TextField()
    user_id = ForeignKeyField(User, backref='conversations')


# 评估记录模型
class Assessment(BaseModel):
    timestamp = DateTimeField(default=datetime.now)
    scores = TextField()  # 存储JSON字符串
    total_score = IntegerField()
    result = TextField()
    user_id = ForeignKeyField(User, backref='assessments')


class DBManager:
    def __init__(self, db_path='mindmate.db'):
        # 初始化数据库连接
        self.db = SqliteDatabase(db_path)
        db_proxy.initialize(self.db)
        # 需要确保所有模型类都继承自BaseModel
        self.models = [User, Emotion, Conversation, Assessment]  # 调整顺序，确保User先创建

        # 自动创建表
        with self.db:
            self._create_tables()
            print("数据库表创建成功")

    def _create_tables(self):
        """创建数据库表"""
        self.db.create_tables(self.models, safe=True)


# 创建数据库实例
db_manager = DBManager()
