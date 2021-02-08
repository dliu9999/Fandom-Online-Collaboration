#!/usr/bin/env python

import sys
import os
import json

sys.path.insert(0, 'src/data')
sys.path.insert(0, 'src/features')
sys.path.insert(0, 'src/visualization')

from make_dataset import *
from build_features import *
from visualize import *

def main(targets):
    sql_config = json.load(open('config/data-db-params.json'))
    test_config = json.load(open('config/test-params.json'))
        
#     if 'data-db' in targets:
        
    if 'test' in targets:
        outdir = test_config['outdir']

        ### TWITTER ###
        tweets_fp = test_config['tweets_fp']
        tweets_release_dates = test_config['tweets_release_dates']
        tweets_legend = test_config['tweets_legend']
        generate_twitter_plot(tweets_fp, tweets_release_dates, tweets_legend, outdir)
        print('Generated twitter plots')
        
        
        ### WIKIPEDIA ###
        
        # Album Release
        wiki_fp = test_config['wiki_fp'][0]
        wiki_release_dates = test_config['wiki_release_dates']
        wiki_legend = test_config['wiki_legend']
        generate_wiki_plot(wiki_fp, wiki_release_dates, wiki_legend, outdir)
        
        # Summary Stats
        wiki_fp = test_config['wiki_fp'][1]
        wiki_summary_stats(wiki_fp, outdir)
        print('Generated wiki plots')
        
        
        
    else:
        print('You did not pass in any arguments!')

if __name__ == '__main__':
    # run via:
    # python main.py data model
    targets = sys.argv[1:]
    main(targets)
