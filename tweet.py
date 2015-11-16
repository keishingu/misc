#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from requests_oauthlib import OAuth1Session

# OAuth2.0用のキーを取得する
with open("twitter.json") as f:
    secretjson = json.load(f)

CK = secretjson["consumer_key"]          # Consumer Key
CS = secretjson["consumer_secret"]       # Consumer Secret
AT = secretjson["access_token"]          # Access Token
AS = secretjson["access_token_secret"]   # Accesss Token Secert

# ツイート投稿用のURL
url = "https://api.twitter.com/1.1/statuses/update.json"

# ツイート本文
params = {"status": "Hello, World!"}

# OAuth認証で POST method で投稿
twitter = OAuth1Session(CK, CS, AT, AS)
req = twitter.post(url, params = params)

# レスポンスを確認
if req.status_code == 200:
    print ("OK")
else:
    print ("Error: %d" % req.status_code)