import requests

url = 'http://0.0.0.0:6000/deploy'
info = {'run_id':'6284e66e802040d496acb155390f5721',
        'exp_id': '0' }

requests.post(url,data=info)
