from src.exception import CustomException
from src.logger import logging
from src.Data_acess.uaedata import UAEdata
from src.Constant import *
from src.entity.config_entity import DataIngestionConfig
from src.entity.artifact_entity import DataIngestionArtifact
from sklearn.model_selection import train_test_split

import pandas as pd
import sys,os

class DataIngestion:
    """
    class name : dataingestion
    Description : this class will ingest the data from mongodb

    Output : reutrns csv 
    On Failure : raise CustomException
    """
    def __init__(self,data_ingestion_config : DataIngestionConfig = DataIngestionConfig()):
        """
        : parms data_ingestion_config : configuration fro dataingestion
        """
        try:
            self.data_ingestion_config = data_ingestion_config

        except Exception as e:
            raise CustomException(e,sys)

    def export_data_to_feature_store(self) -> pd.DataFrame:
        """
        This method will export to data into feature store 
        """
        try:
            logging.info("Data Exporting to feature store started")
            uaedata=UAEdata()
            dataframe=uaedata.export_into_df(collection_name=self.data_ingestion_config.collection_name)

            logging.info(f"Found dataframe with shape : {dataframe.shape}")
            feature_store_file_path=self.data_ingestion_config.feature_store_file_path
            dir_path=os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path,exist_ok=True)
            logging.info(f"Saving the exported data into the path :{feature_store_file_path}")

            dataframe.to_csv(dir_path,index=False,header=True)  
            return dataframe
        
        except Exception as e:
            raise CustomException(e,sys)    

    def train_test_split(self , dataframe : pd.DataFrame) -> None:
        """
        This method will be split the dataframe intot train and test 
        """ 
        logging.info("Entering in to Train test split.")

        try:
            train_set,test_set=train_test_split(dataframe,test_size=self.data_ingestion_config.train_test_split_ratio)
            logging.info("Splited the data into traing and test set.")

            dir_path=os.path.dirname(self.data_ingestion_config.training_file_path)
            os.makedirs(dir_path,exist_ok=True)

            logging.info("Exporting the data into traing and test sets.")
            train_set.to_csv(self.data_ingestion_config.training_file_path,index=False,headers=True)
            test_set.to_csv(self.data_ingestion_config.testing_file_path,index=False,headers=True)

            logging.info("Exported into train and test file path.")

        except Exception as e:
            raise CustomException(e,sys) 
        

    def initiate_data_ingestion(self)-> DataIngestionArtifact:
        """
        Method name : initiate data ingestion
        Description : This method initiate the data ingestion

        Output : train and test data artifact
        On faliure : rasie Custom Exception
        """
        logging.info("Entering into DataIngestion Class")

        try:
            dataframe=self.export_data_to_feature_store()
            logging.info("Got the data from the mongoDB")

            self.train_test_split(dataframe)
            logging.info("Dataframe splited into traning and test set.")

            data_ingestion_artifact=DataIngestionArtifact(
                training_file_path=self.data_ingestion_config.training_file_path,
                test_file_path=self.data_ingestion_config.testing_file_path
            )
            logging.info(f"Data Ingestion Completed Successfully. Artifact: {data_ingestion_artifact}")


            return data_ingestion_artifact

        except Exception as e:
            raise CustomException(e,sys)


