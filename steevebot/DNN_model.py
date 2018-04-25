# coding: utf-8

import requests
import json, os
import tensorflow as tf
import numpy as np
from collections import Counter, OrderedDict
from operator import itemgetter    
from sklearn.model_selection import train_test_split

from .TFIDF import TFIDF

DNN_model_meta_path = './dnn_model.ckpt.meta'
DNN_model_ck_path = './dnn_model.ckpt'


# Use fasttext by interface pyfasttext 
from pyfasttext import FastText
# get model
model = FastText("/home/nlplab/yee0/Atos/wiki.en.bin")
# model = FastText('/home/vincent/atos/wiki.en.bin')
# model = FastText('/home/yee0/Atos/wiki.en.bin')


def reset_graph(seed=42):
    tf.reset_default_graph()
    tf.set_random_seed(seed)
    np.random.seed(seed)

# get post features 2400-d
def get_pl_v(j,pl_cnt,NUM_PL,D_WORD):
    '''
    Get 2400 dimension features for each post
    '''
    m = []
    aaa = {}
    
    # compare four fields tf-idf value
    N_SCORE = .0
    MAX_SCORE = .0
    PREDICT_FIELD = '' 
    
    for cnt_f in pl_cnt:
        for pl in j:
            if pl_cnt[cnt_f].get(pl) == None:
                continue
                N_SCORE += pl_cnt[cnt_f].get(pl)
            if N_SCORE > MAX_SCORE:
                PREDICT_FIELD = cnt_f
                MAX_SCORE = N_SCORE
            elif PREDICT_FIELD == '':
                PREDICT_FIELD = cnt_f
                        
    for pl in j:
#         print(type(pl))
        if pl_cnt[PREDICT_FIELD].get(pl) == None:
            print('can not get',pl)
            pass
        else:
            aaa[pl] = pl_cnt[PREDICT_FIELD].get(pl)
    
    print(sorted(dict(aaa).items(), key=itemgetter(1), reverse=True)[:8])
            
    for i, g in sorted(dict(aaa).items(), key=itemgetter(1), reverse=True)[:8]:
        try:
            print('to vector',i)
            x = list(model[i])
            m = m + x
        except:
            pass
                
                
    if len(m) < D_WORD*NUM_PL:
        if (len(m)/D_WORD)%2 == 1:
            m = m+m[0:D_WORD]
        if len(m) == D_WORD*6:
            m = m + m[0:D_WORD*2]
        elif len(m) == D_WORD*4:
            m = m + m
        elif len(m) == D_WORD*2:
                m = m + m[0:D_WORD]
    if len(m) != 2400:
        m = []
        m.append(model['python'])
        m.append(model['java'])
        m.append(model['sql'])
        m.append(model['security'])
        m = m+m
        print('MATCH DEFAULT')

    return m



def pl_preprocessing(total_pl):
    train_data = []
    train_y = []
    NUM_PL = 8
    D_WORD = 300
    tf_idf = TFIDF(total_pl)
    pl_cnt, words = tf_idf.get_tfidf()
    
    # label
    l = 0
    
    for field in total_pl:
#         print(field)
        for num, j in enumerate(field):

            m = get_pl_v(j,pl_cnt,NUM_PL,D_WORD)
            if len(m) == 2400:                    
                train_data.append(m)
                train_y.append(l)
            else:

                pass
        l += 1
#                             print(i)
#     print(t,s)
            
    return train_data,train_y


class CrossValidationFolds(object):
    '''
    K-fold for mixing up data
    '''
    
    def __init__(self, data, labels, num_folds, shuffle=True):
        self.data = data
        self.labels = labels
        self.num_folds = num_folds
        self.current_fold = 0
        
        # Shuffle Dataset
        if shuffle:
            perm = np.random.permutation(self.data.shape[0]) ##隨機打亂資料
            data = data[perm]
            labels = labels[perm]
    
    def split(self):
        current = self.current_fold
        size = int(self.data.shape[0]/self.num_folds) # k size = 30596 / 5
        
        index = np.arange(self.data.shape[0]) 

        # Use True/False to get validation samples
        lower_bound = index >= current*size # validation lower bound
        upper_bound = index < (current + 1)*size # upper bound

        cv_region = lower_bound*upper_bound

        cv_data = self.data[cv_region] # Get True data
        train_data = self.data[~cv_region]
        
        cv_labels = self.labels[cv_region]
        train_labels = self.labels[~cv_region]
        
        self.current_fold += 1 
        return (train_data, train_labels), (cv_data, cv_labels)


def L_layers_model(X, h_units, n_class, dropout=0.5):
    '''
    Construct DNN
    '''
    # default he_init: factor=2.0, mode='FAN_IN', uniform=False, seed=None, dtype=tf.float32
    he_init = tf.contrib.layers.variance_scaling_initializer()
    keep_prob = tf.placeholder(tf.float32)
    
    with tf.name_scope("DNN"):
        hidden1 = tf.layers.dense(X, 128, activation=tf.nn.relu, name="hidden1",use_bias=True, kernel_initializer= he_init,
                                      bias_initializer=he_init)
        dropout1= tf.layers.dropout(hidden1, rate=0.5,name="dropout1")
        
        hidden2 = tf.layers.dense(dropout1, 128, activation=tf.nn.relu, name="hidden2",use_bias=True, kernel_initializer= he_init,
                                      bias_initializer=he_init)
        dropout2= tf.layers.dropout(hidden2, rate=0.5,name="dropout2")
        
        hidden3 = tf.layers.dense(dropout2, 128, activation=tf.nn.relu, name="hidden3",use_bias=True, kernel_initializer= he_init,
                                      bias_initializer=he_init)
        dropout3= tf.layers.dropout(hidden3, rate=0.5,name="dropout3")
        
        hidden4 = tf.layers.dense(dropout3, 128, activation=tf.nn.relu, name="hidden4",use_bias=True, kernel_initializer= he_init,
                                      bias_initializer=he_init)
        dropout4= tf.layers.dropout(hidden4, rate=0.5,name="dropout4")
        
        hidden5 = tf.layers.dense(dropout4, 128, activation=tf.nn.relu, name="hidden5",use_bias=True, kernel_initializer= he_init,
                                      bias_initializer=he_init)
        dropout5= tf.layers.dropout(hidden5, rate=0.5,name="dropout5")
            
        # Combine tf.nn.sparse_softmax_cross_entropy_with_logits [128 , 5]
        logits = tf.layers.dense(dropout5, n_class, name="logits")
    
    return logits

def Train_op(y, logits,batch_size,n_train):
    with tf.name_scope("calc_loss"):
        entropy = tf.nn.sparse_softmax_cross_entropy_with_logits(labels=y, logits=logits)
        loss = tf.reduce_mean(entropy, name="loss")
    
    ## Use AdamOptimizer 
    with tf.name_scope("train"):
        batch = tf.Variable(0)

        learning_rate = tf.train.exponential_decay(
                1e-4,  # Base learning rate.
                batch * batch_size,  # Current index into the dataset.
                n_train,  # Decay step.
                0.95,  # Decay rate.
                staircase=True)
        
        optimizer = tf.train.AdamOptimizer(0.001)
        training_op = optimizer.minimize(loss, global_step=batch,name="training_op")

    return (loss, training_op)

def acc_model(y, logits):
    # Calc accuracy
    with tf.name_scope('calc_accuracy'):
        correct = tf.equal(tf.argmax(logits, 1), y)
        accuracy = tf.reduce_mean(tf.cast(correct, tf.float32),name="accuracy")

    # Calc precision 
    with tf.name_scope("precision"):
        _, precision = tf.metrics.precision(predictions = tf.argmax(logits,1), labels=y)

    # Calc recall
    with tf.name_scope('recall'):
        _, recall = tf.metrics.recall(predictions = tf.argmax(logits,1), labels=y)

    return (accuracy, precision, recall)


def shuffle_data(data, labels):
    idx = np.random.permutation(len(data))
    data, label = data[idx], labels[idx]
    return (data, label)


def get_Dnn_model(total_pl):
    '''
    Train DNN model
    '''
    
    NUM_PL = 8
    D_WORD = 300
    FOLDS = 5
    
    x, y = pl_preprocessing(total_pl)
    x = np.array(x)
    y = np.array(y)

    ###### test is same as training data #######
    X_train, X_test1, Y_train, y_test1 = train_test_split(x, y, test_size = 0.2)
    data = CrossValidationFolds(X_train, Y_train, FOLDS)
    (X_train1, y_train1), (X_valid1, y_valid1) = data.split()
    
    print(X_train1.shape,y_train1.shape)

    ###### test is different from training data #######
    # data = CrossValidationFolds(x, y, FOLDS)
    # (X_train1, y_train1), (X_valid1, y_valid1) = data.split()

    # X_test1,y_test1 = load_pl('../new_Steeve_data/filter_Dice/can/')
    # X_test1 = np.array(X_test1)
    # y_test1 = np.array(y_test1)
    
    ### setting
    
    in_units = D_WORD*NUM_PL
    n_class = len(total_pl) # tell 0 ,1 ,2 ,3 and 4. = 5 classes

    n_train = len(X_train1) # length of training data
    batch_size = 50
    n_batch = n_train // batch_size

    X = tf.placeholder(tf.float32,[None,in_units],name="X") # init x [None,784]
    y = tf.placeholder(tf.int64, shape=(None), name="y") # init y [None]
    
    logits = L_layers_model(X, 128, n_class, 0.5)
    Y_proba=tf.nn.softmax(logits,name="Y_proba")
    loss, train_op = Train_op(y, logits,batch_size,n_train)
    accuracy, precision, recall = acc_model(y, logits)

    prediction=tf.argmax(Y_proba,1)

    saver = tf.train.Saver()  # call save function
    config = tf.ConfigProto(device_count = {'GPU': 1}) # assign gpu
    
    # Params for Train
    epochs = 1000 # 10 for augmented training data, 20 for training data
    val_step = 100 # calc accuracy every 100 steps

    # Training cycle
    max_acc = 0. # Save the maximum accuracy value for validation data
    early_stop_limit = 0 # record early_stop value

    init = tf.global_variables_initializer()
    init_l = tf.local_variables_initializer()
    
    with tf.Session(config=config) as sess:
        
        sess.run([init, init_l])
        for epoch in range(epochs):
            if early_stop_limit >= 200: 
                print('early_stop...........')
                break

            # Random shuffling
            train_data, train_label = shuffle_data(X_train1, y_train1)

            # Use batch to train model
            for i in range(n_batch):
            # Compute the offset of the current minibatch in the data.
                offset = (i * batch_size) % (n_train)
                batch_xs = train_data[offset:(offset + batch_size), :]
                batch_ys = train_label[offset:(offset + batch_size)]
                sess.run([train_op, loss], feed_dict={X:batch_xs, y: batch_ys})

                # validate model every n step
                if i % val_step == 0:
                    val_acc = sess.run(accuracy, feed_dict={X: X_valid1, y: y_valid1})
                    print("Epoch:", '%04d,' % (epoch + 1),
                          "batch_index %4d/%4d , validation accuracy %.5f" % (i, n_batch, val_acc))

                # Check early stop
                    if max_acc >= val_acc:
                        early_stop_limit += 1
                        if early_stop_limit == 200:
                            break

                # if val_acc > max_acc, replace it
                    else: # validation_accuracy > max_acc
                        early_stop_limit = 0
                        max_acc = val_acc
                        saver.save(sess,DNN_model_ck_path)                        
                        print('dnn_model.ckpt-' + 'complete-%04d-' % (epoch + 1) + 
                          "batch_index-%d" % i)
        sess.run(init_l)
        saver.restore(sess,DNN_model_ck_path) # restore early_stop model

        print('Acc_test :' , sess.run(accuracy, feed_dict={X: X_test1, y: y_test1}))
        print('Prec_value :' , sess.run(precision, feed_dict={X: X_test1, y: y_test1}))
        print('Recall_value :' , sess.run(recall, feed_dict={X: X_test1, y: y_test1}))
    

def get_all_raw_pl():
     
    print("load data")
    total_data = [] 
    r = requests.get('https://steevebot.ml/all')
    ori_data = r.json()
    key = list(ori_data.keys())
    
    for k in key: 
        data = []
    
        for num, job_num in enumerate(ori_data[k]):
            if num%500 ==0:
                print(num)

            pl_des = get_pl_keywords(job_num["jobDescription"])
            pl_ski = get_pl_keywords(job_num["skills"])
            data.append(pl_des+pl_ski)

        total_data.append(data)
    return total_data


def get_predict_field(pl_job,pl_cnt):
    '''
    Input Job PLs and predict a field
    '''
    # print(in)
    reset_graph()
    NUM_PL = 8
    D_WORD = 300
    print('pl_job DNN',pl_job)

    x = get_pl_v(pl_job,pl_cnt,NUM_PL,D_WORD)
    x = np.array(x)
    # print(x)
    x = x.reshape([1,-1])
    
    restore_saver = tf.train.import_meta_graph(DNN_model_meta_path)
    X = tf.get_default_graph().get_tensor_by_name("X:0")
    y = tf.get_default_graph().get_tensor_by_name("y:0")
    loss = tf.get_default_graph().get_tensor_by_name("calc_loss/loss:0")
    Y_proba = tf.get_default_graph().get_tensor_by_name("Y_proba:0")

    init = tf.global_variables_initializer()
    
    with tf.Session() as sess:
        prediction=tf.argmax(Y_proba,1)
        sess.run(init)
#         print("predictions", prediction.eval(feed_dict={X: x}, session=sess),Ty)
        
        predict_field = prediction.eval(feed_dict={X: x}, session=sess)

    return predict_field



"""
Trainig DNN model

total_pl = get_all_raw_pl()
get_Dnn_model(total_pl)
"""

"""
Predict field

get_predict_field(pl of job)
"""

