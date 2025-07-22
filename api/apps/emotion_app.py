#!/usr/bin/env python
# encoding: utf-8
"""
@author: Datawhale
@file: emotion_app.py
@time: 2025/7/21 14:56
@project: resonant-soul
@desc: 
"""
import json
from datetime import datetime

import matplotlib.pyplot as plt

from api.db.services.emotion_service import EmotionService
from api.settings import EMOTION_RECORDS


def analyze_emotion(text):
    """分析用户情绪"""
    emotions = {
        '焦虑': ['焦虑', '紧张', '不安', '担心', '压力', '烦恼'],
        '抑郁': ['抑郁', '难过', '消沉', '伤心', '悲伤', '失落'],
        '愤怒': ['生气', '愤怒', '烦躁', '恼火', '不满'],
        '积极': ['开心', '快乐', '高兴', '兴奋', '满足']
    }

    detected_emotions = []
    for emotion, keywords in emotions.items():
        if any(keyword in text for keyword in keywords):
            detected_emotions.append(emotion)

    return detected_emotions if detected_emotions else ['平静']


def save_emotion_record(emotion, user_input, user_id):
    """保存情绪记录"""
    record = {
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'emotion': emotion,
    }
    EMOTION_RECORDS.append(record)
    record['user_input'] = user_input
    # 添加数据库存储
    EmotionService.save_emotion(emotion, user_input, user_id)


def generate_emotion_chart():
    """生成情绪趋势图表"""
    if not EMOTION_RECORDS:
        fig, ax = plt.subplots()
        ax.text(0.5, 0.5, 'No Emotion Data', ha='center', va='center')
        ax.set_axis_off()
        return fig

    emotion_en_map = {
        '焦虑': 'Anxiety',
        '抑郁': 'Depression',
        '愤怒': 'Anger',
        '积极': 'Positive',
        '平静': 'Calm'
    }

    emotion_counts = {}
    for record in EMOTION_RECORDS:
        for emotion in record['emotion']:
            if emotion in emotion_counts:
                emotion_counts[emotion] += 1
            else:
                emotion_counts[emotion] = 1

    fig, ax = plt.subplots()
    labels = list(emotion_counts.keys())
    sizes = list(emotion_counts.values())
    labels_en = [emotion_en_map.get(label, label) for label in labels]

    colors = {
        '焦虑': 'orange',
        '抑郁': 'blue',
        '愤怒': 'red',
        '积极': 'green',
        '平静': 'gray'
    }

    color_list = [colors.get(label, 'gray') for label in labels]
    ax.pie(sizes, labels=labels_en, autopct='%1.1f%%', colors=color_list)
    ax.set_title('Emotion Distribution')

    return fig


def get_all_emotion_records(user_id):
    """
    获取所有的情绪记录，并按照 date, content, emotions 的数组返回，数组里存放着每一个字典。
    """
    records = []
    # 获取所有情绪记录
    emotions = EmotionService.get_recent_all_emotions(user_id)
    for timestamp, emotion_json, user_input in emotions:
        emotions_list = json.loads(emotion_json)
        record = {
            "date": timestamp,
            "content": user_input,
            "emotions": emotions_list
        }
        records.append(record)
    return records
