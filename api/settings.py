#!/usr/bin/env python
# encoding: utf-8
"""
@author: Datawhale
@file: settings.py
@time: 2025/7/21 14:58
@project: resonant-soul
@desc: 
"""

from camel.models import ModelFactory
from camel.types import ModelPlatformType
from dotenv import load_dotenv

from api.db.db_models import DBManager
from api.utils import get_base_config

EMOTION_RECORDS = []
DIARY_ENTRIES = []
databaseConn = None
CHAT_MDL = None


def init_settings():
    global EMOTION_RECORDS, DIARY_ENTRIES, databaseConn, CHAT_MDL
    # 存储情绪记录和日记
    databaseConn = DBManager()

    # 加载环境变量
    load_dotenv(dotenv_path='.env')

    LLM = get_base_config("llm")

    # 初始化模型
    CHAT_MDL = ModelFactory.create(
        model_platform=ModelPlatformType.OPENAI_COMPATIBLE_MODEL,
        model_type=LLM['model_type'],
        url=LLM['model_url'],
        api_key=LLM['api_key']
    )

    from api.apps.emotion_app import get_all_emotion_records
    # 加载情绪记录
    DIARY_ENTRIES = get_all_emotion_records()
