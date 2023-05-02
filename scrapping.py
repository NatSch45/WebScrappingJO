import os
import urllib.request as urlreq
from bs4 import BeautifulSoup

from commons import *
from DAO.requests import *

def dictToSequence(data):
    return [tuple(dict.values()) for dict in data]

def listToSequence(data):
    return [(val,) for val in data]

    
def prepareRequest(URL):
    req = urlreq.Request(URL)
    req.add_header('User-Agent', os.getenv('USER_AGENT'))
    return req