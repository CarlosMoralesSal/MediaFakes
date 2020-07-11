# -*- coding: utf-8 -*-
"""
Created on Sat May 16 16:08:43 2020

@author: Carlos
"""

import urllib
from urllib import request
from http.cookiejar import CookieJar
from bs4 import BeautifulSoup
import os
#from urllib2 import quote as q, unquote as unq, urlencode
#from urllib2 import build_opener, urlopen, HTTPCookieProcessor
#from cookielib import CookieJar
#import urlparse
import re
import base64
from html.parser import HTMLParser

cj = CookieJar()
opener = request.build_opener(request.HTTPCookieProcessor(cj))

opener.addheaders = [
    ('User-agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:19.0) Gecko/20100101 Firefox/19.0'),
    ('Accept-Language','es,en-us;q=0.7,en;q=0.3')
]


BASE_URL = 'https://www.google.com'
BASE_SEARCH_URL = BASE_URL + '/searchbyimage?%s'

REFERER_KEY = 'Referer'

def get_referer_index():
    i = 0
    for k, v in opener.addheaders:
        if k == REFERER_KEY:
            return i
        i += 1
    else:
        return None


def set_referer(url):
    cur = get_referer_index()
    if cur is not None:
        del opener.addheaders[cur]
    opener.addheaders.append(
        (REFERER_KEY, url)
    )

def search_image(url):
    params = {
        'image_url': url,
        'hl': 'es',
        }
    query = BASE_SEARCH_URL % urllib.parse.urlencode(params)
    print(query)
    f = opener.open(query)
    url = f.url
    f = opener.open(url)
    html = f.read()
    set_referer(f.url)
    return html

def get_similar_image_urls(html):
    soup = BeautifulSoup(html,'html.parser')
    #print(soup.prettify())
    #soup.find_all('div', id="iur")
    for item in soup.find('div', id="iur").find_all('a', class_="bia"):
        url = item.get('href')
#        print(url)
#        print('\n')
#        print(str(item))
        #url2 = item.get('src')
        soup2= BeautifulSoup(str(item),'html.parser')
        for item2 in soup2.find('g-img').findAll('img'):
          #Coger el id de la imagen
          idimage=item2.get('id')
          url2= item2.get('src')
          url3=item2.get('title')
          print(idimage)
          #print(url3)
    scripts=soup.find_all('script')
    path = "./downloadsimages"
    os.mkdir(path)
    for nonce in scripts:
        if nonce.has_attr('nonce'):
            if str(nonce.text.strip()).find("data:image/jpeg;base64")>0:
             images=str(nonce.text.strip())[19:]
             piece="\';"
             print('\n')
             print('\n')
             
             subs='data:image/jpeg;base64,'
             images=images.replace(subs,"")
             print(images)
             #images=images.replace('\\x3d','=')
             imageName=images[images.find(piece)+2:]
             #imageName=imageName[:-(imageName.find(";_setImagesSrc(ii,s);})();"))]
             subStr=";_setImagesSrc(ii,s);})();"
             subStr2="var ii=[";
             imageName=imageName.replace(subStr,"").replace(subStr2,"").replace("]","").replace("\'","").replace(",","_")
             #print(imageName)
             print('\n')
             images=images[:-(len(images)-(images.find(piece)))].replace('\\x3d','=')
             imgdata = base64.b64decode(images)
             #print(images)
             with open(path+"/"+imageName+".jpg", "wb") as fh:
                 fh.write(imgdata)
        
        
        #yield urllib.parse.parse_qs(urllib.parse.urlparse(url).query)['imgurl']

def main():
    import sys
    url = 'http://pbs.twimg.com/media/EPUguZFX0AAN5tg.jpg'
    html = search_image(url)
    #print(html)
    #get_similar_image_urls(html)
    get_similar_image_urls(html)
    
    #for url in get_similar_image_urls(html):
    #    print(url)


if __name__ == '__main__':
    main()