#!/usr/bin/env python
# -*- coding: utf-8 -*-

from requests_oauthlib import OAuth1Session
import json
import re
from evernote.api.client import EvernoteClient
import evernote.edam.type.ttypes as Types

# OAuth2.0用のキーを取得する
with open("twitter.json") as f:
    secretjson = json.load(f)

CK = secretjson["consumer_key"]          # Consumer Key
CS = secretjson["consumer_secret"]       # Consumer Secret
AT = secretjson["access_token"]          # Access Token
AS = secretjson["access_token_secret"]   # Accesss Token Secert

with open("evernote.json") as f:
    enjson = json.load(f)

# evernote
dev_token = enjson["dev_token"]
client = EvernoteClient(token=dev_token)

noteStore = client.get_note_store()
note = Types.Note()

# タイムライン取得用のURL
url = "https://api.twitter.com/1.1/statuses/user_timeline.json"

# とくにパラメータは無い
params = { "count" : "1" }

# OAuth で GET
twitter = OAuth1Session(CK, CS, AT, AS)
req = twitter.get(url, params = params)

if req.status_code == 200:
    # レスポンスはJSON形式なので parse する
    timeline = json.loads(req.text)
    # 各ツイートの本文を表示
    for tweet in timeline:
    	text = "<p>" + tweet["text"] + "</p>"
    	try:
    		img = "<img src=\"" + tweet["entities"]["media"][0]["media_url"] + "\" />"
    	except:
    		img = ""
        note.title = "tweet: " + tweet["text"].encode('utf_8')
        note.content = '<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE en-note SYSTEM "http://xml.evernote.com/pub/enml2.dtd">'
        note.content += '<en-note>'
        note.content += (text + img).encode('utf_8')
        note.content += '</en-note>'
        note = noteStore.createNote(note)

else:
    # エラーの場合
    print ("Error: %d" % req.status_code)