
# Title: Business Twitter API for searching and downloading business related data from Twitter REST API.
# author: Yan Jiang
# Developed in April, 2017


# Major functions:
# 1) request twitter data related to a business: request_business_twitter_data
# 2) check if there is twitter data related to a business: check_business_twitter_data
# 3) summarize twitter data related to a business: summarize_business_twitter_data
# 4) print to screen twitter data related to business in the database: request_business_twitter_data


# Special features include: 
# 1) Request limit hit: handling the request limit hit error by capturing that error using Exception 
# 2) Prevent duplicated message: handling the duplicated message by check each twitter ID which is unique
# 3) Check misformat input query parameters: (a) negative number of input message, (b) too long message, which contains more than 140 characters
# 4) Keep logging record of if a request has been succeed or failed. 



# Import libraries
import json
import time 
import os
import tweepy
import pymongo
import pprint
import logging
from logging.config import dictConfig
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from pymongo import MongoClient



# set up the logger using dictionary file 
logging_config = dict(
    version = 1,
    formatters = {
        'f': {'format':
              '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'}
        },
    handlers = {
        'h': {'class': 'logging.StreamHandler',
              'formatter': 'f',
              'level': logging.DEBUG}
        },
    root = {
        'handlers': ['h'],
        'level': logging.DEBUG,
        },
)

dictConfig(logging_config)
logger = logging.getLogger()



# set up twitter api object
class TwitterAPI(object):
    """
    Access REST API resources

    :param consumer_key: Twitter application consumer key
    :param consumer_secret: Twitter application consumer secret
    :param access_token: Twitter application access token key
    :param access_token_secret: Twitter application access token secret

    """

    def __init__(self,
        access_token =  None,
        access_token_secret = None,  
        consumer_key = None,
        consumer_secret = None):

        """ This handles Twitter authetification and the connection to Twitter Streaming API """

        self.auth = OAuthHandler(consumer_key, consumer_secret)
        self.auth.set_access_token(access_token, access_token_secret)
        self.api = tweepy.API(self.auth)
        



    def request_business_twitter_data(self, business_name, number, tweets):
        """
        Request a Twitter REST API for fetch the business name related tweets, and prevent duplicated record
        :param business name: string, name of the business
        :param number: int, number of tweets requested
        :param tweets: file collection of MongoDB, files related to the business 
        """


        # handling edge cases
        if number < 0:
            logger.debug("User request negative number of message")
            return 

            
        # twitter API will not allow for query longer than 140 characters
        if len(business_name) > 140:
            logger.debug("User request a too long string")
            return 


        # Format query and write to DB
        query = business_name
        count_distinct = 0 


        # Keep download data as long as not reach the token limit     
        try: 
            # Write into database iteratively
            for status in tweepy.Cursor(self.api.search, q=query).items(number):

                # Extract info from tweets 
                raw_json_info = status._json                # convert status to json 
                json_str = json.dumps(status._json)         # convert json to str
                twitter_id = raw_json_info["id"]            # extract twitter id


                # check duplicates 
                check_duplicates = tweets.find({"twitter_id": twitter_id})


                # Write into database
                if check_duplicates.count() == 0:
                    count_distinct += 1

                    reformat_tmp = {"business_name": query, "twitter_id": twitter_id, "tweet_data": raw_json_info} 
                    tweet_id = tweets.insert_one(reformat_tmp).inserted_id                        


        except tweepy.error.TweepError:
            # handle the hitting the request limit error by put a sleep timer for 15 mins. 
            text_message = "Time limit reached, downloaded " + str(count_distinct) + " messages"
            logger.debug(text_message)
            
                
        
        # record a note of finish data downloading 
        logger.debug("Finished data download")
        



    
    def check_business_twitter_data(self, business_name, tweets):
        """
        Check the number of tweets related to a business_name by query the database
        :param business name: string, name of the business
        :param tweets: file collection of MongoDB, files related to the businss 
        :return: bolean variable, True for yes there is this business related data, No for there is no business related data
        """
        
        # twitter API will not allow for query longer than 140 characters
        if len(business_name) > 140:
            logger.debug("User request a too long string")
            return 

        res = tweets.find({"business_name": business_name})
        return res.count() > 0




    def summarize_business_twitter_data(self, business_name, tweets):
        """
        Summarize the number of tweets related to a business_name by query the database
        """

        
        # twitter API will not allow for query longer than 140 characters
        if len(business_name) > 140:
            logger.debug("User request a too long string")
            return 


        res = tweets.find({"business_name": business_name})
        num_tweets = res.count()
        return business_name + ": " + str(num_tweets)



    def print_business_twitter_data(self, business_name, tweets, num = 100):
        """
        Print the tweets json file related to a business_name by query the database
        :param business name: string, name of the business
        :param tweets: file collection of MongoDB, files related to the businss 
        :param num: number of files request to print. It is 100 by default, and can be modified by users.
        :return: None
        :print out the json file onto screen
        """

        
        # handling edge cases
        if num < 0:
            logger.debug("User request negative number of message")
            return 


        # twitter API will not allow for query longer than 140 characters
        if len(business_name) > 140:
            logger.debug("User request a too long string")
            return 


        # search related file to print and use counter to control the number of prints
        res = tweets.find({"business_name": business_name})
        num_tweets = res.count()
        num = min(num_tweets, num) # if the user request to print more than exsiting number of tweets, print all the available tweets 
        counter = 0 

        for doc in res:            
            counter += 1
            if counter > num:
                break 
            print doc


