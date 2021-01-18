#to turn raw data into features for modeling
import pandas as pd
import wikipedia


#find out whether users who contributed in a Wikipedia article are kpop fans or not

def find_contributions(user):
    '''
    Given a username, 
    find all their contributions on Wikipedia
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
    '''

    #find usernames from ld
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
    '''
    u = df[df.users == user].groupby(['users', 'article_name']).count()
    tmp = u.sort_values(by='total_edits', ascending = False)
    #get articles that they contributed in
    total_articles = [article_name for (user, article_name) in tmp.index]
    articles = [x for x in total_articles if x in related]
    #get percentage of kpop contributions
    if len(articles) / len(total_articles) > 0.1:
        return 1
    else:
        return 0
    
    
def percentage_fans(fp, article_name, search_related):
    '''
    Given an article revision history,
    gets percentage of fans from its users.
    '''
    #transform data into dataframe format
    data = user_contributions(fp, article_name)
    df = build_df(data)

    #get all related article titles
    related = []
    for query in search_related:
        related += find_related(query, n=500)

    #analyze each user
    unique_users = df.users.unique()
    fans = [user for user in unique_users if kpop_fan(user,df) == 1 ]
    df['fan'] = df.users.apply(lambda x: 1 if x in fans else 0)

    #get percentage of fans
    return len(fans) / len(unique_users)
    
