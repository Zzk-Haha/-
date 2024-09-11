
from flask import Flask, session, redirect, url_for, flash, render_template, g, request, jsonify
import config
from exts import db,mail
from models import UserModel
from blueprints.qa import bp as qa_bp
from blueprints.auth import bp as auth_bp
from models import UserModel
from flask_migrate import Migrate
import large_model_api
import xunfei_api
import logging
import uuid
import requests
import time
import hashlib
import hmac
import base64
import urllib.parse


app = Flask(__name__)
# 绑定配置文件
app.config.from_object(config)

# 先创建再绑定
db.init_app(app)
mail.init_app(app)

migrate=Migrate(app,db)


# 绑定
app.register_blueprint(qa_bp)
app.register_blueprint(auth_bp)

# blueprint 用来做模块化的
# 电影，读书，音乐，xx，模块化

@app.route('/api/vivogpt', methods=['POST'])
def vivogpt_endpoint():
    # 获取前端发送的文本数据
    data = request.get_json()
    message = data.get('message')

    if not message:
        return jsonify({'error': 'No message provided'}), 400

    # 调用大模型API
    response_data = large_model_api.sync_vivogpt(message)

    # 返回结果给前端
    return jsonify(response_data)


@app.route('/api/xunfei', methods=['POST'])
def xunfei_api():
    # 获取前端发送的文本数据
    data = request.get_json()
    message = data.get('message')


    # 调用大模型API
    response_data = xunfei_api.use_xunfei_api(message)

    # 返回结果给前端
    return jsonify(response_data)



# before_request/beofore_first_request/after_request
# hook
@app.before_request
def my_before_request():
    user_id=session.get('user_id')
    if user_id:
        user=UserModel.query.get(user_id)
        setattr(g,'user',user)
    else:
        setattr(g,'user',None)

@app.context_processor
def my_context_processor():
    return {'user':g.user}




if __name__ == '__main__':
    app.run(debug=True)
