import pandas as pd
import numpy as np

#apis for data
from pytrends.request import TrendReq

default_list = ["BTS", "Girls' Generation", "BLACKPINK", "Taylor Swift", "Justin Bieber"]

def query_trends(term_list = default_list,
                 category = None, dates = 'all'):
    '''
    Query Google Trends data with search terms between
    given dates
    
    :param term_list: list of terms to search
    :param category: optional Google Trends category
    :param dates: start and end dates of query search in 'yyyy-mm-dd yyyy-mm-dd' format
    
    :return: DataFrame with Google Trends popularity for the search terms in the given timeframe
    '''
    pytrends = TrendReq()
    
    pytrends.build_payload(kw_list = term_list,
                           timeframe = dates)
    
    df = pytrends.interest_over_time()
    
    df.drop('isPartial', inplace = True, axis = 1)
    df.reset_index(inplace = True)
    
    df = df.melt(id_vars = ['date'],
                var_name = 'artist',
                value_name = 'popularity')
    
    return df