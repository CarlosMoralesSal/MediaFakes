# -*- coding: utf-8 -*-
"""
Created on Tue Apr  7 20:26:53 2020

@author: Carlos
"""

#!/usr/bin/env python
# encoding: utf-8

import tweepy #https://github.com/tweepy/tweepy
import csv
import sys

#Twitter API credentials
consumer_key = ""
consumer_secret = ""
access_key = ""
access_secret = ""


def get_all_tweets(screen_name):
        #Twitter only allows access to a users most recent 3240 tweets with this method

        #authorize twitter, initialize tweepy
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_key, access_secret)
        api = tweepy.API(auth)

        #initialize a list to hold all the tweepy Tweets
        alltweets = []

        #make initial request for most recent tweets (200 is the maximum allowed count)
        new_tweets = api.user_timeline(screen_name = screen_name,count=1)

        #save most recent tweets
        alltweets.extend(new_tweets)

        #save the id of the oldest tweet less one
        oldest = alltweets[-1].id - 1

        #keep grabbing tweets until there are no tweets left to grab
        while len(new_tweets) > 0:
                print("getting tweets before %s" % (oldest))

                #all subsequent requests use the max_id param to prevent duplicates
                new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)

                #save most recent tweets
                alltweets.extend(new_tweets)

                #update the id of the oldest tweet less one
                oldest = alltweets[-1].id - 1

                print("...%s tweets downloaded so far" % (len(alltweets)))

        #go through all found tweets and remove the ones with no images 
        outtweets = [] #initialize master list to hold our ready tweets
        for tweet in alltweets:
                #not all tweets will have media url, so lets skip them
                try:
                        print(tweet.entities['media'][0]['media_url'])
                except (NameError, KeyError):
                        #we dont want to have any entries without the media_url so lets do nothing
                        pass
                else:
                        #got media_url - means add it to the output
                        outtweets.append([tweet.entities['media'][0]['media_url']])

        #write the csv  
        with open('%s_tweets.csv' % screen_name, 'w') as f:
            writer = csv.writer(f)
       #         #writer.writerow(["id","created_at","text","media_url"])
            writer.writerows(outtweets)

        pass
        with open('%s_tweets.csv' % screen_name) as infile, open('%s_tweets_clean.csv' % screen_name, 'w') as outfile:
            for line in infile:
                if not line.strip(): continue  # skip the empty line
                outfile.write(line)  # 


if __name__ == '__main__':
        #pass in the username of the account you want to download
        get_all_tweets("CarlosMoralesD1")