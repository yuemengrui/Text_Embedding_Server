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
    LOG_LEVEL = logging.INFO

    EMBEDDING_MODEL_LIST = [
        {
            "embedding_type": "text",
            "model_name": "m3e-base",
            "max_seq_length": 512,
            "embedding_dim": 768,
            "model_path": "",
            "device": "cuda"
        },
        {
            "embedding_type": "text",
            "model_name": "text2vec-large-chinese",
            "max_seq_length": 512,
            "embedding_dim": 1024,
            "model_path": "",
            "device": "cuda"
        }
    ]



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
