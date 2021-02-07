#!/usr/bin/env python

import sys
import os
import json

sys.path.insert(0, 'src/data')
sys.path.insert(0, 'src/features')
sys.path.insert(0, 'src/visualization')

# from make_dataset import *
from make_dataset import *
from build_features import *
from visualize import *

def main(targets):
    sql_config = json.load(open('config/data-db-params.json'))
    test_config = json.load(open('config/test-params.json'))
        
    if 'data-db' in targets:
        for i in range(len(sql_config['xml_fp'])):
            #convert to light dump
            fp = sql_config['xml_fp'][i]
            outfp = sql_config['ld_outfp'][i]
            xml_to_light_dump(fp, outfp)
            
            #store content
            outfp = sql_config['content_outfp'][i]
            store_xml_content(fp, outfp)
        
    if 'test' in targets:
        outdir = test_config['outdir']

        ### Tweets ###
        tweets_fp = test_config['tweets_fp']
        tweets_release_dates = test_config['tweets_release_dates']
        tweets_legend = test_config['tweets_legend']
        generate_twitter_plot(tweets_fp, tweets_release_dates, tweets_legend, outdir)
        print('Generated twitter plot')
        
        
    else:
        print('You did not pass in any arguments!')

if __name__ == '__main__':
    # run via:
    # python main.py data model
    targets = sys.argv[1:]
    main(targets)
