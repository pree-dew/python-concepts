import requests
import threading
import time

def get_page(url):
    return requests.get(url).text

url = 'https://www.google.com'
start = time.time()
thread1 = threading.Thread(target=get_page, args=(url,))
thread2 = threading.Thread(target=get_page, args=(url,))

thread1.start()
thread2.start()

thread1.join()
thread2.join()

print('Time taken: ', time.time() - start)
