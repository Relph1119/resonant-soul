#!/usr/bin/env python
# encoding: utf-8
"""
@author: Datawhale
@file: conversation_app.py
@time: 2025/7/21 15:20
@project: resonant-soul
@desc: 
"""
from camel.societies import RolePlaying

from api.apps.emotion_app import analyze_emotion, save_emotion_record, save_diary_entry, generate_emotion_chart
from api.db.services.conversation_service import ConversationService
from api.settings import CHAT_MDL


def process_user_input(user_input, history:list):
    """处理用户输入并返回响应"""
    emotions = analyze_emotion(user_input)
    save_emotion_record(emotions, user_input)
    save_diary_entry(user_input, emotions)
    print(f"检测到的情绪: {emotions}")

    task_prompt = "作为心灵伙伴AI心理健康助手，直接以第一人称与大学生进行心理健康对话"
    role_play_session = RolePlaying(
        assistant_role_name="心灵伙伴AI心理健康助手",
        assistant_agent_kwargs=dict(model=CHAT_MDL),
        user_role_name="在校大学生",
        user_agent_kwargs=dict(model=CHAT_MDL),
        task_prompt=task_prompt,
        with_task_specify=True,
        task_specify_agent_kwargs=dict(model=CHAT_MDL),
        output_language='中文'
    )

    input_msg = role_play_session.init_chat()
    input_msg.content = f"""
    Instruction: 请以心灵伙伴AI心理健康助手的第一人称身份回应。根据检测到的情绪 {emotions}，提供针对性的支持和建议。
    Input: {user_input}
    """

    assistant_response, _ = role_play_session.step(input_msg)
    response_content = assistant_response.msg.content

    if "Solution:" in response_content:
        response_content = response_content.split("Solution:")[1].split("Next request.")[0].strip()

    third_person_phrases = [
        "作为心理咨询师，",
        "作为一名心理咨询师，",
        "作为您的心理健康助手，",
        "作为一个AI助手，",
        "作为心灵伙伴，"
    ]

    for phrase in third_person_phrases:
        response_content = response_content.replace(phrase, "")

    # 保存对话记录到数据库
    ConversationService.save_conversation(user_input, response_content)

    new_history = history + [
        {"role": "user", "content": user_input},
        {"role": "assistant", "content": response_content}
    ]

    return new_history, generate_emotion_chart()
