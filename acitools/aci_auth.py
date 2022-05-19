from typing import Tuple
import requests

def aci_auth(auth_url, auth_data):
    requests.packages.urllib3.disable_warnings() 
    session = requests.session()
    auth_res = True     

    try: 
      session.post(auth_url, json=auth_data, verify=False)
    except:
      auth_res = False
      print("Login failed. Provide correct login info")

    return session, auth_res