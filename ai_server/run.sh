# prod
CUDA_VISIBLE_DEVICES=0 gunicorn -c gunicorn_conf_text_embedding.py manage:app
