from collections import defaultdict
from sklearn.feature_extraction.text import TfidfTransformer, CountVectorizer

class TFIDF:
    '''
    TFIDF instance, use sklearn package
    '''
    def __init__(self, raw_doc):
        '''
        Params: 3-d array [[[], []], [[], []]]
        '''
        doc = []
        for field in raw_doc:
            doc.append(' '.join([ pl for post in field for pl in post])) # flatten and to string

        vectorizer  = CountVectorizer(min_df=1, token_pattern=r'[\w\+\.#-]+')  # 該類會將文本中的詞語轉換為詞頻矩陣，矩陣元素a[i][j] 表示j詞在i類文本下的詞頻  
        transformer = TfidfTransformer()                                       # 該類會統計每個詞語的tf-idf權值  
        tfidf = transformer.fit_transform(vectorizer.fit_transform(doc))       # 第一個fit_transform是計算tf-idf，第二個fit_transform是將文本轉為詞頻矩陣  

        words  = vectorizer.get_feature_names()                                # 獲取詞袋模型中的所有詞語  
        weight = tfidf.toarray()                                               # 將tf-idf矩陣抽取出來，元素a[i][j]表示j詞在i類文本中的tf-idf權重  

        tfidf_score = defaultdict(lambda: defaultdict())
        for i in range(len(weight)):                                           # 打印每類文本的tf-idf詞語權重，第一個for遍歷所有文本，第二個for便利某一類文本下的詞語權重  
            for j in range(len(words)):
                tfidf_score[i][words[j]] = weight[i][j]

        self.tfidf_dict = tfidf_score
        self.tfidf_list = tfidf_score.items()
        self.words = words
               
    
    def get_tfidf(self):
        '''
        Returns:
        - tfidf_dict: dict[field_index[pl]] = score
        - words: all words in tfidf_score
        '''
        return self.tfidf_dict, self.words
    

    def predict_field(self, post):
        '''
        Params: ['pl_A', 'pl_B', 'pl_C']

        Returns: predicted field index
        '''
        scores = []
        for field, score_table in self.tfidf_list:
            scores.append((field, sum([score_table[pl] for pl in post if pl in self.words])))

        try:
            return max(scores, key=lambda x: x[1])[0]
        except:
            return 0 # Unknown to return field: 0

# ### How to use

# doc = [
#     [
#         ['pl', 'abc'],
#         ['a', 'b']
#     ],
#     [
#         ['c','d']
#     ]
# ]
# post = ['a']

# Predict = TFIDF(doc)
# tfidf_scores, words = Predict.get_tfidf()
# predict_field = Predict.predict_field(post)
# predict_field
