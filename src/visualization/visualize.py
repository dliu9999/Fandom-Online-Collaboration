#creating explanatory and results oriented visualizations
import pandas as pd
import sys
import os

sys.path.insert(0, 'src/data')

from make_dataset import *

def plot_albums(title, outdir, *album_tups):
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
    ax.figure.savefig(os.path.join(outdir, title + '.png'))

def generate_twitter_plot(tweets_fp, tweets_release_dates, tweets_legend, outdir):
    '''
    Generate twitter overlaid plot
    '''
    tweet_csvs = os.listdir(tweets_fp)
    dfs = []

    # normalize dates
    for csv, date in zip(tweet_csvs, tweets_release_dates):
        df = pd.read_csv(os.path.join(tweets_fp, csv))
        dfs.append(normalize_dates(df, date))
    # plot overlaid line chart
    tweet_tup = tuple(zip(dfs, tweets_legend))
    plot_albums('Tweet Plots', outdir, *tweet_tup)