# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
#Fizz Buzz
import tweepy


ACCESS_TOKEN = '905181825127022593-gKI45FEc7dAbdZNSY6KAd4OOUPF3sxW'
ACCESS_SECRET = 'X9tuQUZx73LGfYI0geRSjninLB5TbuCMf8Pt1dPL0QT3V'
CONSUMER_KEY = 'eDkXjOyo5F2LC6EI71hMbpvDD'
CONSUMER_SECRET = 'tQTSHWFYMrlNXuexiLYqKMyPqEoqplME9elT7jXWsvybYGMP7N'
SEARCH=input("Enter the search string ")
print (SEARCH)
FROM=input("Enter the from date (YYYY-MM-DD format) ")
print (FROM)
TO=input("Enter the to data (YYYY-MM-DD format) ")
print (TO)
INPUT_FILE_PATH= './'+SEARCH+'.txt'

num=int(input("Enter the number of tweets you want to retrieve for the search string "))
auth = tweepy.auth.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth)

i=0;

f = open(INPUT_FILE_PATH, 'w', encoding='utf-8')

for res in tweepy.Cursor(api.search, q=("{}&since:{}&until:{}").format(SEARCH,FROM,TO), rpp=100, count=20, result_type="recent", include_entities=True, lang="en").items(num):
    i+=1
    f.write(res.user.screen_name)
    f.write(' ')
    f.write('[')
    f.write(res.created_at.strftime("%d/%b/%Y:%H:%M:%S %Z"))
    f.write(']')	
    f.write(" ")
    f.write('"')
    f.write(res.text.replace('\n',''))
    f.write('"')
    f.write(" ")
    f.write(str(res.user.followers_count))
    f.write(" ")
    f.write(str(res.retweet_count))
    f.write('\n')
f.close
print("Tweets retrieved ",i)