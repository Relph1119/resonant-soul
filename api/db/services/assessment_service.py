#!/usr/bin/env python
# encoding: utf-8
"""
@author: Datawhale
@file: assessment_service.py
@time: 2025/7/21 14:40
@project: resonant-soul
@desc: 
"""
import json

from peewee import fn

from api.db.db_models import Assessment


class AssessmentService:
    model = Assessment

    @classmethod
    def save_assessment(cls, user_id, scores, total_score, result):
        """保存评估记录"""
        cls.model.create(
            user_id=user_id,
            scores=json.dumps(scores),
            total_score=total_score,
            result=result
        )

    @classmethod
    def get_assessment_history(cls, user_id):
        """获取评估历史"""
        query = (cls.model
                 .select()
                 .where(cls.model.user_id == user_id)
                 .order_by(cls.model.timestamp.desc()))

        return [
            (
                a.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                json.loads(a.scores),
                a.total_score,
                a.result
            )
            for a in query
        ]

    @classmethod
    def get_assessment_stats(cls, user_id):
        """获取评估结果统计"""
        # 获取基本统计数据
        basic_stats = (
            cls.model
            .select(
                fn.COUNT(cls.model.id).alias('total_count'),
                fn.AVG(cls.model.total_score).alias('avg_score'),
                fn.MIN(cls.model.total_score).alias('min_score'),
                fn.MAX(cls.model.total_score).alias('max_score')
            )
            .where(cls.model.user_id == user_id)
            .first()
        )
        # 获取结果分布
        result_distribution = dict(
            (row.result, row.count)
            for row in cls.model.select(
                cls.model.result,
                fn.COUNT(cls.model.id).alias('count')
            ).group_by(cls.model.result)
        )
        return {
            'total_assessments': basic_stats.total_count,
            'average_score': round(basic_stats.avg_score or 0),
            'score_range': {
                'min': basic_stats.min_score or 0,
                'max': basic_stats.max_score or 0
            },
            'result_distribution': result_distribution
        }
