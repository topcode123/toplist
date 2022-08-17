from newspaper import Config
from sys import prefix
from pymongo import MongoClient
import time
import html.parser    
import requests
from requests.models import HTTPBasicAuth
from Settings import *
from bs4 import BeautifulSoup
import re
from urllib.parse import urlparse
from SpinService import *
import json
from unidecode import unidecode
from Title_fix import *
from aiohttp import request
import requests
import json
import base64
import html
import html.parser  
from Settings import *
from bson import ObjectId
from pymongo import MongoClient
import time
from PIL import Image
import io
from unidecode import unidecode
from aiohttp import request
from extract import ContentExtractor
from lxml.html import tostring
spinService = SpinService()

config = Config()
campaign_root  = MongoClient(CONNECTION_STRING_MGA1).campaigns.data
keywords  = MongoClient(CONNECTION_STRING_MGA1).keywords

contentExtractor = ContentExtractor(config)
from bs4 import BeautifulSoup
def replace_attr(soup, from_attr: str, to_attr: str):
    if from_attr in str(soup):
        soup[to_attr] = soup[from_attr]
        del soup[from_attr]

        return soup
    else:
        return soup


def process_content(url,content,category,title,self_url):
        content = {
            "user":url,
            "title":title,
            "content":content,
            "category":category,
            "slug":self_url
        }
        return content

def restImgUL(website,user,password,urlimg,src_img):
    newID = None
    if urlimg ==None:
        return newID
    else:
        try:
            path_files = urlimg.split("/")[-1].split("?")[0]
            with requests.get(urlimg,stream=True,allow_redirects=False,verify=False,timeout=50) as response:
                if response.status_code == 200:
                    image = Image.open(io.BytesIO(response.content))
                    image = image.resize((900,603))
                    output = io.BytesIO()
                    credentials = user + ':' + password
                    token = base64.b64encode(credentials.encode())
                    if "JPG" in path_files.upper():
                        image.save(output,format='JPEG',optimize = True,quality = 30)
                        headers={ 'Authorization': 'Basic ' + token.decode('utf-8'),'Content-Type': 'image/jpeg','Content-Disposition' : 'attachment; filename=%s'%path_files}

                    elif "PNG" in path_files.upper():
                        image.save(output,format='PNG',optimize = True,quality = 30)
                        headers={ 'Authorization': 'Basic ' + token.decode('utf-8'),'Content-Type': 'image/png','Content-Disposition' : 'attachment; filename=%s'%path_files}
                    image = output.getvalue()

                    with requests.post(website,
                        data=image,
                        headers=headers,timeout=10) as response:
                            res = response.json(encoding="utf-8")
                            newID= res.get('id')
                            return newID
        except Exception as e:
            print(str(e))
            return None

def importcontent(content,idthump):
    #cl = await clientt.user["userdatabase"].find_one({'_id':ObjectId(content['UserId'])})
    cl = content['user']["web_info"]
    website = cl["WebsitePost"]
    websiteimg  = cl["Website"] + "/wp-json/wp/v2/media"
    user = cl["UserWP"]
    password = cl["PasswordWP"]

    if idthump == None:
        post = {
            'status': 'publish', 
            "title":content["title"],
            "content":content["content"],
            'categories':content["category"],
            'slug': content['slug'] 
        }
    else:
        post = {
            'status': 'publish', 
            "title":content["title"],
            "content":content["content"],
            'categories':content["category"],
            'featured_media':int(idthump),
            'slug': content['slug'] 
        }
    credentials = user + ':' + password
    token = base64.b64encode(credentials.encode())
    header = {'Authorization': 'Basic ' + token.decode('utf-8'),'Content-Type': 'application/json'}


    with requests.post(website , headers=header,json = post) as response:
        res = response.status_code
    if res!=None:
        print(res)
        print(post["slug"])
        url = content['user']["campaign"]
        if idthump != None:
            if url["Top10url"] == None or url["Top10url"] == []:
                url["Top10url"] = [{"link":content['user']["web_info"]["Website"] +"/"+ post['slug'],"name":content["title"]}]
            elif len(url["Top10url"])<10:
                url["Top10url"].append({"link":content['user']["web_info"]["Website"] +"/"+ post['slug'],"name":content["title"]})
            else:
                url["Top10url"]= [{"link":content['user']["web_info"]["Website"] +"/"+ post['slug'],"name":content["title"]}] + url["Top10url"][1:10]

            campaign_root.update_one({"_id":ObjectId( content['user']["campaign"]["_id"])},{"$set":{"Top10url":url["Top10url"]}})
            keywords[content['user']['campaign']["WebsiteId"]].update_one({"_id":ObjectId( content['user']["keyword"]["_id"])},{"$set":{"status":"done","link":content['user']["web_info"]["Website"] +"/"+ post['slug']}})
    return True

def ImportContents(url,content,category,title,self_url,idthump):
    dataprocess = process_content(url,content,category,title,self_url)
    import_content =  importcontent(dataprocess,idthump)
    return import_content
