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
1) Request limit hit: handling the request limit hit error by capturing that error using Exception 
2) Prevent duplicated message: handling the duplicated message by check each twitter ID which is unique
3) Check misformat input query parameters: (a) negative number of input message, (b) too long message, which contains more than 140 characters
4) Keep logging record of if a request has been succeed or failed. 


### To install/import the API library

from Business_Twitter_API import *

### To use the library

##### 1) Set query paramters 

access_token = os.environ.get("access_token")

access_token_secret = os.environ.get("access_token_secret")

consumer_key = os.environ.get("consumer_key")

consumer_secret = os.environ.get("consumer_secret")


2) Set up Mongo DB 

client = MongoClient()

db = client.test_database  # get a database
    
tweets = db.tweets         # get a collection


3) Intilize API

api = TwitterAPI(access_token, access_token_secret, consumer_key, consumer_secret)    


4) Request data from API
    
api.request_business_twitter_data("philz", -2, tweets)
