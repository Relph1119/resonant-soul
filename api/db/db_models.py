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

from peewee import DateTimeField, TextField, IntegerField, Proxy, ForeignKeyField
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
        self.models = [Emotion, Conversation, Assessment, User]

        # 自动创建表
        with self.db:
            self._create_tables()

    def _create_tables(self):
        """创建数据库表"""
        self.db.create_tables(self.models, safe=True)
