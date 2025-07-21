#!/usr/bin/env python
# encoding: utf-8
"""
@author: Datawhale
@file: __init__.py
@time: 2025/7/21 14:27
@project: resonant-soul
@desc: 
"""
from api import settings
from api.utils import show_configs

show_configs()
settings.init_settings()
