import tweepy
import pandas as pd
import numpy as np
from twitter_access import holder

#pulling keys from separate script
keys = holder()

#authentication to endpoint
auth = tweepy.OAuth1UserHandler(keys['consumer_key'], keys['consumer_secret'], keys['access_token'], keys['access_token_secret'])
api = tweepy.API(auth)

class bot:
    def __init__(bot):
        pass

    def tweet(bot):
        body = input("Enter what you would like to tweet:\n")
        api.update_status(body)

#returns dataframe with up to 10000 tweets about a user inputted topic
    def search_tool(bot, query):
        results = api.search_tweets(q=query, count=10000)
        data = []
        for result in results:
            data.append(result.created_at)
        df = pd.DataFrame(data, columns=['Search Term Results Timestamp'])
        df['Tweet Text'] = np.array([result.text for result in results])
        df['Tweet Length'] = np.array([len(result.text) for result in results])
        df['Tweet ID'] = np.array([result.id for result in results])
        df["Location"] = np.array([result.geo for result in results])
        return df

    #returns dataframe of the last 10 favourited tweets from the authenticated user
    def faves(bot):
        data = []
        favourites = api.get_favorites(count=10)
        for fave in favourites:
            data.append(fave.created_at)
        df = pd.DataFrame(data, columns="My Favourite Tweets Timestamp")
        df['Tweet Text'] = np.array(fave.text for fave in favourites)
        df['Tweet Length'] = np.array(len(fave.text) for fave in favourites)
        df['Tweet ID'] = np.array([fave.id for fave in favourites])
        return df
    
    #returns a dataframe with the last 1000 tweets from the specificied user
    def user_search(bot, screenName):
        data = []
        timeline = api.user_timeline(screen_name=screenName, count=1000)
        for tweets in timeline: data.append(tweets.created_at)
        df = pd.DataFrame(data, columns=["Tweet Timestamp"])
        df['Tweet Text'] = np.array(tweets.text for tweets in timeline)
        df['Tweet Length'] = np.array(len(tweets.text) for tweets in timeline)
        df['Tweet ID'] = np.array([tweets.id for tweets in timeline])
        return df

    #takes in a pandas dataframe and creates a csv output to be used in tableau
    def data_extract(bot, df):
        df.to_csv(r'Data Output/data_output.csv')
            

choice = input("1 to pull user data, 2 to pull search term data, 3 to get favourites data\n")
test_bot = bot()

if choice == "1":
    #allows user to tweet from the cmd-line
    x = test_bot.user_search(input("Please enter the twitter handle of the user whose tweets you want to pull:\n"))
    test_bot.data_extract(x)

elif choice == "2":
    #allows a user to search for tweets related to the string they enter
    y = test_bot.search_tool(input("Enter a search term:\n"))
    test_bot.data_extract(y)    

else:
    #allows you to search twitter by a topic
    z = test_bot.faves()
    test_bot.data_extract(z)



