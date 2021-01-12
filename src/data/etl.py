# Transforms XML data into more useful formats

import pandas as pd
import numpy as np
import os
from bs4 import BeautifulSoup

#Converting XML to Light Dump
def xml_to_soup(fp):
    '''
    Processes xml data using beautiful soup and
    returns list of data for each page
    '''
    content = []
    with open(fp, encoding = 'utf8') as file:

        content = file.readlines()
        content = "".join(content)
        soup = BeautifulSoup(content, "xml")
        
    pages = soup.findAll("page")
    return pages

def soup_to_df(pages):
    '''
    Converts soupified xml data for Wiki pages 
    into dataframe
    
    pages: list of xml data for each page
    '''
    data = {}
    for page in pages:
        title = page.title.text
        revisions = page.findAll("revision")

        for revision in revisions:
            r_id = revision.id.text 
            time = revision.timestamp.text
            try:
                try:
                    username = revision.contributor.username.text
                except: 
                    username = revision.contributor.ip.text
            except:
                username = 'N/A'
            text = revision.format.next_sibling.next_sibling.text
            if title in data:
                data[title].append([title, r_id, time, username, text])
            else:
                data[title] = [[title, r_id, time, username, text]]
    
    dframes = []
    for page in data:

        df = pd.DataFrame(data[page], columns = ['title', 'id', 'time', 'username', 'text'])

        hist = [] #history of text
        version = [] #edit version
        username = []
        revert = [] #0 or 1
        curr = 1 #to keep track of version

        for idx, row in df.iterrows():
            if row.text not in hist: # not a revert
                hist.append(row.text)
                version.append(curr)
                username.append(row.username)
                revert.append('0')
                curr += 1
            else: #is revert
                temp = hist.index(row.text)
                version.append(version[temp])
                username.append(row.username)

                #if self revert
                if row.username == username[version[temp]]:
                    revert.append('0')
                else:
                    revert.append('1')


        df['version'] = version
        df['revert'] = revert
        dframes.append(df)

    return dframes

def df_to_ld(dframes, outpath):
    '''
    Given a list of cleaned dataframes from xml data,
    produces light dump file into data/raw
    '''
    
    light_dump = ''
    for df in dframes:
        title = df.title[0]
        light_dump = light_dump + title + '\n'
        for idx, row in df.iterrows():
            line = '^^^_' + row.time + ' ' + row.revert + ' ' + str(row.version) + ' ' + row.username
            light_dump = light_dump + line + '\n'
    with open(outpath, 'w') as f:
        f.write(light_dump)
    repo = 'XML Converted to light dump at ' + outpath
    print(repo)
    
    return

def xml_to_light_dump(fp, outfp):
    '''
    Given an input file path and output path, 
    turns the xml file into a light dump 
    and stores it at the output file path
    '''
    #create light dump directory first
    if not os.path.isdir("data/raw/light_dump"):
        os.mkdir("data/raw/light_dump")
    
    #convert to light dump
    soup = xml_to_soup(fp)
    dframes = soup_to_df(soup)
    return df_to_ld(dframes, outfp)


# Store revision content in separate txt files
def soup_to_df_with_content(pages):
    '''
    Converts soupified xml data for Wiki pages 
    into dataframe
    
    pages: list of xml data for each page
    '''
    data = {}
    for page in pages:
        title = page.title.text
        revisions = page.findAll("revision")

        for revision in revisions:
            r_id = revision.id.text 
            time = revision.timestamp.text
            try:
                try:
                    username = revision.contributor.username.text
                except: 
                    username = revision.contributor.ip.text
            except:
                username = 'N/A'
            text = revision.format.next_sibling.next_sibling.text
            if title in data:
                data[title].append([title, r_id, time, username, text])
            else:
                data[title] = [[title, r_id, time, username, text]]
    
    dframes = []
    for page in data:

        df = pd.DataFrame(data[page], columns = ['title', 'id', 'time', 'username', 'text'])

        hist = [] #history of text
        version = [] #edit version
        username = []
        revert = [] #0 or 1
        curr = 1 #to keep track of version

        for idx, row in df.iterrows():
            if row.text not in hist: # not a revert
                hist.append(row.text)
                version.append(curr)
                username.append(row.username)
                revert.append('0')
                curr += 1
            else: #is revert
                temp = hist.index(row.text)
                version.append(version[temp])
                username.append(row.username)

                #if self revert
                if row.username == username[version[temp]]:
                    revert.append('0')
                else:
                    revert.append('1')


        df['version'] = version
        df['revert'] = revert
        df['text'] = text
        dframes.append(df)

    return dframes


def df_to_content(dframes, outpath):
    '''
    Given a list of cleaned dataframes from xml data,
    produces content file into data/raw
    '''
    
    content = ''
    for df in dframes:
        title = df.title[0]
        content = content + title + '\n'
        for idx, row in df.iterrows():
            line = '^^^_' + str(row.version) + ' ' + row.username + '\n' + row.text
            content = content + line + '\n'
    with open(outpath, 'w') as f:
        f.write(content)
    repo = 'XML Converted to content at ' + outpath
    print(repo)
    
    return

def store_xml_content(fp, outfp):
    '''
    Given an input file path and output path, 
    stores the revision content in the xml file
    at the output file path
    '''
    #create content directory first
    if not os.path.isdir("data/raw/content"):
        os.mkdir("data/raw/content")
    
    #convert to light dump
    soup = xml_to_soup(fp)
    dframes = soup_to_df_with_content(soup)
    return df_to_content(dframes, outfp)