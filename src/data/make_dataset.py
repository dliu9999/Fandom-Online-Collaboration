import pandas as pd
import twint

def tweets_query(search, since, until, pandas=True, csv=False, output='test.csv'):
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

def user_query(user, since, until, pandas=True, csv=False, output='test.csv'):
    c = twint.Config()
    c.User_id = user
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

# dw = tweets_query('#btsdarkandwild', '2014-08-17', '2014-09-02', csv=True, output='../../data/raw/dark_wild1.csv')
# wings = tweets_query('#bts', '2016-10-08', '2016-10-24', csv=True, output='../../data/raw/wings.csv')
# love = tweets_query('#love_yourself', '2018-05-16', '2018-06-1', csv=True, output='../../data/raw/love1.csv')
# map_ = tweets_query('#bts', '2020-02-19', '2020-03-04', csv=True, output='../../data/raw/map.csv')
# be = tweets_query('#bts_be', '2020-11-18', '2020-12-04', csv=True, output='../../data/raw/bts/be1.csv')

# nine = tweets_query('#ts1989', '2014-10-25', '2014-11-10', csv=True, output='../../data/raw/taylor/nine1.csv')
# reputation = tweets_query('#reputation', '2017-11-08', '2017-11-24', csv=True, output='../../data/raw/taylor/reputation1.csv')
# folklore = tweets_query('#folklore', '2020-07-22', '2020-08-07', csv=True, output='../../data/raw/taylor/folklore1.csv')

# believe = tweets_query('#believe', '2012-06-13', '2012-06-29', csv=True, output='../../data/raw/justin/believe1.csv')
# purpose = tweets_query('#purpose', '2015-11-11', '2015-11-27', csv=True, output='../../data/raw/justin/purpose1.csv')
# changes = tweets_query('#changes', '2020-02-12', '2020-02-28', csv=True, output='../../data/raw/taylor/changes1.csv')

# wlm = tweets_query('#whitelivesmatter', '2020-06-18', '2020-06-30', csv=True, output='../../data/raw/wlm.csv')
# c = twint.Config()
# c.Search = '#whitelivesmatter'
# c.Since = '2020-06-18'
# c.Until = '2020-06-30'
# c.Hide_output = True
# c.Pandas = True
# c.Store_object = True
# twint.run.Search(c)
# Tweets_df = twint.storage.panda.Tweets_df

# jan_jb = tweets_query('#justinbieber', '2021-01-01', '2021-01-31', csv=True, output='../../data/raw/justin/jan_jb.csv')

# taylor1 = user_query('17919972', '2014-10-25', '2014-11-10', csv=True, output='../../data/raw/taylor/taylor1.csv')
# taylor2 = user_query('17919972', '2017-11-08', '2017-11-24', csv=True, output='../../data/raw/taylor/taylor2.csv')
# taylor3 = user_query('17919972', '2020-07-22', '2020-08-07', csv=True, output='../../data/raw/taylor/taylor3.csv')

# justin1 = user_query('27260086', '2012-06-13', '2012-06-29', csv=True, output='../../data/raw/justin/justin1.csv')
# justin2 = user_query('27260086', '2015-11-11', '2015-11-27', csv=True, output='../../data/raw/justin/justin2.csv')
# justin3 = user_query('27260086', '2020-02-12', '2020-02-28', csv=True, output='../../data/raw/justin/justin3.csv')

# be = tweets_query('#bts', '2020-11-30', '2020-12-04', csv=True, output='../../data/raw/be1.csv')

# dw = tweets_query('#btsdarkandwild', '2014-08-17', '2014-09-02', csv=True, output='../../data/raw/bts/dark_wild1.csv')
# love = tweets_query('#love_yourself', '2018-05-16', '2018-06-1', csv=True, output='../../data/raw/bts/love1.csv')
# be = tweets_query('#bts_be', '2020-11-18', '2020-12-04', csv=True, output='../../data/raw/bts/be1.csv')