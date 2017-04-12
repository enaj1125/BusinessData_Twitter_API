# import libraries 

from Business_Twitter_API import *




# main function 
if __name__ == '__main__':

    # Set query paramters 
    access_token = os.environ.get("access_token")
    access_token_secret = os.environ.get("access_token_secret")
    consumer_key = os.environ.get("consumer_key")
    consumer_secret = os.environ.get("consumer_secret")


    # Set up Mongo DB 
    client = MongoClient()
    db = client.test_database  # get a database
    tweets = db.tweets         # get a collection


    # Intilize API
    api = TwitterAPI(access_token, access_token_secret, consumer_key, consumer_secret)    


    # Request data from API
    api.request_business_twitter_data("philz", 1, tweets)


    # Check if business data
    check_exsit = api.check_business_twitter_data("philz", tweets)
    print check_exsit


    # Summarize business data
    # summary = api.summarize_business_twitter_data("philz", tweets)
    # print summary


    # # Print out business data 
    # printout = api.print_business_twitter_data("philz", tweets, 5)
    
