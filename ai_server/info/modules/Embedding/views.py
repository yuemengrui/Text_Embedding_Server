# *_*coding:utf-8 *_*
# @Author : YueMengRui
import json
from . import embedding_blu
from info import limiter, text_embedding_model
from flask import request, jsonify, current_app
from info.utils.response_code import RET, error_map


@embedding_blu.route('/ai/text/embedding', methods=['POST'])
@limiter.limit("60 per minute", override_defaults=False)
def text_embedding():
    data = request.get_data()
    json_data = json.loads(data.decode("utf-8"))
    sentences = json_data.get('sentences', [])

    current_app.logger.info(str({'sentences': sentences}) + '\n')

    if not sentences:
        return jsonify(errcode=RET.PARAMERR, errmsg=error_map[RET.PARAMERR])

    try:
        embeddings = text_embedding_model.encode(sentences)
        return jsonify(errcode=RET.OK, errmsg=error_map[RET.OK], data={'embeddings': [x.tolist() for x in embeddings]})
    except Exception as e:
        current_app.logger.error(str({'EXCEPTION': e}) + '\n')
        return jsonify(errcode=RET.DATAERR, errmsg=error_map[RET.DATAERR])
