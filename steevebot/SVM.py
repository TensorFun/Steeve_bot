import pickle 
import numpy as np
from sklearn import feature_extraction, svm, metrics
from pyfasttext import FastText


class SVM:
    '''
    Create SVM instance and train SVM model
    '''
    def __init__(self, TFIDF): # TODO: plz give me the model or using global singleton
        # self.model = FastText('/home/yee0/Atos/wiki.en.bin')
        self.model = FastText("/home/nlplab/yee0/Atos/wiki.en.bin")
        self.TFIDF = TFIDF
        self.tfidf_dict, self.words = TFIDF.get_tfidf()
    
    def set_tfidf(self, TFIDF):
        '''
        Update TFIDF instance

        Params: new TFIDF instance
        '''
        self.TFIDF = TFIDF
        self.tfidf_dict, self.words = TFIDF.get_tfidf()
    
    def to_feature(self, X):
        '''
        Convert all posts (X) to vector format

        Param: X(list) - all posts
        '''
        return [self.vec(self.TFIDF.predict_field(post), post) for post in X]
        
    def vec(self, field_index, post):
        '''
        Convert a post (PL list) to vector

        Params: 
        - field_index: the predicted field
        - post: PL list
        
        Return: 300 dimension vector
        '''
        v = np.zeros(300)
        post = set(post) # make unique
        for pl in post:
            if pl != '' and pl in self.words:
                # multiply vector by the PL's TFIDF score as weight
                v += self.model.get_numpy_vector(pl) * self.tfidf_dict[field_index][pl]
        return v
    
    def train(self, X, y):
        '''
        Train SVM model

        Params:
        - X: PL posts, 2-d list
        - y: 1-d list
        '''
        self.svc = svm.SVC()
        svc_fit = self.svc.fit(self.to_feature(X), y)

    def predict(self, post):
        '''
        Predict field

        Param: post - PL list
        Return: predicted field
        '''
        return self.svc.predict(self.to_feature([post]))
        
    def save_model(self):
        with open('steevebot/save/svm.pickle', 'wb') as f:
            pickle.dump(self.svc, f)
    
    def restore_model(self):
        with open('steevebot/save/svm.pickle', 'rb') as f:
            self.svc = pickle.load(f)
