import json
import oauth2 as oauth
consumer_key = 'PcbOwOjAbWhptLNby9ZAOwYyX'
consumer_secret = 'VNUAhklgxH5RDZ3qan4mjRoXgcTKhJiDGb4ls6vQ6RB7cYdN2m'

access_token = '881921522981642240-qgG0HddwwkI2YImAzA7XdKobmLtjD5l'
access_token_secret = 'YJ5OEOYicHgB8f99VNGd1bKSYPekqv882xj8Nf3dG5Asx'

consumer = oauth.Consumer(key=consumer_key, secret=consumer_secret)
access_token = oauth.Token(key=access_token, secret=access_token_secret)
client = oauth.Client(consumer, access_token)

timeline_endpoint = 'https://api.twitter.com/1.1/statuses/user_timeline.json?screen_name=tofire&count=20&exclude_replies=true&include_rts=false'

response, data = client.request(timeline_endpoint)

tweets = json.loads(data.decode('utf-8'))

with open("extracted.txt", 'w') as f:
    for tweet in tweets:
        f.write(str(tweet['text']) + '\n')
    # print(tweet['text'], tweet['created_at'])


