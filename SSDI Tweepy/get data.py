import json
from pprint import pprint
import re
from stop_words import get_stop_words
from os import path
from wordcloud import WordCloud, STOPWORDS
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

n=0
data=[]
words1=[]

'''
open file
'''
SEARCH = input("Enter the datafile path: ")
OUTPUT_FILE_PATH = SEARCH + '.txt'
f = open(OUTPUT_FILE_PATH, 'r', encoding='utf-8')


for line in f:
   if len(line.strip())>0:
       data.append(line)
   #n = n+1
#print (n)
t=0



temp = []
dataDict ={}
'''
save data in dataDict as structure listed below
ID:(name, time, tweets, followers, retweet)

'''

for i,tweet in enumerate(data):
    temp = tweet.split(" ")
   
    
    s=temp[3:(-2)]

    sentence = ""
    for word in s:
        sentence = sentence+word+' '

    
    dataDict[i]=(temp[0],temp[1],sentence,temp[-2],temp[-1])

#print(dataDict[56])
#('talk2tori', '[14/Feb/2018:15:39:03', '"“I have 3 doctors appointments today”: True life- I was hit by a car as a pedestrian" ', '814', '0\n')

'''
The top n users who have tweeted the most for the entire timeline.

'''
def userTweetMost(n):
    SEARCH = input("Enter the file write path: ")
    OUTPUT_FILE_PATH = SEARCH + '.txt'
    myDict={}
    count = 1
    
    for i in dataDict:
        if dataDict[i][0] in myDict:
            myDict[dataDict[i][0]] += 1
        else:
            myDict[dataDict[i][0]] = 1
    dictSortedkey = sorted(myDict, key=myDict.get, reverse=True)
    newFile = open(OUTPUT_FILE_PATH, 'w', encoding = 'utf-8')
    newFile.write("The top " + str(n) + " users who have tweeted the most for the entire timeline:"+"\n\n")
    for i in dictSortedkey:
        newFile.write("The top " + str(count) + " user " + str(i) + " has tweeted: "+ str(myDict[i]) + "times." + "\n")
        count += 1
        if count > 10:
            break
    newFile.close
#userTweetMost(10)
        

'''
The top n users who have tweeted the most for every hour.

'''
def userTweetperhour(n):
    SEARCH = input("Enter the file write path: ")
    OUTPUT_FILE_PATH = SEARCH + '.txt'
    rows_list = []
    dayList = []
    for i in dataDict:
        RecordtoAdd = {}
        
        t = dataDict[i][1]
        # get '[14/Feb/2018:15:39:03'
        t1 = t.split("/")
        t1[0] = t1[0][1:]
        #get '14', 'Feb', '2018:15:39:16'
        t2 = t1[2]
        t3 = t2.split(":")
        #get ['2018','15','39','16']
        year = t3[0]
        #get '2018'
        day = year + '-' + t1[1] + '-' + t1[0] + '-' + t3[1]
        RecordtoAdd.update({'Day' : (year + '-' + t1[1] + '-' + t1[0] + '-' + t3[1])})
        RecordtoAdd.update({'Name' : dataDict[i][0]})
        rows_list.append(RecordtoAdd)    
        if day in dayList:
            pass
        else:
            dayList.append(day)

    AnalysedData = pd.DataFrame(rows_list)
    AnalysedData1 = AnalysedData.groupby(['Day','Name']).size().reset_index(name='counts')
    
    ad = AnalysedData1.groupby(['Day','Name']).agg({'counts':sum})
    newFile = open(OUTPUT_FILE_PATH, 'w', encoding = 'utf-8')
    for i in dayList:
        
        temp = 0
        temp = ad.loc[i,'counts']
        temp = temp.sort_values(ascending=False)        
        tempTop10 = temp.nlargest(n)
        newFile.write('Top ' + str(n) + ' user who have tweeted the most at ' + str(i) + "\n\n")
        newFile.write(str(tempTop10))
    newFile.close





userTweetperhour(10)
 


'''
The top n users who have the maximum followers.

'''
def userMaximumFollower(n):

    SEARCH = input("Enter the file write path: ")
    OUTPUT_FILE_PATH = SEARCH + '.txt'
    nameList=[]
    rows_list = []
    count = 1
    
    for i in dataDict:
        name = dataDict[i][0]
        follower = int(dataDict[i][-2])
        if name in nameList:
            pass
        else:
            nameList.append(name) 
            RecordtoAdd = {}
            RecordtoAdd.update({'Follower' :follower})
            RecordtoAdd.update({'Name' : name})
            rows_list.append(RecordtoAdd)    

    AnalysedData = pd.DataFrame(rows_list)
    df = AnalysedData.sort_values(['Follower','Name'], ascending=False)
    df.reset_index(drop=True, inplace=True)
    df1 = df[:n]
    
    newFile = open(OUTPUT_FILE_PATH, 'w', encoding = 'utf-8')
    newFile.write("The top " + str(n) + " users who have the maximum followers:"+"\n\n")
   
    for i in df1.get_values():
        newFile.write("The top " + str(count) + " user " + str(i[1]) + " has "+ str(i[0]) + " followers." + "\n")
        count += 1
    newFile.close
#call function userMaximumFollower(10)
#userMaximumFollower(10)

'''
The top n tweets which have the maximum retweet count.

'''
def tweetMaximumRetweet(n):

    SEARCH = input("Enter the file write path: ")
    OUTPUT_FILE_PATH = SEARCH + '.txt'
    tweetList=[]
    rows_list = []
    count = 1
    
    for i in dataDict:
        tweets = dataDict[i][2]
        retweet = int(dataDict[i][-1])
        if tweets in tweetList:
            pass
        else:
            tweetList.append(tweets)
            RecordtoAdd = {}
            RecordtoAdd.update({'Tweet' : tweets})
            RecordtoAdd.update({'retweetCount' : retweet})
            rows_list.append(RecordtoAdd)    

    AnalysedData = pd.DataFrame(rows_list)
    df = AnalysedData.sort_values(['retweetCount','Tweet'], ascending=False)
    df.reset_index(drop=True, inplace=True)
    df1 = df[:n]
    
    newFile = open(OUTPUT_FILE_PATH, 'w', encoding = 'utf-8')
    for i in df1.get_values():
        newFile.write("The top " + str(count) + " tweet: " + str(i[0]) + "has "+ str(i[1]) + " retweets." + "\n\n")
        count += 1
    newFile.close
    
# call function tweetMaximumRetweet(10)




