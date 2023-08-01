# *_*coding:utf-8 *_*
import os
import logging
from config import config_dict
from flask import Flask
from flask_cors import CORS
from copy import deepcopy
from flask_limiter import Limiter
from logging.handlers import TimedRotatingFileHandler
from sentence_transformers import SentenceTransformer


def setup_logging(log_level):
    logging.basicConfig(level=log_level)
    # file_log_handler = RotatingFileHandler("logs/log", maxBytes=1024 * 1024 * 100, backupCount=10)
    file_log_handler = TimedRotatingFileHandler("logs/log", when="MIDNIGHT", backupCount=30)
    file_log_handler.suffix = "%Y-%m-%d.log"
    formatter = logging.Formatter('[%(asctime)s] %(levelname)s %(filename)s:%(lineno)d %(message)s')
    file_log_handler.setFormatter(formatter)
    logging.getLogger().addHandler(file_log_handler)


def api_limit_key_func():
    return '127.0.0.1'
    # return request.remote_addr or "127.0.0.1"


limiter = Limiter(
    key_func=api_limit_key_func,
    # 默认方案 每小时2000，每分钟100，适用于所有路线。如果想忽略此全局配置，方法上增加此注解@limiter.exempt
    default_limits=["60 per minute"]
)

app = Flask(__name__, static_folder='', static_url_path='')
CORS(app)
config_cls = config_dict['dev']
app.config.from_object(config_cls)
if not os.path.exists(app.config['TEMP_FILE_DIR']):
    os.makedirs(app.config['TEMP_FILE_DIR'])
if not os.path.exists(app.config['VS_ROOT_DIR']):
    os.makedirs(app.config['VS_ROOT_DIR'])

app.json.ensure_ascii = False

if app.config['LOGGER_MODE'] == 'gunicorn':
    gunicorn_logger = logging.getLogger('gunicorn.access')
    app.logger = gunicorn_logger
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
else:
    setup_logging(config_cls.LOG_LEVEL)

limiter.init_app(app)

embedding_model_list = []

for d in deepcopy(app.config['EMBEDDING_MODEL_LIST']):
    model_path = d.pop('model_path')
    device = d.pop('device')

    if model_path:
        embedding_model = SentenceTransformer(model_name_or_path=model_path, device=device)

        d.update({"embedding_model": embedding_model})
        embedding_model_list.append(d)


from info.modules.Embedding import embedding_blu
app.register_blueprint(embedding_blu)
