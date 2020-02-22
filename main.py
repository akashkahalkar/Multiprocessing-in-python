import requests
from multiprocessing.pool import ThreadPool
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup
from threading import Thread
from queue import Queue
import os
from time import time
from functools import partial

headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'} 
cookies = {}
urls = []
folderName = 'XKCD'
Folderpath = os.path.join(os.getcwd(), folderName)

for i in range(100, 200):
    url = 'https://xkcd.com/'+str(i)+"/"
    urls.append(url)

def get_XKCD_Comic_Image_url(url):
    try:
        XKCD_page = requests.get(url, headers = headers, cookies = cookies)
        XKCD_page.raise_for_status()
    except:
        print("Error occured while getting image data")
        SystemExit(1)

    XKCD_soup = BeautifulSoup(XKCD_page.content, 'html.parser')
    comic_src = XKCD_soup.find(id="comic").img['src']
    if not comic_src.startswith("http:"):
        return "http:" + comic_src
    else:
        return comic_src 
    

def download_XKCD_Comic(page_url):
    comic_image_url = get_XKCD_Comic_Image_url(page_url)    
    file_name_index = comic_image_url.rfind("/") + 1
    file_name = comic_image_url[file_name_index:]
    filePath = os.path.join(Folderpath, file_name)
    r = requests.get(comic_image_url, stream=True)
    if r.status_code == 200:
        with open(filePath, 'wb') as f:
            for data in r:
                f.write(data)

class DownloadWorker(Thread):
    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            # Get the work from the queue and expand the tuple
            link = self.queue.get()
            try:
                download_XKCD_Comic(link)
            finally:
                self.queue.task_done()

def folderCheck():
    path = os.path.join(os.getcwd(), folderName)
    if not os.path.exists(path):
        os.mkdir(folderName)

def CreateQueues(num):
    queue = Queue()
    # Create 8 worker threads
    for _ in range(num):
        worker = DownloadWorker(queue)
        # Setting daemon to True will let the main thread exit even though the workers are blocking
        worker.daemon = True
        worker.start()
    # Put the tasks into the queue as a tuple
    for link in urls:
        queue.put((link))
    # Causes the main thread to wait for the queue to finish processing all the tasks
    queue.join()

def downloadWithoutQueue():
    for file_url in urls:
        download_XKCD_Comic(file_url)

def UsingConcurrentFuture():
    #using thread pool executioner
    with ThreadPoolExecutor() as executor:
        executor.map(download_XKCD_Comic, urls)
        

def main():   
    ts = time()
    folderCheck()
    #CreateQueues(10)
    #downloadWithoutQueue()
    UsingConcurrentFuture()
    print("Time taken: ", time() - ts)

if __name__ == '__main__':
    main()