import requests
import time
from multiprocessing import cpu_count
from multiprocessing.pool import ThreadPool
import pandas as pd

t0 = time.time()

def download_url(args):
    t0 = time.time()
    url, fn = args[0], args[1]
    try:
        r = requests.get(url)
        with open(f'data2/{fn}', 'wb') as f:
            f.write(r.content)
        return(url, time.time() - t0)
    except Exception as e:
        print('Exception in download_url():', e)

def download_parallel(args):
    cpus = cpu_count()
    results = ThreadPool(cpus - 1).imap_unordered(download_url, args)
    for result in results:
        print('url:', result[0], 'time (s):', result[1])

df = pd.read_csv('links2.csv')
urls = df['url']
destinations = [i.rsplit('/',1)[1] for i in urls]

inputs = zip(urls,destinations)

download_parallel(inputs)

print(f'Total download time: {time.time() - t0}')

# Total download time: 43.9612591266632
