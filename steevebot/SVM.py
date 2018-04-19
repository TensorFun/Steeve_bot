
# coding: utf-8

# In[2]:

import numpy as np
from sklearn import feature_extraction, svm, metrics
from pyfasttext import FastText

import pickle 


class SVM:
    def __init__(self, TFIDF): # TODO: plz give me the model or using global singleton
        self.model = FastText('/home/yee0/Atos/wiki.en.bin')
        self.TFIDF = TFIDF
        self.tfidf_dict, self.words = TFIDF.get_tfidf()
    
    def set_tfidf(self, TFIDF):
        self.TFIDF = TFIDF
        self.tfidf_dict, self.words = TFIDF.get_tfidf()
    
    def to_feature(self, X):
        return [self.vec(self.TFIDF.predict_field(post), post) for post in X]
        
    def vec(self, field_index, post):
        v = np.zeros(300)
        post = set(post) # make unique
        for pl in post:
            if pl != '' and pl in self.words:
                v += self.model.get_numpy_vector(pl) * self.tfidf_dict[field_index][pl]
        return v
    
    def train(self, X, y):
        # 建立 SVC 模型
        self.svc = svm.SVC()
        svc_fit = self.svc.fit(self.to_feature(X), y)

    def predict(self, post):
        return self.svc.predict(self.to_feature([post]))
        
    def save_model(self):
        with open('steevebot/save/svm.pickle', 'wb') as f:
            pickle.dump(self.svc, f)
    
    def restore_model(self):
        with open('steevebot/save/svm.pickle', 'rb') as f:
            self.svc = pickle.load(f)

# In[ ]:




# In[ ]:



