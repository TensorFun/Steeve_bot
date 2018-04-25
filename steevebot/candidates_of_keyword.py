from .training import *
from .data_responser import *


def save_pl_DB():
    '''
    Extract PLs from all posts
    '''
    import json
    from .training import create_PL
    from .modules import get_pl_keywords
    # from .google_map_API import get_all_location_range
    
    print("load data")
    total_data = [] 
    # load all data from database
    ori_data = all_data()
    key = list(ori_data.keys())
    to_DB = []
    for k in key: 
        print(k)
        for num, job_num in enumerate(ori_data[k]):
            if num%500 == 0:
                print(num)
           
            pl_des = get_pl_keywords(job_num["jobDescription"])
            pl_ski = get_pl_keywords(job_num["skills"])
            
            str_data = ",".join(pl_des+pl_ski) 

            #### future ####
            # get location #
            temp = []
            temp.append(job_num["JobID"])
            temp.append(k)
            temp.append(str_data)
            temp.append("None")
            to_DB.append(temp)
            
    #### save PL and location to DB ####
#     str_loc = get_all_location_range(all_loc)
#     for n,l in enumerate(to_DB):
#         s = ",".join(str_loc[n])
#         l.append(s)
    create_PL(to_DB)

def all_pl_data():
    '''
    Return all PL posts
    '''
    from .modules import get_pl_keywords

    # load all PL posts from database
    pl_data = all_PL()
    key = list(pl_data.keys())
    total_data = []
    for k in key:
        print(k)
        data = []
        for num, job_num in enumerate(pl_data[k]):
            job_pl = job_num["PL"]
            data.append(job_pl.split(","))
        
        total_data.append(data)
    return total_data

def convert_field_type(num_k):
    '''
    Convert the field corresponding to the number
    
    param: num_k (int) - field index
    return: field name(str)
    '''
    pl_data = all_PL()
    key = list(pl_data.keys())
    for n, k in enumerate(key):
        if n == int(num_k):
            return str(k)
        
            
######### for backend #########

######### Below is SVM

# use global variable to store SVM instance with its model
Predict_TFIDF, Predict_SVM = None, None
def training_SVM():
    '''
    Get all data and train SVM model
    '''
    from .TFIDF import TFIDF
    from .SVM import SVM

    save_pl_DB()
    total_data = all_pl_data()
    
    # create TFIDF and SVM instance
    global Predict_TFIDF
    global Predict_SVM
    Predict_TFIDF = TFIDF(total_data)
    Predict_SVM = SVM(Predict_TFIDF)

    # reform data
    X, y = [], []
    for i, field_posts in enumerate(total_data):
        for post in field_posts:
            y.append(i)
            X.append(post)
    
    Predict_SVM.train(X, y)
    Predict_SVM.save_model() # store model in case of the system crashes

        
def get_jobs(user_cv):
    '''
    Input user CV and return recommend jobs
    '''
    from .modules import pick_top_k, get_pl_keywords
    from .TFIDF import TFIDF
    from .SVM import SVM

    global Predict_TFIDF
    global Predict_SVM

    try:
        pl_cnt, words = Predict_TFIDF.get_tfidf()
    except: 
        # if there is no TFIDF instance
        total_data = all_pl_data()
        Predict_TFIDF = TFIDF(total_data)
        pl_cnt, words = Predict_TFIDF.get_tfidf()
    
    if not Predict_SVM:
        Predict_SVM = SVM(Predict_TFIDF)
        Predict_SVM.restore_model()
    
    print('load_data')
    # User_CV preprocessing - get PLs
    cv_PL = get_pl_keywords(user_cv)
    print(cv_PL)

    cv_toDB = ",".join(cv_PL)
    # predict_field = "Frontend"
    print('start predict f')
    predict_field = Predict_SVM.predict(cv_PL)
    print(predict_field)
    # predict_field = 0
    # predict_field = get_predict_field(cv_PL,pl_cnt)
    # convert predict_field style
    print('get field ', predict_field)

    # get field name by field index
    predict_field_DB_style = convert_field_type(predict_field)
    
    # get field data from DB
    print('to db style', predict_field_DB_style)
    p = get_field_PL(predict_field_DB_style)
    posts_predict_field = []
    
    ### TODO: future work ###
    # location filter #
    for j in p:
        # if location_filter(user_location,j.PL_location):
        posts_predict_field.append({'id':j.Job.JobID,'PL':j.PL.split(",")})
    print(posts_predict_field[0])

    job_candidates = pick_top_k(cv_PL, posts_predict_field)

    return cv_toDB,job_candidates,predict_field_DB_style


########### Below is DNN

def training_DNN():
    '''
    Preprocess posts and save them to DB, and train a DNN model
    '''
    from .DNN_model import get_Dnn_model,get_predict_field
    
    # get all PL posts
    save_pl_DB()
    total_data = all_pl_data()
    
    # training DNN model and save
    get_Dnn_model(total_data)

    
# # input user CV and get recommend jobs #
# def get_jobs(User_CV):
#     # from .DNN_model import get_predict_field
#     from .modules import pick_top_k,get_pl_keywords
#     from .google_map_API import location_filter
#     from .TFIDF import TFIDF

#     try:
#         pl_cnt, words = Predict.get_tfidf()
# #         print('pl_cnt exists')

#     except:
#         total_data = all_pl_data()
#         Predict = TFIDF(total_data)
#         pl_cnt, words = Predict.get_tfidf()
    
#     print('load_data')
#     # User_CV preprocessing 
#     cv_PL = get_pl_keywords(User_CV)
#     print(cv_PL)

#     cv_toDB = ",".join(cv_PL)
# #     predict_field = "Frontend"
#     print('start predict f')
#     predict_field = Predict.predict_field(cv_PL)
#     print(predict_field)
#     # predict_field = 0
#     # predict_field = get_predict_field(cv_PL,pl_cnt)
#     # convert predict_field style
#     print('get field ',predict_field)
#     predict_field_DB_style = convert_field_type(predict_field)
    
#     #### get field data from DB ####
#     print('to db style', predict_field_DB_style)
#     p = get_field_PL(predict_field_DB_style)
#     posts_predict_field = []
    
#     ### future ###
#     # location filter #
#     for j in p:
#         # if location_filter(user_location,j.PL_location):
#         posts_predict_field.append({'id':j.Job.JobID,'PL':j.PL.split(",")})
#     print(posts_predict_field[0])

    
#     job_candidates = pick_top_k(cv_PL, posts_predict_field)

#     return cv_toDB,job_candidates,predict_field_DB_style
    

# input company post and return applicants
def get_applicants(post):
    '''
    Input company requirement and recommend applicants

    params: post(str) - company requirement
    return: applicants(list) - top 6 suitable applicants
    '''
    from .modules import pick_top_k,get_pl_keywords
    post_PL = get_pl_keywords(post)

    user_PLs = []
    applicants_PL = get_applicants_PL()

    for i in applicants_PL:
        user_PLs.append({'id':i[1],'PL':i[0].split(',')})

    applicants = pick_top_k(post_PL, user_PLs)

    return applicants


# total_data = all_pl_data()

# from .DNN_model import get_Dnn_model    
# get_Dnn_model(total_data)
# a = get_applicants("html,javascript html, java,c,css,css,css")
# a = get_jobs("html,javascript html, java,c,css,css,css")

# print(a)