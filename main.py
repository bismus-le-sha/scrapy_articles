import requests
from bs4 import BeautifulSoup

data = requests.get('https://www.digitalocean.com/community/tutorials/how-to-work-with-web-data-using-requests-and-beautiful-soup-with-python-3')
print(data.status_code)
if (data.status_code != 200):
  text =(data.content)

bs = BeautifulSoup(data.text, 'html.parser')
print(bs.h1)