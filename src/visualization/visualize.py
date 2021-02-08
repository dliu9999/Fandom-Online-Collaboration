#creating explanatory and results oriented visualizations
import sys
import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

sys.path.insert(0, 'src/data')

from make_dataset import *

def plot_albums(title, outdir, *album_tups):
    '''
    Plots multiple albums as a single overlayed line plot with
    normalized dates

    :param title: Title of overlaid plot
    :outdir: output filepath for plot
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
    ax.clear()

def generate_twitter_plot(tweets_fp, tweets_release_dates, tweets_legend, outdir):
    '''
    Generate twitter overlaid plot

    :param tweets_fp: file path to directory with data
    :param tweets_release_dates: album release dates for each plot
    :param tweets_legend: legend names for overlaid plot
    :param outdir: output filepath for plot
    '''
    tweet_csvs = os.listdir(tweets_fp)
    tweet_csvs.sort()
    dfs = []

    # normalize dates
    for csv, date in zip(tweet_csvs, tweets_release_dates):
        df = pd.read_csv(os.path.join(tweets_fp, csv))
        dfs.append(normalize_dates(df, date))
        
    # plot overlaid line chart
    tweet_tup = tuple(zip(dfs, tweets_legend))
    plot_albums('Tweet Plots', outdir, *tweet_tup)
    
    
##### For Wikipedia #####

def generate_wiki_plot(wiki_fp, wiki_release_dates, wiki_legend, outdir):
    '''
    Generate wiki overlaid plot

    :param wiki_fp: file path to directory with data
    :param wiki_release_dates: album release dates for each plot
    :param wiki_legend: legend names for overlaid plot
    :param outdir: output filepath for plot
    '''
    wiki_ld = os.listdir(wiki_fp)
    wiki_ld.sort()
    dfs = []

    # normalize dates
    for dump, date in zip(wiki_ld, wiki_release_dates):
        fp = os.path.join(wiki_fp, dump)
        title, df = read_lightdump(fp)
        dfs.append(normalize_dates(df, date))
        
    # plot overlaid line chart
    wiki_tup = tuple(zip(dfs, wiki_legend))
    plot_albums('Wiki Plots', outdir, *wiki_tup)

##### For Google Trends #####

def visualize_google_trends(trends_fp, outdir):
    '''
    Visualize Google Trends data with search terms between
    given dates
    
    :param trends_fp: file path to directory with data
    :param outdir: output filepath for plot
    '''
    trend_csvs = os.listdir(trends_fp)
    
    for csv in trend_csvs:
        df = pd.read_csv(os.path.join(trends_fp, csv))
        
        start = str(df['date'].min())[:10]
        end = str(df['date'].max())[10:]
        
        title_text = 'Google Search Trends: '+ start + ' to ' +\
                end + ')'
        
        file_name = 'Google Trend Plots'+ start + ' ' + end + '.png'
        
        #plotting
        g = sns.lineplot(data = df, x = 'date', y = 'Popularity',
                 hue = 'Artist', dashes = False)
        
        g.set_title(title_text)
        g.set(xlabel = 'Date')
        
        plt.savefig(os.path.join(outdir, file_name))
        

##### For Wikipedia Page Views #####

def visualize_pageviews(views_fp, outdir):
    '''
    Visualize Wikipedia page view data
    
    :param fp: file path to directory with data
    :param outdir: output filepath for plot
    '''
    trend_csvs = os.listdir(views_fp)
    
    for csv in trend_csvs:
        df = pd.read_csv(os.path.join(views_fp, csv))
        
        start = str(df['timestamp'].min())[:10]
        end = str(df['timestamp'].max())[10:]
        
        title_text = 'Wikipedia Page Views: '+ start + ' to ' +\
                end + ')'
        
        file_name = 'Wikipedia Page Views Plot'+ start + ' ' + end + '.png'
        
        #plotting
        g = sns.lineplot(data = df, x = 'timestamp', y = 'views',
                 hue = 'article', dashes = False)
        
        g.set_title(title_text)
        g.set(xlabel = 'Date', ylabel = 'Views')
        
        plt.savefig(os.path.join(outdir, file_name))
