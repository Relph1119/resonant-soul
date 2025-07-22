#!/usr/bin/env python
# encoding: utf-8
"""
@author: Datawhale
@file: statistics_app.py
@time: 2025/7/21 15:14
@project: resonant-soul
@desc: 
"""
from api.db.services.assessment_service import AssessmentService
from api.db.services.conversation_service import ConversationService
from api.db.services.emotion_service import EmotionService
import matplotlib.pyplot as plt


def get_stats_text(user_id):
    """获取统计文本"""
    assessment_stats = AssessmentService.get_assessment_stats(user_id=user_id)
    conversation_stats = ConversationService.get_conversation_stats(user_id=user_id)

    return f"""
### Overall Statistics
- Total Assessments: {assessment_stats['total_assessments']}
- Average Score: {assessment_stats['average_score']}
- Score Range: {assessment_stats['score_range']['min']} - {assessment_stats['score_range']['max']}

### Last 7 Days Activity
- Total Conversations: {conversation_stats['total_conversations']}
- Active Days: {conversation_stats['active_days']}
    """


def generate_stats_charts(user_id):
    """生成统计图表"""
    # 获取统计数据
    emotion_stats = EmotionService.get_emotion_stats(days=7, user_id=user_id)
    assessment_stats = AssessmentService.get_assessment_stats(user_id=user_id)
    conversation_stats = ConversationService.get_conversation_stats(days=7, user_id=user_id)

    # 创建图表
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(15, 5))

    # 中文情绪映射到英文
    emotion_en_map = {
        '焦虑': 'Anxiety',
        '抑郁': 'Depression',
        '愤怒': 'Anger',
        '积极': 'Positive',
        '平静': 'Calm'
    }

    result_en_map = {
        "焦虑水平在正常范围内": "Normal",
        "轻度焦虑": "Mild Anxiety",
        "中度焦虑": "Moderate Anxiety",
        "重度焦虑": "Severe Anxiety"
    }

    # 1. 情绪分布图
    if emotion_stats['total_distribution']:
        emotions = list(emotion_stats['total_distribution'].keys())
        counts = list(emotion_stats['total_distribution'].values())
        # 转换情绪标签为英文
        emotions_en = [emotion_en_map.get(e, e) for e in emotions]
        ax1.bar(emotions_en, counts)
        ax1.set_title('7-Day Emotion Distribution')
        ax1.tick_params(axis='x', rotation=45)
    else:
        ax1.text(0.5, 0.5, 'No Emotion Data', ha='center', va='center')
        ax1.set_axis_off()

    # 2. 评估结果分布
    if assessment_stats['result_distribution']:
        results = list(assessment_stats['result_distribution'].keys())
        counts = list(assessment_stats['result_distribution'].values())
        # 转换结果标签为英文
        results_en = [result_en_map.get(r, r) for r in results]
        ax2.pie(counts, labels=results_en, autopct='%1.1f%%')
        ax2.set_title('Assessment Results Distribution')
    else:
        ax2.text(0.5, 0.5, 'No Assessment Data', ha='center', va='center')
        ax2.set_axis_off()

    # 3. 对话活跃度
    if conversation_stats['daily_counts']:
        dates = list(conversation_stats['daily_counts'].keys())
        counts = list(conversation_stats['daily_counts'].values())
        ax3.plot(dates, counts, marker='o')
        ax3.set_title('Daily Conversation Count')
        ax3.set_xlabel('Date')
        ax3.set_ylabel('Count')
        ax3.tick_params(axis='x', rotation=45)
    else:
        ax3.text(0.5, 0.5, 'No Conversation Data', ha='center', va='center')
        ax3.set_axis_off()

    plt.tight_layout()
    return fig
