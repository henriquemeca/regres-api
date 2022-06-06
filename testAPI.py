from ast import arg
from matplotlib.ft2font import BOLD
import requests
import pandas as pd
import sys
import argparse

def parse_args(args):
    """Parse command line flags"""
    parser=argparse.ArgumentParser(
    description='''This script provides 2 execution modes to load data from the API https://reqres.in/api/''',
    epilog="""Developer:Henrique Brito Silva
    Date:18/05/2022""")
    parser.add_argument('-m','--mode', type=int,required=True, choices=range(1,3), help='''To execute the script specify the execution mode.
                        1: Fetches the API with specfic records per page and saves all data in a CSV file. Use -r to 
                        set the records per page and -f to set the file name. 2: Fetches an ID on the API and prints its name.Use -i to set the fetched ID ''')
    parser.add_argument('-r','--records', type=int, default=12, help='Specify the number of records per page requested to the API  (default=12)')
    parser.add_argument('-f','--fileName', type=str, default='users.csv', help='Specify the file name for saving data (default=users.csv)')
    parser.add_argument('-i','--id', type= int, default=-1, help='Prints the name of a specified ID (default=-1)')
    
    return parser.parse_args(args)

url = 'https://reqres.in/api/'
endpoint = 'users'

class reqresApi:
    def __init__(self,url,endpoint):
        self.url = url
        self.endpoint = endpoint

    def getJson(self,page=None,records=None):
        adress = f'{self.url}{self.endpoint}?page={page}&per_page={records}'
        r = requests.get(adress)
        return r.json()

    def getAllPages(self,records=None):
        r = self.getJson(records=records)
        data = r['data']
        totalPages = r['total_pages']
        print('Total pages to get',totalPages)
        for page in range(2,totalPages+1):
            print('Getting page:',page)
            data+=self.getJson(page,records)['data']
        print('Finished')
        return data

    def saveDataCsv(self,data=None,fileName='users.csv'):
        if data is not None:
            pd.DataFrame.from_records(data).to_csv(fileName)
            print('File ',fileName,' created')
        else:
            print('Data is none, no file was created')
            pass
    
    def getUserById(self,id=-1):
        adress = f'{self.url}{self.endpoint}?id={id}'
        r = requests.get(adress)
        return r.json()


if __name__ == "__main__":
    args=parse_args(sys.argv[1:])
    api = reqresApi(url,endpoint)
    if args.mode == 1:
        api.saveDataCsv(api.getAllPages(args.records),args.fileName)
    elif args.mode == 2:
        r = api.getUserById(args.id)
        name = 'Id not found' if not r else ' '.join([r['data']['first_name'],r['data']['last_name']])
        print(name)
    else:
        print('Invalid mode')