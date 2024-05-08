import pandas as pd
import time
import requests

t0 = time.time()
error_urls = []

def download_url(args):
    t0 = time.time()
    url, fn = args[0], args[1]
    try:
        headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
}
        r = requests.get(url,headers=headers)
        if r.status_code != 200:
            # error_urls.append(url)
            print(r,url)
        with open(f'data/{fn}', 'wb') as f:
            f.write(r.content)
        return(url, time.time() - t0)
    except Exception as e:
        print('Exception in download_url():', e)

df = pd.read_csv('img_list.csv')
urls = df['url']
# urls = ['https://www.speednik.com/files/2022/01/coyote-powered-and-gunnin-for-9s-bondo-bird-is-a-purists-nightmare-2022-01-27_22-29-54_483752-1440x1080.jpeg']
destinations = [i.rsplit('/',1)[1] for i in urls]
inputs = zip(urls,destinations)

for input in inputs:
    download_url(input)

print(f'Total download time: {time.time() - t0}')
print(error_urls)
print(len(error_urls))  

# Total download time: 107.41932320594788
