import requests

def aci_auth(auth_url, auth_data):
    requests.packages.urllib3.disable_warnings() 
    session = requests.session()     

    try: 
      session.post(auth_url, json=auth_data, verify=False)
    except:
      print("Login failed")

    return session