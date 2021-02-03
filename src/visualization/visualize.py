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
    