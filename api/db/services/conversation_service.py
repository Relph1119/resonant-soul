#!/usr/bin/env python
# encoding: utf-8
"""
@author: Datawhale
@file: conversation_service.py
@time: 2025/7/21 14:36
@project: resonant-soul
@desc: 
"""
from datetime import datetime, timedelta

from api.db.db_models import Conversation
from peewee import fn


class ConversationService:
    model = Conversation

    @classmethod
    def save_conversation(cls, user_input, ai_response, user_id):
        """保存对话记录"""
        cls.model.create(
            user_input=user_input,
            ai_response=ai_response,
            user_id=user_id
        )

    @classmethod
    def get_recent_conversations(cls, limit=10):
        """获取最近的对话记录"""
        query = (cls.model
                 .select()
                 .order_by(cls.model.timestamp.desc())
                 .limit(limit))
        return [(c.timestamp.strftime("%Y-%m-%d %H:%M:%S"), c.user_input, c.ai_response)
                for c in query]

    @classmethod
    def get_conversation_stats(cls, days=7, user_id=None):
        """获取对话统计信息"""
        if user_id:
            query = cls.model.select().where(cls.model.user_id == user_id)
        else:
            query = cls.model.select()

        start_date = datetime.now() - timedelta(days=days)

        # 基础统计
        basic_stats = (
            query.select(
                fn.COUNT(cls.model.id).alias('total_count'),
                fn.COUNT(fn.DISTINCT(fn.date(cls.model.timestamp))).alias('active_days')
            )
            .where(fn.date(cls.model.timestamp) >= start_date.date())
        ).first()

        # 每日对话次数统计
        daily_counts = dict(
            (row.date, row.count)
            for row in query.select(
                fn.date(cls.model.timestamp).alias('date'),
                fn.COUNT(cls.model.id).alias('count')
            )
            .where(fn.date(cls.model.timestamp) >= start_date.date())
            .group_by(fn.date(cls.model.timestamp))
            .order_by(fn.date(cls.model.timestamp))
        )

        return {
            'total_conversations': basic_stats.total_count or 0,
            'active_days': basic_stats.active_days or 0,
            'daily_counts': daily_counts
        }
