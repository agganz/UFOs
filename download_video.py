# -*- coding: utf-8 -*-
"""
Created on Thu Nov 23 11:43:47 2023

@author: Doctorando1
"""

import requests

user_name = 'jjb3129'
pwd = 'Rooster10010101'

payload = {"Username": user_name, "Password": pwd}

auth_path = requests.auth.HTTPBasicAuth(user_name, pwd)
url_auth = 'webproxy-jet.jetdata.eu:3128'

response_auth = requests.get(url_auth, auth = auth_path)

url = "https://users.euro-fusion.org/avihost//{0}/on//00{1}".format('kl1-o8wa', 94626)

response = requests.get(url, data = payload)

open("0094626", "wb").write(response.content)