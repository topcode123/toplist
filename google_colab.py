import traceback
def get_database():
    from pymongo import MongoClient
    import pymongo

    # Provide the mongodb atlas url to connect python to mongodb using pymongo
    CONNECTION_STRING_MGA1 = "mongodb://mnetwordtest2021:mnetwordtest2021@94.237.76.25:27017/admin?retryWrites=true&w=majority"
    # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
    from pymongo import MongoClient
    client = MongoClient(CONNECTION_STRING_MGA1)

    # Create the database for our example (we will use the same database throughout the tutorial
    return client
    
# This is added so that many files can reuse the function get_database()
from ImportContent import *
from googlesearch import search
import requests
import time
import random
from googlesearchcustomer import *
import traceback
from newspaper import Config,Article
from urllib.parse import urlparse
from google_colab1 import *
client1 = get_database()

userAgents=['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36','Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36','Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36','Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36','Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36','Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36','Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.71 Safari/537.36','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.83 Safari/537.1']
cl = client1.queuekeywords.data
url = client1.url_test.data
cl1 = client1.keywords

while True:

  while True:

    cancle = False
    time.sleep(20)
    if cl.count_documents({})>0:
      try:
        # h=h+1
        keyword = cl.find_one_and_delete({})
        if keyword:
              createandimportcontent(keyword)
      except Exception as e:
        print(traceback.format_exc())

        if "429" in str(e):
          raise("too many")           # except Exception as e:
    if cancle:
      break
                # print(h)