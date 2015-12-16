#!/usr/bin/env python
# -*- coding: utf-8 -*-

from requests_oauthlib import OAuth1Session
from datetime import datetime, timedelta, tzinfo
import json
import re

# OAuth2.0用のキーを取得する
with open("twitter.json") as f:
    secretjson = json.load(f)

CK = secretjson["consumer_key"]          # Consumer Key
CS = secretjson["consumer_secret"]       # Consumer Secret
AT = secretjson["access_token"]          # Access Token
AS = secretjson["access_token_secret"]   # Accesss Token Secert

# タイムライン取得用のURL
url = "https://api.twitter.com/1.1/statuses/user_timeline.json"

# とくにパラメータは無い
params = { "count" : "50" }

# OAuth で GET
twitter = OAuth1Session(CK, CS, AT, AS)
req = twitter.get(url, params = params)

# タイムゾーン設定
class JST(tzinfo):
    def utcoffset(self, dt):
        return timedelta(hours=9)

    def dst(self, dt):
        return timedelta(0)

    def tzname(self, dt):
        return 'JST'

if req.status_code == 200:
    # レスポンスはJSON形式なので parse する
    timeline = json.loads(req.text)
    # 各ツイートの本文を表示
    now = datetime.now(tz=JST()).replace(tzinfo=None)
    print "now:" + str(now)
    for tweet in timeline:
        # print(json.dumps(tweet, indent=4))
        t   = datetime.strptime(tweet["created_at"], "%a %b %d %H:%M:%S +0000 %Y")
        print "t:" + str(t)
        print (now - t).seconds
        if (now - t).seconds < 300:
            time        = datetime.strptime(tweet["created_at"], "%a %b %d %H:%M:%S +0000 %Y").strftime('%Y/%m/%d %H:%M:%S')
            time_html   = time + "<br />"
            text_html   = re.sub(r'((http|https)://[A-Za-z0-9.-_]*)', '', tweet["text"]).replace("\n", "<br />")
            source_html = "<br />by " + tweet["source"]
    
            if len(tweet["entities"]["urls"]) > 0:
                url = tweet["entities"]["urls"][0]["expanded_url"]
                url_html = ' <a href="' + url + '">' + url + '</a>'
            else:
                url_html = ""
    
            try:
                img_html = "<br><img src=\"" + tweet["entities"]["media"][0]["media_url"] + "\" />"
            except:
                img_html = ""
    
            print((time_html + text_html + url_html + source_html + img_html + "<hr />").encode('utf_8'))

else:
    # エラーの場合
    print ("Error: %d" % req.status_code)