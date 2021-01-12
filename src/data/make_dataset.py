import pandas as pd
import twint

def tweets_query(search, since, until, pandas=True, csv=True, output='test.csv'):
	'''
	Query tweets with search terms between given dates
	Sample query: tweets_query('#whitelivesmatter', '2020–05–20', '2020–05–30')
	'''
    c = twint.Config()
    c.Search = search
    c.Since = since
    c.Until = until
    c.Hide_output = True
    c.Pandas=True
    c.Store_object = True
    c.Count = True
    c.Store_csv = csv
    c.Output = output
    twint.run.Search(c)
    Tweets_df = twint.storage.panda.Tweets_df
    return Tweets_df