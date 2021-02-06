#creating explanatory and results oriented visualizations
import pandas as pd
import sys

sys.path.insert(0, 'src/data')

# from make_dataset import *
from etl import *

def normalize_dates(df, release_date, start=-2, end=10):
    '''
    Normalizes dates to release date, only keeping "start" days
    before to "end" days after. Returns a copy.
    '''
    df = df.copy()
    df['date'] = pd.to_datetime(df['date'])
    date_diff = (pd.Timestamp(release_date) - df['date'].min())
    normalized_dates = (pd.factorize(df['date'], sort=True)[0] - date_diff.days).astype(object)
    
    # remove out of scope
    normalized_dates[(normalized_dates > end) | (normalized_dates < start)] = np.NaN
    df['normalized_dates'] = normalized_dates
    return df.dropna(subset=['normalized_dates'])

def plot_albums(title, *album_tups):
    '''
    Plots multiple albums as a single overlayed line plot with
    normalized dates
    '''
    assert len(album_tups) > 1, 'passed in only one album'
    assert len(album_tups[0]) == 2, 'need to pass in both album and legend name'
    assert all(['normalized_dates' in album.columns for album, leg in album_tups])
    
    legend = []
    album, leg = album_tups[0]
    legend.append(leg)
    ax = album.groupby('normalized_dates').size().plot(figsize=(10,7), title=title)
    for album_tup in album_tups[1:]:
        album, leg = album_tup
        legend.append(leg)
        album.groupby('normalized_dates').size().plot(ax=ax)
        
    # release date line
    mean_counts = album.normalized_dates.value_counts().mean()
    ax.annotate('Album Release', xy = (0, np.mean([0, mean_counts])), color='purple', alpha = 0.5)
    ax.axvline(0, color='purple', alpha=0.5)
    
    # legend
    ax.legend(legend)

    