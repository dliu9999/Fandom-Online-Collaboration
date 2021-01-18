#creating explanatory and results oriented visualizations
import pandas as pd
import sys

sys.path.insert(0, 'src/data')

# from make_dataset import *
from etl import *

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
    