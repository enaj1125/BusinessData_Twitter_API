# Business Data Twitter API


##### Title: Business Twitter API for searching and downloading business related data from Twitter REST API.

##### Author: Yan Jiang

##### Developed in April, 2017


### Major functions:
1) request twitter data related to a business: request_business_twitter_data
2) check if there is twitter data related to a business: check_business_twitter_data
3) summarize twitter data related to a business: summarize_business_twitter_data
4) print to screen twitter data related to business in the database: request_business_twitter_data


### Special features include: 
1) request limit hit: handling the request limit hit error by capturing that error using Exception 
2) duplicated message: handling the duplicated message by check each twitter ID which is unique


1) how to import API library 
from Business_Twitter_API import *


2) Set query paramters 
   access_token = os.environ.get("access_token")
   access_token_secret = os.environ.get("access_token_secret")
   consumer_key = os.environ.get("consumer_key")
   consumer_secret = os.environ.get("consumer_secret")


3) Set up Mongo DB 
  client = MongoClient()
  db = client.test_database  # get a database
  tweets = db.tweets         # get a collection


4) Intilize API
    api = TwitterAPI(access_token, access_token_secret, consumer_key, consumer_secret)    


5) Request data from API
    api.request_business_twitter_data("philz", -2, tweets)


6) Check if business data
    check_exist = api.check_business_twitter_data("philz", tweets)
    print check_exist


7) Summarize business data
    summary = api.summarize_business_twitter_data("philz", tweets)
    print summary


 8) Print out business data 
    api.print_business_twitter_data("philz", tweets, 5)
