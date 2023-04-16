import pandas as pd
import urllib
from catboost import CatBoostClassifier
from tqdm import tqdm
import tldextract
import numpy as np

global df

def cal_len_util(str):
    try:
        return len(str)
    except:
        return 0

def cal_len(df, col):
    df[f'{col}_length']=df[col].apply(cal_len_util)

def qty_dot(df, col):
    df[f'qty_dot_{col}'] = df[[col]].applymap(lambda x: str.count(x, '.'))

def qty_hyphen(df, col):
    df[f'qty_hyphen_{col}'] = df[[col]].applymap(lambda x: str.count(x, '-'))

def qty_slash(df, col):
    df[f'qty_slash_{col}'] = df[[col]].applymap(lambda x: str.count(x, '/'))
    
def qty_questionmark(df, col):
    df[f'qty_questionmark_{col}'] = df[[col]].applymap(lambda x: str.count(x, '?'))

def qty_equal(df, col):
    df[f'qty_equal_{col}'] = df[[col]].applymap(lambda x: str.count(x, '='))

def qty_at(df, col):
    df[f'qty_at_{col}'] = df[[col]].applymap(lambda x: str.count(x, '@'))
    
def qty_and(df, col):
    df[f'qty_and_{col}'] = df[[col]].applymap(lambda x: str.count(x, '&'))
    
def qty_exclamation(df, col):
    df[f'qty_exclamation_{col}'] = df[[col]].applymap(lambda x: str.count(x, '&'))

def qty_space(df, col):
    df[f'qty_space_{col}'] = df[[col]].applymap(lambda x: str.count(x, ' '))
    
def qty_tilde(df, col):
    df[f'qty_tilde_{col}'] = df[[col]].applymap(lambda x: str.count(x, '~'))

def qty_comma(df, col):
    df[f'qty_comma_{col}'] = df[[col]].applymap(lambda x: str.count(x, ','))
    
def qty_plus(df, col):
    df[f'qty_plus_{col}'] = df[[col]].applymap(lambda x: str.count(x, '+'))

def qty_asterisk(df, col):
    df[f'qty_asterisk_{col}'] = df[[col]].applymap(lambda x: str.count(x, '*'))
    
def qty_hashtag(df, col):
    df[f'qty_hashtag_{col}'] = df[[col]].applymap(lambda x: str.count(x, '#'))
    
def qty_dollar(df, col):
    df[f'qty_dollar_{col}'] = df[[col]].applymap(lambda x: str.count(x, '$'))
    
def qty_percent(df, col):
    df[f'qty_percent_{col}'] = df[[col]].applymap(lambda x: str.count(x, '%'))
def isHttp(url):
  if 'http' in url or 'https' in url:
    return 1
  return 0

from urllib.parse import urlparse
def get_path(url):
  try:
    path = urlparse(url).path
    path = path.strip()
    if path == "":
      return np.NaN
    return path
  except:
    return np.NaN

def get_query(url):
    try:
        path = urlparse(url).query
        path = path.strip()
        if path == "":
            return np.NaN
        return path
    except:
        return np.NaN

def get_fragment(url):
    try:
        path = urlparse(url).fragment
        path = path.strip()
        if path == "":
            return np.NaN
        return path
    except:
        return np.NaN
import string
import math
def entropy(url):
    try:
        url = url.strip()
        prob = [float(url.count(c)) / len(url) for c in dict.fromkeys(list(url))]
        entropy = sum([(p * math.log(p) / math.log(2.0)) for p in prob])
        return entropy
    except:
        return 0

def get_features(df, urls):
    
        
    df['isHttp'] = df['url'].apply(isHttp)
    
    domains = []
    subdomains = []
    suffixs = []

    for url in urls:
        ext = tldextract.extract(url)
        domain, subdomain, suffix = ext.domain, ext.subdomain, ext.suffix
        domain = domain.strip()
        subdomain = subdomain.strip()
        suffix = suffix.strip()

        if domain == "":
            domain = np.NaN
        if subdomain == "":
            subdomain = np.NaN
        if suffix == "":
            suffix = np.NaN
        domains.append(domain)
        subdomains.append(subdomain)
        suffixs.append(suffix)
    
    df['domain'] = domains
    df['subdomain'] = subdomains
    df['suffix'] = suffixs
    df['path'] = df['url'].apply(get_path)
    df['query'] = df['url'].apply(get_query)
    df['fragment'] = df['url'].apply(get_fragment)
    
    needed_cols = ['url', 'domain', 'path', 'query', 'fragment']
    for col in needed_cols:
        df[f'{col}_length']=df[col].apply(cal_len_util)
        df[f'qty_dot_{col}'] = df[[col]].applymap(lambda x: str.count(str(x), '.'))
        df[f'qty_hyphen_{col}'] = df[[col]].applymap(lambda x: str.count(str(x), '-'))
        df[f'qty_slash_{col}'] = df[[col]].applymap(lambda x: str.count(str(x), '/'))
        df[f'qty_questionmark_{col}'] = df[[col]].applymap(lambda x: str.count(str(x), '?'))
        df[f'qty_equal_{col}'] = df[[col]].applymap(lambda x: str.count(str(x), '='))
        df[f'qty_at_{col}'] = df[[col]].applymap(lambda x: str.count(str(x), '@'))
        df[f'qty_and_{col}'] = df[[col]].applymap(lambda x: str.count(str(x), '&'))
        df[f'qty_exclamation_{col}'] = df[[col]].applymap(lambda x: str.count(str(x), '!'))
        df[f'qty_space_{col}'] = df[[col]].applymap(lambda x: str.count(str(x), ' '))
        df[f'qty_tilde_{col}'] = df[[col]].applymap(lambda x: str.count(str(x), '~'))
        df[f'qty_comma_{col}'] = df[[col]].applymap(lambda x: str.count(str(x), ','))
        df[f'qty_plus_{col}'] = df[[col]].applymap(lambda x: str.count(str(x), '+'))
        df[f'qty_asterisk_{col}'] = df[[col]].applymap(lambda x: str.count(str(x), '*'))
        df[f'qty_hashtag_{col}'] = df[[col]].applymap(lambda x: str.count(str(x), '#'))
        df[f'qty_dollar_{col}'] = df[[col]].applymap(lambda x: str.count(str(x), '$'))
        df[f'qty_percent_{col}'] = df[[col]].applymap(lambda x: str.count(str(x), '%'))
    
    needed_cols = ['url', 'domain', 'path', 'query', 'fragment']
    for col in needed_cols:
        df[f'entropy_{col}'] = df[col].apply(entropy)
    
   
        

def process_urls(url_list):
    _len = len(url_list)
    df = pd.DataFrame(columns = ['url', 'label'])
    df['url'] = url_list
    df['label'] = [0 for _ in range(_len)]
    # print(url_list)
    df['protocol'],df['domain'],df['path'],df['query'],df['fragment'] = zip(*[urllib.parse.urlsplit(x) for x in url_list])
    get_features(df, url_list)
    columns = ['isHttp',
 'url_length',
 'qty_dot_url',
 'qty_hyphen_url',
 'qty_slash_url',
 'qty_questionmark_url',
 'qty_equal_url',
 'qty_at_url',
 'qty_and_url',
 'qty_exclamation_url',
 'qty_space_url',
 'qty_tilde_url',
 'qty_comma_url',
 'qty_plus_url',
 'qty_asterisk_url',
 'qty_hashtag_url',
 'qty_dollar_url',
 'qty_percent_url',
 'domain_length',
 'qty_dot_domain',
 'qty_hyphen_domain',
 'qty_slash_domain',
 'qty_questionmark_domain',
 'qty_equal_domain',
 'qty_at_domain',
 'qty_and_domain',
 'qty_exclamation_domain',
 'qty_space_domain',
 'qty_tilde_domain',
 'qty_comma_domain',
 'qty_plus_domain',
 'qty_asterisk_domain',
 'qty_hashtag_domain',
 'qty_dollar_domain',
 'qty_percent_domain',
 'path_length',
 'qty_dot_path',
 'qty_hyphen_path',
 'qty_slash_path',
 'qty_questionmark_path',
 'qty_equal_path',
 'qty_at_path',
 'qty_and_path',
 'qty_exclamation_path',
 'qty_space_path',
 'qty_tilde_path',
 'qty_comma_path',
 'qty_plus_path',
 'qty_asterisk_path',
 'qty_hashtag_path',
 'qty_dollar_path',
 'qty_percent_path',
 'query_length',
 'qty_dot_query',
 'qty_hyphen_query',
 'qty_slash_query',
 'qty_questionmark_query',
 'qty_equal_query',
 'qty_at_query',
 'qty_and_query',
 'qty_exclamation_query',
 'qty_space_query',
 'qty_tilde_query',
 'qty_comma_query',
 'qty_plus_query',
 'qty_asterisk_query',
 'qty_hashtag_query',
 'qty_dollar_query',
 'qty_percent_query',
 'fragment_length',
 'qty_dot_fragment',
 'qty_hyphen_fragment',
 'qty_slash_fragment',
 'qty_questionmark_fragment',
 'qty_equal_fragment',
 'qty_at_fragment',
 'qty_and_fragment',
 'qty_exclamation_fragment',
 'qty_space_fragment',
 'qty_tilde_fragment',
 'qty_comma_fragment',
 'qty_plus_fragment',
 'qty_asterisk_fragment',
 'qty_hashtag_fragment',
 'qty_dollar_fragment',
 'qty_percent_fragment',
 'entropy_url',
 'entropy_domain',
 'entropy_path',
 'entropy_query',
 'entropy_fragment']
    # X = df.drop(columns=['url', 'subdomain', 'suffix', 'domain', 'path', 'query', 'fragment','label'])
    X = df[columns]
    
    return X

def get_predict(X):
    cat_model = CatBoostClassifier()
    cat_model.load_model('./catboost_4')
    return cat_model.predict_proba(X)

# test_df = pd.read_csv('./public_test.csv')
# urls = test_df.x.tolist()
# print(urls)
# res = process_urls(['https://www.youtube.com/watch?v=t1T8CplP72w'])

# print(get_predict(res))