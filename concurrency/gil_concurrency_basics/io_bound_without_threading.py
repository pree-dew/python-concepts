import requests
import time

def get_page(url):
    return requests.get(url).text

url = 'https://www.google.com'
start = time.time()
get_page(url)
get_page(url)
print('Time taken: ', time.time() - start)
