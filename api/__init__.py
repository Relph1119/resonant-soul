#!/usr/bin/env python
# encoding: utf-8
"""
@author: Datawhale
@file: __init__.py
@time: 2025/7/21 14:27
@project: resonant-soul
@desc: 
"""
import logging

from api import settings
from api.db.init_data import init_web_data
from api.utils import show_configs
from api.utils.log_utils import initRootLogger

initRootLogger("resonant-soul")

logging.info(r"""
______                                  _     _____             _ 
| ___ \                                | |   /  ___|           | |
| |_/ /___  ___  ___  _ __   __ _ _ __ | |_  \ `--.  ___  _   _| |
|    // _ \/ __|/ _ \| '_ \ / _` | '_ \| __|  `--. \/ _ \| | | | |
| |\ \  __/\__ \ (_) | | | | (_| | | | | |_  /\__/ / (_) | |_| | |
\_| \_\___||___/\___/|_| |_|\__,_|_| |_|\__| \____/ \___/ \__,_|_|
                                                                  
""")

logging.info(
    f'project base: {utils.file_utils.get_project_base_directory()}'
)

show_configs()
settings.init_settings()
init_web_data()
