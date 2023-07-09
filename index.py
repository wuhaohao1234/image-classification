import hashlib
import random
import time
import requests


def get_nonce():
    pool = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    length = 10
    ret = ""

    while len(ret) < length:
        ret += random.choice(pool)
    return ret


ts = str(int(time.time()))
nonce = get_nonce()
access_key = "r1alN7e35UlDxBd5wyGo2WKx"
secret_key = "2qxo6N5ZLIJBxLv9M0r4Ln7E"

concat_string = "uri=/api/v1/openapi/auth&ts=%s&nonce=%s&accessKey=%s&secretKey=%s" % (ts, nonce, access_key, secret_key)
sign = hashlib.sha256(concat_string.encode("utf-8")).hexdigest()

url = "https://platform.openmmlab.com/gw/user-service/api/v1/openapi/auth"

imageClassificationUrl = 'https://platform.openmmlab.com/gw/model-inference/openapi/v1/classification'

imageUrl = "https://cdn.wujiebantu.com/ai/3536B713E92EEF8C6F3D2BFC9C8D053B-01.jpg?imageView2/2/w/800/q/75/format/webp"


headers = {
    "ts": ts,
    "nonce": nonce,
    "sign": sign,
    "accessKey": access_key
}
ret = requests.post(url, headers=headers)

auth = ret.json()['data']['accessToken']

body = {
  "resource": imageUrl,
  "resourceType": "URL",
  "requestType": "SYNC",
  "backend": "PyTorch",
  "algorithm": "Swin-Transformer",
  "dataset": "ImageNet"
}

headers = {
  'Authorization': auth
}


response = requests.post(imageClassificationUrl, headers=headers, json=body)


print(response.json()['data']['result'])