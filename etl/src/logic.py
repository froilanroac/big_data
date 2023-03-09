import pandas as pd
import pymongo as pm
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URL = os.getenv("MONGO_URL")

def etl(url, fields, mongourl, dbname, collectionname):
    try:
        # extraccion
        data = pd.read_csv(url)

        # transform
        data_to_export = data[fields]

        # conection to mongo
        client = pm.MongoClient(mongourl)
        db = client[dbname]
        collection = db[collectionname]
        

        # load
        data_to_export.reset_index(inplace=True)
        data_dict = data_to_export.to_dict("records")
        collection.insert_many(data_dict)

        print("etl process successfully completed")
    except Exception as e:
        print(f"Unexpected error in etl process -> {e}")

def execute():

    url = "https://raw.githubusercontent.com/fivethirtyeight/covid-19-polls/master/covid_approval_polls.csv"
    fields = ['end_date', 'subject', 'text','party', 'approve', 'disapprove']
    dbname = 'project'
    collectionname = 'covid_approval_polls'

    etl(url, fields, MONGO_URL, dbname, collectionname)

    url = 'https://raw.githubusercontent.com/fivethirtyeight/covid-19-polls/master/covid_concern_polls.csv'
    fields = ['end_date', 'subject', 'very', 'somewhat', 'not_very', 'not_at_all']
    collectionname = 'covid_concern_polls'

    etl(url, fields, MONGO_URL, dbname, collectionname)
