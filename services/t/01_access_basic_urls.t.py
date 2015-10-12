from TAP.Simple   import *
import requests

plan(4)

r = requests.get('http://localhost:8000/')
eq_ok(r.status_code, 200, 'accessing the base url should have code 200')
eq_ok(r.headers['content-type'], 'application/json', 'default responses should be json')

r2 = requests.get('http://localhost:8000/?format=html')
eq_ok(r.status_code, 200, 'accessing the base url in html format should have code 200')
eq_ok(r.headers['content-type'], 'text/html')
