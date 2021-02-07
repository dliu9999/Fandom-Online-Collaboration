#creating explanatory and results oriented visualizations
import pandas as pd
import seaborn as sns
import sys

sys.path.insert(0, 'src/data')

# from make_dataset import *
from etl import *
from trends import *
from pageviews import *

#visualize Wikipedia activity before / after album releases
def date_range(release_date):
    '''
    Given a string with the album release date,
    calculates the given time range to extract data from
    '''
    date = pd.to_datetime(release_date)
    start = date - timedelta(days=2)
    end = date + timedelta(days = 14)
    return start, end
    
    
def visualize_album_activity(fp, release_dates):
    '''
    Visualizes Wikipedia activity after album releases
    '''
    titles, dfs = lightdump_read_n(fp, 5)
    d = list(zip(titles, dfs))
    for [title, df] in d:
        release_date = release_dates[title]
        start, end = date_range(release_date)

        df.timestamp = pd.DatetimeIndex(pd.to_datetime(df.timestamp)).tz_localize(None)
        filtered = df[(df.timestamp > start) & (df.timestamp < end)]
        filtered = filtered.sort_values(by = 'timestamp', ascending = True)
        filtered.timestamp = filtered.timestamp.apply(lambda x: x.date())
        data = filtered.groupby(by = 'timestamp').count()

        if data.shape[0] == 0:
            data = pd.DataFrame()
            data['timestamp'] = pd.date_range(start= start, end = end)
            data.timestamp = pd.to_datetime(data.timestamp)
            data['user'] = [0 for i in range(len(data.timestamp))]
            data = data.set_index('timestamp')

        display(data)
        data[["user"]].plot()
        plt.ylabel('number of revisions')
        plt.xlabel('date')
        plt.xticks(rotation=45, ha="right")
        plt.title(title + ' Album\'s Wikipedia Revision Activity')

        x = release_date
        ax.annotate('Album Release', xy = (x ,5), color='purple', alpha = 0.5)
        ax.axvline(x, color='purple', alpha=0.5)

        plt.savefig("data/eda/album_" + title + "wiki_activity.png")
        
        
def visualize_google_trends(fp, outdir):
    '''
    Visualize Google Trends data with search terms between
    given dates
    
    :param fp: file path to directory with data
    :param outdir: file path to directory where to save the plot
    '''
    trend_csvs = os.listdir(fp)
    
    for csv in trend_csvs:
        df = pd.read_csv(os.path.join(fp, csv))
        
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
        
        plt.savefig('data/eda/' + file_name)
        
        
def visualize_pageviews(fp, outdir):
    '''
    Visualize Wikipedia page view data
    
    :param fp: file path to directory with data
    :param outdir: file path to directory where to save the plot
    '''
    trend_csvs = os.listdir(fp)
    
    for csv in trend_csvs:
        df = pd.read_csv(os.path.join(fp, csv))
        
        start = str(df['timestamp'].min())[:10]
        end = str(df['timestamp'].max())[10:]
        
        title_text = 'Wikipedia Page Views: '+ start + ' to ' +\
                end + ')'
        
        file_name = 'Wikipedia Page Views'+ start + ' ' + end + '.png'
        
        #plotting
        g = sns.lineplot(data = df, x = 'timestamp', y = 'views',
                 hue = 'article', dashes = False)
        
        g.set_title(title_text)
        g.set(xlabel = 'Date', ylabel = Views)
        
        plt.savefig('data/eda/' + file_name)