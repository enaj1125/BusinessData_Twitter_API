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
