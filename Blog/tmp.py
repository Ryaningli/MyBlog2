import requests

url = 'http://127.0.0.1:8000/api/blog/?search=2021-07-23 16:30:13'

result = requests.get(url)

print(result.json())