import requests
import re
from bs4 import BeautifulSoup
from .tor_session import *

# def link_is_invalid(url):
#     html = requests.get(url)
#     sp = BeautifulSoup(html.text, "html.parser")

#     if "Sorry! That job has been removed." in sp.text:
#         return True
#     elif "404 - The page you're looking for couldn't be found or it may have expired." in sp.text:
#         return True
    
#     return False

headers = {'User-Agent': 'User-Agent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}

def remove_invalid_url(job):
    html = session.get(job.url, headers=headers)

    if html.status_code > 400:
        print("Error code > 400. Your IP address may have been blocked.")
        return
    sp = BeautifulSoup(html.text, "html.parser")

    if "Sorry! That job has been removed." in sp.text:
        job.delete()
        return 1
    elif "404 - The page you're looking for couldn't be found or it may have expired." in sp.text:
        job.delete()
        return 1
    
    return 0
