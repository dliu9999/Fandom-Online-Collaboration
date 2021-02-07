import pandas as pd
import numpy as np

#api for data
import pageviewapi

def query_per_article(page, start, end, interval = 'daily'):
    '''
    Query Wikipedia page view data from English Wikipedia
    for a specific page between given dates
    
    :param page: specific Wikipedia page to query
    :param start: start date in yyyy-mm-dd format, cannot be prior to 2015-07-01
    :param end: end date in yyyy-mm-dd format, cannot be prior to 2015-07-01
    :param interval: date interval such as daily, monthly, etc.
    
    :return: DataFrame listing page views for a single article within a specific timeframe
    '''
    raw_page = pageviewapi.per_article('en.wikipedia', page, start,
                                        end, granularity = interval)
    
    page_views = raw_page.items()
    page_views = list(page_views)[0][1]
    page_views = pd.DataFrame.from_dict(page_views)
    page_views = page_views[['article', 'timestamp', 'views']]

    page_views['timestamp'] = page_views['timestamp']\
        .apply(lambda x: x[:4] + '-' + x[4:6] + '-' + x[6:8])

    page_views['article'] = page_views['article']\
        .apply(lambda y: y.replace('_', ' '))
    
    return page_views