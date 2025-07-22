#!/usr/bin/env python
# encoding: utf-8
"""
@author: Datawhale
@file: emotion_service.py
@time: 2025/7/21 14:33
@project: resonant-soul
@desc: 
"""
import json
from datetime import datetime, timedelta

from api.db.db_models import Emotion


class EmotionService:
    model = Emotion

    @classmethod
    def save_emotion(cls, emotions, user_input, user_id):
        """保存情绪记录"""
        cls.model.create(
            emotions=json.dumps(emotions),
            timestamp=datetime.now(),
            user_input=user_input,
            user_id=user_id
        )

    @classmethod
    def get_recent_emotions(cls, limit=100):
        """获取最近的情绪记录"""
        query = (cls.model
                 .select()
                 .order_by(cls.model.timestamp.desc())
                 .limit(limit))
        return [(e.timestamp.strftime("%Y-%m-%d %H:%M:%S"), e.emotions)
                for e in query]

    @classmethod
    def get_recent_all_emotions(cls, user_id):
        """获取最近的情绪记录"""
        query = (cls.model
                 .select()
                 .where(cls.model.user_id == user_id)
                 .order_by(cls.model.timestamp.desc()))
        return [(e.timestamp.strftime("%Y-%m-%d %H:%M:%S"), e.emotions, e.user_input)
                for e in query]

    # 统计方法改为使用ORM表达式
    @classmethod
    def get_emotion_stats(cls, days=7, user_id=None):
        """获取情绪统计"""
        start_date = datetime.now() - timedelta(days=days)

        # 查询指定时间范围内的记录
        query = (cls.model
                 .select()
                 .where(cls.model.timestamp >= start_date, cls.model.user_id == user_id)
                 .order_by(cls.model.timestamp))

        # 统计每种情绪的出现次数和时间分布
        emotion_counts = {}
        daily_emotions = {}

        for record in query:
            emotions = json.loads(record.emotions)
            date_str = record.timestamp.strftime("%Y-%m-%d")

            # 统计总体情绪分布
            for emotion in emotions:
                emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1

            # 统计每日情绪分布
            if date_str not in daily_emotions:
                daily_emotions[date_str] = {}
            for emotion in emotions:
                daily_emotions[date_str][emotion] = daily_emotions[date_str].get(emotion, 0) + 1

        return {
            'total_distribution': emotion_counts,
            'daily_distribution': daily_emotions
        }
