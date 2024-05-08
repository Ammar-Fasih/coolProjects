import requests
import pandas as pd
from globalFunction import *

# Define the filepath
sourceFile_path = 'sampleCom.csv'
status = None
log_filename = 'sampleCom_logs.csv'
col_toDownload = 'URL'
download_folder = 'sampleCom_data/'

# Read csv and convert into dataframe(df)
df = pd.read_csv(sourceFile_path)

# Iterate dataframe by each row
for index,i in df.iterrows():

    # Extract docID, URL and filename
    link = i[col_toDownload]
    
    download_filename = link.rsplit('/',1)[1]

    # Search for download folder and create if not exist
    if os.path.exists(download_folder) == False:
        os.makedirs(download_folder)

    response = requests.get(link)

    # If response is successfull, download and save file
    if response.status_code == 200:
        download_filePath = download_folder + download_filename
        open(download_filePath,'wb').write(response.content)
        status = 'Success'
    else:
        status = 'Failure'

    # Log all details regarding the download process
    fileDownload_log(id, status, link,download_filename,log_filename)
    print(f'{index}  {response.status_code} done')

print('All Done')