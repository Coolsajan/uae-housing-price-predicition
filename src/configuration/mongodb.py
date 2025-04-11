from src.exception import CustomException
from src.logger import logging
from src.Constant import DATABASE_NAME,CONNECTION_URL

import os,sys
import pymongo
import pandas as pd

class MongoDBConnection:
    """
    Class name : mongo connection
    Describition : This method will connect the mongo python with mongo atlas server.

    Output : establish the mongoDB connection
    On Faliure : raise Custom Exception
    """
    client = None
    def __init__(self,database_name=DATABASE_NAME):
        try:
            if MongoDBConnection.client is None :
                connection_url=os.getenv(CONNECTION_URL)

                if connection_url is None :
                    raise Exception (f"Envirmonet key: {CONNECTION_URL} is not set.")
                
                MongoDBConnection.client = pymongo.MongoClient(connection_url)
            
            self.client = MongoDBConnection.client
            self.database = self.client[database_name]
            self.database_name = database_name
            logging.info("MongoDB connection established.")

        except Exception as e:
            CustomException(e,sys)
        
        




        

