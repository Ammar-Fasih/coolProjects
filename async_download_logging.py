import asyncio # for async io operations
import aiohttp # for sync http request submission
import pandas as pd
import time
import logging
import os

input_file = 'sampleCom.csv'
log_file = 'sampleCom_logs.log'
destination_folder = 'sampleCom_data'
col_toDownload = 'URL'

os.makedirs(destination_folder,exist_ok=True)

t1 = time.time()
logging.basicConfig(level=logging.INFO, filename=f'logging/{log_file}', format= '%(asctime)s - %(levelname)s - %(message)s')

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
}
responseList = []

async def download_file(url, dest): # use of async since we need to define async funciton and not normal function
    async with aiohttp.ClientSession() as session: # creating a context manager
        async with session.get(url,headers=headers) as response: # creating a async response
            if response.status != 200:
                logging.error(f'URL: {url} not downloaded | response: {response.status}', exc_info=False)
            try:
                if dest.rsplit('/')[1] != '':
                    with open(dest, 'wb') as fd:
                        while True: # creates an infinite loop, will be False when chunk will be empty and return False and hence loop breaks
                            chunk = await response.content.read(2048) # define the byte/ data packet size - will need to vary and see optimal result based open network/ io etc
                            if not chunk:
                                break
                            fd.write(chunk) # it then writes collective chunk on the file
                else:
                    print(f'{dest} no file name')
            except Exception as e:
                print(f'Error wirting file {dest}:: {e}:: {response.status}')
async def main(): # defining an async function
    df = pd.read_csv(input_file)

    urls = df[col_toDownload]
    destinations = [i.rsplit('/',1)[1] for i in urls]
    tasks = []
    c=1
    for url, dest in zip(urls, destinations):
        tasks.append(download_file(url, f'{destination_folder}/{dest}')) # collecting all the tasks in a list
        # print(c)
        c+=1
    await asyncio.gather(*tasks) # actually executing all the collected tasks (of a list) in here using async and waits till it completes using await

asyncio.run(main()) # need to write this way to run async function, else it will not wait for the function to complete process.
print(f'Length of chunk: {len(responseList)}')
print(f'Total Time: {time.time() - t1}')