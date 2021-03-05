#to turn raw data into features for modeling
import pandas as pd
#import wikipedia
import sys

sys.path.insert(0, 'src/data')
from make_dataset import *


##### For Wikipedia #####

#find out whether users who contributed in a Wikipedia article are kpop fans or not

def find_contributions(user):
    '''
    Given a username, 
    find all their contributions on Wikipedia

    :param user: user's username
    :return: user contributions on Wikipedia
    '''
    site = Site('en', 'wikipedia')  # The site we want to run our bot on
    user = User(site, user)

    contrib = []
    for page, oldid, ts, comment in user.contributions():
        # for each edit, yields (pywikibot.Page, oldid, pywikibot.Timestamp, comment)
        contrib.append(page.title() + " ^^^ " + comment)
        
    return contrib


def find_users(fp, article_name):
    '''
    Given a light dump file and an article name, 
    find unique list of users who contributed

    :param fp: lightdump input filepath
    :param article_name: wiki article name
    :return: list of unique users
    '''

    # find usernames from ld
    with open(fp) as f:
        content = f.readlines()

    users = {}

    for line in content:
        line = line.strip()

        if line[:4] != "^^^_":  # line is title
            title = line
            users[title] = []
        else:  # line is revision
            users[title].append(line.split(" ")[3])        

    lst = users[article_name]
    return [i for n, i in enumerate(lst) if i not in lst[:n]] 


def user_contributions(fp, article_name):
    '''
    Finds contributions of users

    :param fp: lightdump input filepath
    :param article_name: wiki article name
    :return: contributions of users
    '''
    users = find_users(fp, article_name)
    contributions = {}
    for user in users:
        try:
            contributions[user] = find_contributions(user)
        except:
            continue
    return contributions


def build_df(data):
    '''
    Given user contribution data, build a user contibution dataframe

    :param data: user contribution data
    :return: user contribution dataframe
    '''
    d = []
    user = data.keys()
    for user in data.keys():
        total_contrib = len(data[user])
        for page in data[user]:
            # clean page title
            page = str(re.findall('^[^\^^^]+', page)[0][:-1])
            d.append([user, total_contrib, page])
            
    df = pd.DataFrame(d, columns = ['users', 'total_edits', 'article_name'])
    return df


def find_related(article_name, n):
    '''
    Given an article name, 
    returns n most related articles

    :param article_name: wiki article name
    :param n: number of articles to return
    :return: n most related articles
    '''
    articles = []
    articles.append(article_name)
    results = wikipedia.search(article_name, results = n)
    articles += results
    return articles


def kpop_fan(user, df):
    '''
    Given a username and dataframe of user contributions,
    determines whether a user is a kpop fan or not

    :param user: user username
    :param df: user contributions 
    :return: whether user is a kpop fan or not
    '''
    u = df[df.users == user].groupby(['users', 'article_name']).count()
    tmp = u.sort_values(by='total_edits', ascending = False)
    # get articles that they contributed in
    total_articles = [article_name for (user, article_name) in tmp.index]
    articles = [x for x in total_articles if x in related]
    # get percentage of kpop contributions
    if len(articles) / len(total_articles) > 0.1:
        return 1
    else:
        return 0
    
    
def percentage_fans(fp, article_name, search_related):
    '''
    Given an article revision history,
    gets percentage of fans from its users.

    :param fp: input filepath
    :param article_name: wiki article name
    :param search_related: related article names
    :return: percentage of k-pop fans
    '''
    # transform data into dataframe format
    data = user_contributions(fp, article_name)
    df = build_df(data)

    # get all related article titles
    related = []
    for query in search_related:
        related += find_related(query, n=500)

    # analyze each user
    unique_users = df.users.unique()
    fans = [user for user in unique_users if kpop_fan(user,df) == 1 ]
    df['fan'] = df.users.apply(lambda x: 1 if x in fans else 0)

    # get percentage of fans
    return len(fans) / len(unique_users)


def calculate_M(edits):
    '''
    Calculates the M stat for a single article
    :param edits: edits
    :return: M stat 
    '''
    edits = edits.values.tolist()
    edits.reverse()
    
    # cannot have edit war with 2 edits
    if len(edits) <= 2:
        return 0
    
    # cannot have edit war with less than 2 reverts
    try:
        num_reverts = sum([int(x[1]) for x in edits])
        if num_reverts < 2:
            return 0
    except:
        pass # bad data
    
    # M STAT: find revert pairs
    revert_pairs = []

    for lst in edits:
        if len(lst) < 4: # skip bad data
            continue
        
        if lst[1]=='1':  # is a revert
            user_one = lst[3]
            org_idx = int(lst[2])-1
            try:
                user_two = edits[org_idx][3]
            except:
                continue
            
            # exclude self revert
            if user_one == user_two:
                continue
            
            if (user_one, user_two) not in revert_pairs:
                revert_pairs.append((user_one, user_two))

    # M STAT: find mutual reverts
    mutual_rev_users = []
    mutual_rev_pairs = []
    for pair in revert_pairs:
        one = pair[0]
        two = pair[1]

        #mutual revert found
        if (two, one) in revert_pairs:
            mutual_rev_pairs.append((one, two))
            mutual_rev_users.append(two)
            mutual_rev_users.append(one)

    # remove duplicates, calculate num
    E = len(list(set(mutual_rev_users)))

    if E == 0:
        return 0
    
    # get num edits per user
    users = [x[3] for x in edits if len(x) == 4]
    user_edits = dict((x,users.count(x)) for x in set(users))
    
    # calculate M
    M = 0
    
    for pair in list(set(mutual_rev_pairs)):
        one = pair[0]
        two = pair[1]
        if user_edits[one] < user_edits[two]:
            N = user_edits[one]
        else:
            N = user_edits[two]

        M += N
    
    M *= E
    return M


def summary_stats(files):
    '''
    Create a row of stats for a given article

    :param files: lightdump files
    '''
    summary = pd.DataFrame([], columns = ['title', 
                                      'M', 
                                      'num_edits', 
                                      'num_reverts', 
                                      'num_users', 
                                      'avg_edits_per_user',
                                      'num_bots', 
                                      'bot_edits', 
                                      'bot_reverts'
                                     ])
    for fp in files:
        title, df = read_lightdump(fp)
        data = [title]
        data.append(calculate_M(df))
        data.append(df.shape[0])
        data.append(df.revert.sum())
        unique_users = df.user.str.lower().unique()
        data.append(len(unique_users))
        data.append(df.groupby('user').count().revert.mean())
        data.append(len([x for x in unique_users if 'bot' in x]))
        df['bots'] = df.user.apply(lambda x: 1 if 'bot' in x else 0)
        data.append(df[df.bots == 1].shape[0])
        data.append(df[(df.revert == 1)&(df.bots == 1)].shape[0])
        data = pd.Series(data, index = summary.columns)
        summary = summary.append(data, ignore_index = True)
    summary['revert/edit'] = summary.num_reverts / summary.num_edits
    summary['bot/users'] = summary.num_bots / summary.num_users
    return summary

def wiki_summary_stats(wiki_fp, outdir):
    '''
    Generate wiki summary stats

    :param wiki_fp: input wiki fp
    :param outdir: output filepath for csv
    '''
    wiki_ld = os.listdir(wiki_fp)
    wiki_ld.sort()
    files = []
    
    for dump in wiki_ld:
        fp = os.path.join(wiki_fp, dump)
        files.append(fp)
    df = summary_stats(files)
    df.to_csv(os.path.join(outdir, 'wiki_summary_stats.csv'))
    
##### For Google Trends #####

def trends_summary_stats(trends_fp, outdir):
    '''
    Generate Google Trends summary stats
    
    :param trends_fp: input Google Trends fp
    :param outdir: output filepath for csv
    '''
    
    trend_csvs = os.listdir(trends_fp)
    
    for csv in trend_csvs:
        df = pd.read_csv(os.path.join(trends_fp, csv))
        
        summary = df.groupby('Artist').agg({'Popularity': ['mean', 'median',
                                                 pd.Series.mode, 'count',
                                                 'max', 'min', 'std',
                                                 'var', 'skew', pd.DataFrame.kurt]})
        
        start = str(df['date'].min())[:10]
        end = str(df['date'].max())[10:]
        
        file_name = 'google_trend_summary_stats_'+ start + '_' + end + '.csv'
        df.to_csv(os.path.join(outdir, file_name))
