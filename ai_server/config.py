# *_*coding:utf-8 *_*
import os
import json
import logging
from urllib import parse


class Config(object):
    SECRET_KEY = 'YueMengRui-LLM'

    JSON_AS_ASCII = False

    # 默认日志等级
    LOG_LEVEL = logging.INFO
    LOGGER_MODE = 'gunicorn'


class DevelopmentConfig(Config):
    """开发模式下的配置"""
    DEBUG = logging.INFO

    EMBEDDING_MODEL_NAME_OR_PATH = ''
    EMBEDDING_DEVICE = "cuda"


class UatConfig(Config):
    """生产模式下的配置"""
    LOG_LEVEL = logging.INFO


class ProductionConfig(Config):
    """生产模式下的配置"""
    LOG_LEVEL = logging.INFO


config_dict = {
    "dev": DevelopmentConfig,
    "uat": UatConfig,
    "prod": ProductionConfig
}
