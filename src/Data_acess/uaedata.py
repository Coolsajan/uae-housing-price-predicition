from src.logger import logging
from src.exception import CustomException
from src.Constant import DATABASE_NAME
from src.configuration.mongodb import MongoDBConnection

import pandas as pd
import sys
from typing import Optional

class UAEdata:
    """
    This class will export the entire mongo collection into pandas df.
    
    """
    def __init__(self):
        try:
            self.mongo_client=MongoDBConnection(database_name=DATABASE_NAME)
        except Exception as e:
            CustomException(e,sys)
    
    def export_into_df(self,collection_name:str,database_name:Optional[str]=None) -> pd.DataFrame:
        """
        This method will export all the collention data in to pandas dataframe
        """
        try:
            logging.info("Dataframe extrection started.")
            if database_name is None:
                collection = self.mongo_client.database[collection_name]
            else :
                collection=self.mongo_client[database_name][collection_name]
            
            dataframe=pd.DataFrame(list(collection.find()))

            if "_id" in dataframe.columns.to_list():
                dataframe=dataframe.drop(columns=["_id"],axis=1)
            logging.info("Dataframe extrection sucessfull..")
            return dataframe
        except Exception as e:
            CustomException(e,sys)

