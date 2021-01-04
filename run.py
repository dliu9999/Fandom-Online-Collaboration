#!/usr/bin/env python

import sys
import json

sys.path.insert(0, 'src/data')
sys.path.insert(0, 'src/features')
sys.path.insert(0, 'src/visualization')

from make_dataset import *
from build_features import *
from visualize import *

def main(targets):
    sql_config = json.load(open('config/data-db-params.json'))
    eda_config = json.load(open('config/eda-params.json'))
    all_config = json.load(open('config/all-params.json'))
    test_config = json.load(open('config/test-params.json'))
        
    if 'data-db' in targets:
        pass
        
    if 'eda' in targets:
        pass
        
    if 'all' in targets:
        pass
        
    if 'test' in targets:
        pass
        
    else:
        print('You did not pass in any arguments!')

if __name__ == '__main__':
    # run via:
    # python main.py data model
    targets = sys.argv[1:]
    main(targets)
