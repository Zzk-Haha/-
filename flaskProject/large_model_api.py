#!/usr/bin/env python
# encoding: utf-8

import uuid
import time
import requests
import random
import string
import time
import hashlib
import hmac
import base64
import urllib.parse

__all__ = ['gen_sign_headers']


# 随机字符串
def gen_nonce(length=8):
    chars = string.ascii_lowercase + string.digits
    return ''.join([random.choice(chars) for _ in range(length)])


# 如果query项只有key没有value时，转换成params[key] = ''传入
def gen_canonical_query_string(params):
    if params:
        escape_uri = urllib.parse.quote
        raw = []
        for k in sorted(params.keys()):
            tmp_tuple = (escape_uri(k), escape_uri(str(params[k])))
            raw.append(tmp_tuple)
        s = "&".join("=".join(kv) for kv in raw)
        return s
    else:
        return ''


def gen_signature(app_secret, signing_string):
    bytes_secret = app_secret.encode('utf-8')
    hash_obj = hmac.new(bytes_secret, signing_string, hashlib.sha256)
    bytes_sig = base64.b64encode(hash_obj.digest())
    signature = str(bytes_sig, encoding='utf-8')
    return signature


def gen_sign_headers(app_id, app_key, method, uri, query):
    method = str(method).upper()
    uri = uri
    timestamp = str(int(time.time()))
    app_id = app_id
    app_key = app_key
    nonce = gen_nonce()
    canonical_query_string = gen_canonical_query_string(query)
    signed_headers_string = 'x-ai-gateway-app-id:{}\nx-ai-gateway-timestamp:{}\n' \
                            'x-ai-gateway-nonce:{}'.format(app_id, timestamp, nonce)
    signing_string = '{}\n{}\n{}\n{}\n{}\n{}'.format(method,
                                                     uri,
                                                     canonical_query_string,
                                                     app_id,
                                                     timestamp,
                                                     signed_headers_string)
    signing_string = signing_string.encode('utf-8')
    signature = gen_signature(app_key, signing_string)
    return {
        'X-AI-GATEWAY-APP-ID': app_id,
        'X-AI-GATEWAY-TIMESTAMP': timestamp,
        'X-AI-GATEWAY-NONCE': nonce,
        'X-AI-GATEWAY-SIGNED-HEADERS': "x-ai-gateway-app-id;x-ai-gateway-timestamp;x-ai-gateway-nonce",
        'X-AI-GATEWAY-SIGNATURE': signature
    }
#-------------------------------------------------------------------------------------------------------------------

# 请替换APP_ID、APP_KEY
APP_ID = '3030307186'
APP_KEY = 'tnukhWAwDifLroDv'
URI = '/vivogpt/completions'
DOMAIN = 'api-ai.vivo.com.cn'
METHOD = 'POST'


def sync_vivogpt(message):
    params = {
        'requestId': str(uuid.uuid4())
    }
    print('requestId:', params['requestId'])

    data = {

        'prompt': message,
        'model': 'vivo-BlueLM-TB',
        'sessionId': str(uuid.uuid4()),
        'extra': {
            'temperature': 0.9
        }
    }
    headers = gen_sign_headers(APP_ID, APP_KEY, METHOD, URI, params)
    headers['Content-Type'] = 'application/json'

    start_time = time.time()
    url = 'https://{}{}'.format(DOMAIN, URI)
    response = requests.post(url, json=data, headers=headers, params=params)

    if response.status_code == 200:
        res_obj = response.json()
        #print(f'response:{res_obj}')
        if res_obj['code'] == 0 and res_obj.get('data'):
            content = res_obj['data']['content']
            return {'status': 'success', 'content': content}
        else:
            return {'status': 'error', 'message': res_obj.get('message', 'Unknown error')}
    else:
        return {'status': 'error', 'message': f'Status code: {response.status_code}, {response.text}'}

    end_time = time.time()
    timecost = end_time - start_time
    print('请求耗时: %.2f秒' % timecost)

# if __name__ == '__main__':
#     question = input('请输入:')
#     result = sync_vivogpt(question)
#     print(result)

