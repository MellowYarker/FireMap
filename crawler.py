import json
import oauth2 as oauth
consumer_key = 'ADD_YOUR_KEY'
consumer_secret = 'ADD_YOUR_KEY'

access_token = 'ADD_YOUR_KEY'
access_token_secret = 'ADD_YOUR_KEY'

consumer = oauth.Consumer(key=consumer_key, secret=consumer_secret)
access_token = oauth.Token(key=access_token, secret=access_token_secret)
client = oauth.Client(consumer, access_token)

timeline_endpoint = 'https://api.twitter.com/1.1/statuses/user_timeline.json?screen_name=tofire&count=200&exclude_replies=true&include_rts=false'

response, data = client.request(timeline_endpoint)

tweets = json.loads(data.decode('utf-8'))

with open("extracted.txt", 'w') as f:
    for tweet in tweets:
        f.write(str(tweet['text']) + '\n')
    # print(tweet['text'], tweet['created_at'])
