# -*- coding: utf-8 -*-
"""
Created on Mon Apr 13 17:25:19 2020

@author: Carlos
"""

import requests
import webbrowser

filePath = "C:\\Users\\Carlos\\Desktop\\regalos\\20180728_180529.jpg"
searchUrl = 'http://www.google.hr/searchbyimage/upload'
multipart = {'encoded_image': (filePath, open(filePath, 'rb')), 'image_content': ''}
response = requests.post(searchUrl, files=multipart, allow_redirects=False)
print(response.content)
fetchUrl = response.headers['Location']
webbrowser.open(fetchUrl)