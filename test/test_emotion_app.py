#!/usr/bin/env python
# encoding: utf-8
"""
@author: HuRuiFeng
@file: emotion_app_test.py
@time: 2025/7/21 22:19
@project: resonant-soul
@desc: 
"""

import pytest

from api.apps.emotion_app import analyze_emotion


# 定义测试夹具，用于重置 EMOTION_RECORDS
@pytest.fixture
def reset_emotion_records():
    global EMOTION_RECORDS
    EMOTION_RECORDS = []
    yield
    EMOTION_RECORDS = []


# 使用参数化测试单个情绪识别
@pytest.mark.parametrize("text, expected_emotion", [
    ("我今天很开心", ["积极"]),
    ("我感到很焦虑", ["焦虑"]),
    ("他非常愤怒", ["愤怒"]),
    ("她有点抑郁", ["抑郁"]),
])
def test_analyze_emotion_single_emotion(text, expected_emotion):
    """测试单个情绪识别"""
    assert analyze_emotion(text) == expected_emotion


# 使用参数化测试多个情绪同时识别
@pytest.mark.parametrize("text, expected_emotions", [
    ("我又开心又紧张", ["积极", "焦虑"]),
    ("既生气又难过", ["愤怒", "抑郁"]),
    ("兴奋但有点担心", ["积极", "焦虑"]),
])
def test_analyze_emotion_multiple_emotions(text, expected_emotions):
    """测试多个情绪同时识别"""
    assert sorted(analyze_emotion(text)) == sorted(expected_emotions)


# 使用参数化测试没有检测到情绪时返回平静
@pytest.mark.parametrize("text", [
    "今天天气不错",
    "这是一条普通消息",
    "",
])
def test_analyze_emotion_no_emotion(text):
    """测试没有检测到情绪时返回平静"""
    assert analyze_emotion(text) == ["平静"]


# 使用参数化测试部分匹配
@pytest.mark.parametrize("text, expected_emotion", [
    ("压力山大", ["焦虑"]),
    ("满足感", ["积极"]),
    ("失落感", ["抑郁"]),
])
def test_analyze_emotion_partial_match(text, expected_emotion):
    """测试部分匹配"""
    assert analyze_emotion(text) == expected_emotion


# 使用参数化测试边界情况
@pytest.mark.parametrize("text, expected_emotion", [
    ("开心开心开心", ["积极"]),  # 重复词
    ("123开心456", ["积极"]),  # 包含数字
])
def test_analyze_emotion_edge_cases(text, expected_emotion):
    """测试边界情况"""
    assert analyze_emotion(text) == expected_emotion
