
# coding: utf-8

# In[1]:

# Extract PL

from flashtext import KeywordProcessor

pls = open('steevebot/Rule.txt', 'r', encoding='utf8').read().split('\n')

keyword_processor = KeywordProcessor()
keyword_processor.add_keywords_from_list(pls)

def get_pl_keywords(content):
    return keyword_processor.extract_keywords(content)

def norm_pls(pls):
    '''
    Params: ['pl_A', 'pl_B', 'pl_C']
    
    Returns: list for normalized pls
    '''
    return [pl.lower().replace(' ', '_').replace('.js', '') for pl in pls]


# In[15]:

def pick_top_k(target_pls, dataset, k=100):
    '''
    Params:
    - target_pls (from user's pls or company requirement): ['pl_A', 'pl_B', 'pl_C']
    - dataset: every post's or candidate's pls [{id, pl}, {id, pl}, {id, pl}]
    - k: return top k jobs and must match at least one pl
    
    Return: Top k or 100 jobs id in suitable order
    '''
    matches = [len(set(target_pls).intersection(set(each['PL']))) for each in dataset]

    top = sorted(zip(dataset, matches), key=lambda pair: pair[1], reverse=True)
    top_k = filter(lambda pair: pair[1] > 0, top[:k])
    top_k = list(map(lambda pair: pair[0]['id'], top_k))
    return top_k


# In[17]:

# pick_top_k(['A','B','C'], [{'id': 1, 'PL': ['A','B']}, {'id': 12, 'PL': ['A','D']}, {'id': 3, 'PL': ['E']}])


# In[ ]:




# In[ ]:



