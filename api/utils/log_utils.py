#!/usr/bin/env python
# encoding: utf-8
"""
@author: Datawhale
@file: log_utils.py
@time: 2025/7/23 9:42
@project: resonant-soul
@desc: 
"""
import logging
import os
import sys

from loguru import logger

from api.utils.file_utils import get_project_base_directory

LOG_FORMAT = ("[%s][<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green>][<level>{level}</level>][{thread.name}][<cyan>{"
              "file}</cyan> <cyan>{module}</cyan>.<cyan>{function}</cyan>:<cyan>{line}</cyan>]-<level>{"
              "message}</level>")


def initRootLogger(logfile_basename: str,
                   log_format: str = LOG_FORMAT):
    log_format = log_format % logfile_basename
    log_filename = logfile_basename + ".{time:YYYY-MM-DD}.log"

    log_path = os.path.abspath(os.path.join(get_project_base_directory(), "logs", log_filename))
    os.makedirs(os.path.dirname(log_path), exist_ok=True)

    # Remove default handler
    logger.remove()

    # Add file handler with rotation
    logger.add(
        log_path,
        rotation="10 MB",
        retention="5 days",
        format=log_format,
        level="INFO",
        enqueue=False
    )

    # Add console handler
    logger.add(
        sys.stderr,
        format=log_format,
        level="INFO",
        enqueue=False
    )

    # Configure log levels from environment variable
    LOG_LEVELS = os.environ.get("LOG_LEVELS", "")
    pkg_levels = {}
    for pkg_name_level in LOG_LEVELS.split(","):
        terms = pkg_name_level.split("=")
        if len(terms) != 2:
            continue
        pkg_name, pkg_level = terms[0], terms[1]
        pkg_name = pkg_name.strip()
        pkg_level = pkg_level.strip().upper()
        pkg_levels[pkg_name] = pkg_level

    # Set default levels for specific packages
    for pkg_name in ['peewee', 'pdfminer']:
        if pkg_name not in pkg_levels:
            pkg_levels[pkg_name] = "WARNING"
    if 'root' not in pkg_levels:
        pkg_levels['root'] = "INFO"

    # Configure log levels for packages
    for pkg_name, pkg_level in pkg_levels.items():
        if pkg_name == 'root':
            logger.remove()
            logger.add(sys.stderr, level=pkg_level)
        else:
            # Convert string level to int
            level_mapping = {
                'DEBUG': 10,
                'INFO': 20,
                'WARNING': 30,
                'ERROR': 40,
                'CRITICAL': 50
            }
            level_num = level_mapping.get(pkg_level, 20)  # default to INFO if level not found

            # Create a new level for the package if it doesn't exist
            logger.level(pkg_name, no=level_num)

            # Add handler for this package
            logger.add(
                lambda msg: logger.log(pkg_level, f"[{pkg_name}] {msg}"),
                format="{message}",
                level=pkg_level,
                filter=lambda record: record["extra"].get("name", "").startswith(pkg_name)
            )

        class InterceptHandler(logging.Handler):
            def __init__(self):
                super().__init__()
                self.formatter = None

            def emit(self, record):
                try:
                    level = logger.level(record.levelname).name
                except ValueError:
                    level = record.levelno

                frame, depth = logging.currentframe(), 2
                while frame.f_code.co_filename == logging.__file__:
                    frame = frame.f_back
                    depth += 1

                logger.opt(depth=depth, exception=record.exc_info).log(
                    level, record.getMessage()
                )

        # Replace all standard logging handlers with our intercept handler
        logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)

        # msg = f"{logfile_basename} log path: {log_path}, log levels: {pkg_levels}"
        # logger.info(msg)
