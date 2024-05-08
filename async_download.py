import asyncio # for async io operations
import aiohttp # for sync http request submission
import pandas as pd
import time

t1 = time.time()

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
}
responseList = []

async def download_file(url, dest): # use of async since we need to define async funciton and not normal function
    async with aiohttp.ClientSession() as session: # creating a context manager
        async with session.get(url,headers=headers) as response: # creating a async response
            with open(dest, 'wb') as fd:
                while True: # creates an infinite loop, will be False when chunk will be empty and return False and hence loop breaks
                    chunk = await response.content.read(2048) # define the byte/ data packet size - will need to vary and see optimal result based open network/ io etc
                    if not chunk:
                        break
                    fd.write(chunk) # it then writes collective chunk on the file

async def main(): # defining an async function
    df = pd.read_csv('img_list.csv')

    urls = df['url']
    destinations = [i.rsplit('/',1)[1] for i in urls]
    tasks = []
    c=1
    for url, dest in zip(urls, destinations):
        tasks.append(download_file(url, f'data/{dest}')) # collecting all the tasks in a list
        # print(c)
        c+=1
    await asyncio.gather(*tasks) # actually executing all the collected tasks (of a list) in here using async and waits till it completes using await

asyncio.run(main()) # need to write this way to run async function, else it will not wait for the function to complete process.
print(f'Length of chunk: {len(responseList)}')
print(f'Total Time: {time.time() - t1}')