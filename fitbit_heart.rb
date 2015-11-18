require 'json'
require 'oauth2'
require 'base64'
require 'readline'
require "twitter"


json_fitbit = open('fitbit.json') do |io|
  JSON.load(io)
end
client_id     = json_fitbit["client_id"]
client_secret = json_fitbit["client_secret"]
redirect_uri  = json_fitbit["redirect_uri"]

client = OAuth2::Client.new(client_id, client_secret, site: 'https://api.fitbit.com', authorize_url: 'https://www.fitbit.com/oauth2/authorize', token_url: 'https://api.fitbit.com/oauth2/token')
authurl = client.auth_code.authorize_url(redirect_uri: redirect_uri, scope: 'heartrate')
p authurl

p "上記のURLにアクセスして認証後、codeパラメータの値を入力: "
code = Readline.readline

bearer_token = "#{client_id}:#{client_secret}"
encoded_bearer_token = Base64.strict_encode64(bearer_token)

access_token = client.auth_code.get_token(code, grant_type: 'authorization_code', client_id: client_id, redirect_uri: redirect_uri, :headers => {'Authorization' => "Basic #{encoded_bearer_token}"})

#twitter
json_twitter = open('twitter.json') do |io|
  JSON.load(io)
end

twitter = Twitter::REST::Client.new do |config|
  config.consumer_key        = json_twitter["consumer_key"]
  config.consumer_secret     = json_twitter["consumer_secret"]
  config.access_token        = json_twitter["access_token"]
  config.access_token_secret = json_twitter["access_token_secret"]
end
#/twitter

count = 0   # 一時間近く経ったらアクセストークンをリフレッシュする
while true do
	hearts = JSON.parse(access_token.get('https://api.fitbit.com/1/user/-/activities/heart/date/today/1d.json').body)
	heart = hearts["activities-heart-intraday"]["dataset"].last()
	p heart
	if heart == nil then
		sleep 300
		next
	end
	heart_t = heart["time"]
	heart_v = heart["value"]

	if heart_v > 90 then
		twitter.update("ただいま緊張しております！心拍数#{heart_v} (#{heart_t})")
	end

	sleep 300
	
	count += 1
	if count > 10 then
		access_token = access_token.refresh!(grant_type: 'refresh_token', refresh_token: access_token.refresh_token, :headers => {'Authorization' => "Basic #{encoded_bearer_token}"})
		count = 0
	end
end
