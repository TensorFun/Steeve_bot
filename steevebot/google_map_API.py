
# coding: utf-8

"""
FUTURE WORK
"""

import time
import googlemaps
from .credentials import api_keys
# gmaps = googlemaps.Client(key=google_Key)
import random 
import signal
# r_key = random.randint(0,3)
# gmaps = googlemaps.Client(key=api_keys[r_key])

class TimeoutException(Exception):   # Custom exception class
    pass

def timeout_handler(signum, frame):   # Custom signal handler
    raise TimeoutException


# def get_location_range(address):
#     # Change the behavior of SIGALRM
#     signal.signal(signal.SIGALRM, timeout_handler)
#     signal.alarm(5)
#     address_range = []
#     try :
#         geocode_result = gmaps.geocode(address)
#         first_filter = geocode_result[0]['address_components']
#         #[0]['long_name']
#         for a in first_filter[:2]:
#             address_range.append(a['long_name'])
        
#     except:
#         address_range.append(address)
# #     print(address_range)

#     return address_range

def get_all_location_range(address_list):
    # Change the behavior of SIGALRM
    all_address_range = []
    loc_len = len(address_list)
    r_key = 0
    gmaps = googlemaps.Client(key=api_keys[r_key])
    print('start')
    for n,address in enumerate(address_list):
        if r_key != int(n//3000%4):
            r_key = int(n//3000%4)
            gmaps = googlemaps.Client(key=api_keys[r_key])
            print('change key',r_key)
        else:
            r_key = int(n//3000%4)
        if n%100 == 0:
            print(n)

        
        signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(5)
        address_range = []
        try :
            geocode_result = gmaps.geocode(address)
            first_filter = geocode_result[0]['address_components']
        #[0]['long_name']
            for a in first_filter[:2]:
                address_range.append(a['long_name'])
        
        except:
            address_range.append(address)
        all_address_range.append(address_range)
#     print(address_range)
    

    return all_address_range


# In[1]:


def location_filter(user_target, company_range):
    
    for c_address in company_range:
        if user_target == c_address:
            break
    
    return True
    


# In[8]:


"""get_location_range('taichung')"""
"""location_filter('taichung',['taipei','china',''usa])"""

