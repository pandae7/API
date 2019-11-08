import requests

url = 'http://0.0.0.0:6000/deploy'
info = {'run_id':'e0ef407d89d9459ea30d71b9112cfe4e',
        'exp_id': '0' }

x = requests.post(url,data=info)
# print(x.text)