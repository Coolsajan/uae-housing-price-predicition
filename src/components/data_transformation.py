from src.Constant import *
from src.exception import CustomException
from src.logger import logging
from src.entity.artifact_entity import DataIngestionArtifact ,DataTrasformationArtifact
from src.entity.config_entity import DataTransformationConfig
import os,sys
from src.utils import save_numpy_array_data,save_object

from dataclasses import dataclass
from sklearn.preprocessing import MinMaxScaler,StandardScaler,OneHotEncoder
from sklearn.compose import ColumnTransformer
import pandas as pd
import numpy as np


class FeatureEngineering:
    def __init__(self):
        logging.info("**--Feature Enginerring started--**")
    
    def clean_bedroom(self,bedroom:pd.Series):
        """this will correct the data of Bedroom sereis"""
        bedroom=bedroom.apply(lambda x:x.lower())
        for i in range(len(bedroom)):
            if "bed" in bedroom[i]:
                bedroom[i]=bedroom[i].split()[0]
            elif "studio" in bedroom[i]:
                bedroom[i]=float(0.5)

        return bedroom.astype(float)  


    def quater_to_float(self,handover_data):
        """this will convert your handover data into float"""
        q,y=handover_data.split()
        q=int(q[1])
        return  int(y) + (q-1)*0.25
    
    def rearrange_address(self,address,vc_address):
        """This method will encode the address """
        result=vc_address.get(address)
        if result <=5:
            address ="others"
        else :
            pass
        return address
    
    def transform_data(self,df: pd.DataFrame):
        """This Method will perform  the feature engeenering part"""
        try:
            logging.info("Entering Feature engineering...")
            df.drop(columns=COLUMN_TO_DROP,axis=1,inplace=True)
            logging.info(f"Dropped {COLUMN_TO_DROP}. ")
            df=df[df['area(sqft)']!=13149888.0]
            df=df[df['propert_type']!="residential building"]

            df["bedroom"]=self.clean_bedroom(df["bedroom"])
            logging.info("Bedroom  data corrected.")

            df['handover']=df['handover'].apply(self.quater_to_float)
            logging.info("Handover data corrected.")

            df['address']=df['address'].str.replace(" ","")
            vc_address=dict(df['address'].value_counts())

            df['address'] = df['address'].apply(lambda x: self.rearrange_address(x, vc_address=vc_address))

            df['area(sqft)']=(df['area(sqft)'].str.split().str[0]).str.replace(",","").astype(float)
            df['area(sqft)']=np.log(df['area(sqft)']+1)
                              
            logging.info("area data corrected.")

            df['price']=df['price'].str.replace(",","").astype(int)
            df['price']=np.log(df['price']+1)
            logging.info("Price data corrected..")

            df['bathroom']=(df['bathroom'].str.split().str[0]).astype(int)
            logging.info("Bathroom data corrected.")


            maping_furnishing={'Unfurnished':0,'Furnished':1}
            maping_completion_status={'Off-Plan':0,'Ready':1}

            df['furnishing']=df['furnishing'].map(maping_furnishing)
            df['completion_status']=df['completion_status'].map(maping_completion_status)
            logging.info("Furnishing,Completion status data mapped..")

            project_maping=df['project_name'].value_counts()
            df['project_name']=df['project_name'].map(project_maping)

            df['propert_type'].replace({"villa compound":"villa"},inplace=True)

            logging.info("Feature Engineering completed..")
            return df

        except Exception as e:
            raise CustomException(e,sys)
    
    def fit_transform(self, X, y=None):
        return self.transfrom(X, y)

    def transfrom(self,X:pd.DataFrame,y:None):
        try:
            dataframe=self.transform_data(X)

            return dataframe
        except Exception as e:
            raise CustomException(e,sys)
        

class DataTransformation:
    """
    :param data_ingestion_artifact: Output reference of data ingestion artifact stage
    :param data_transformation_config: configuration for data transformation
    """
    def __init__(self,data_transformation_config:DataTransformationConfig=DataTransformationConfig(),
                data_ingestion_artifact:DataIngestionArtifact=DataIngestionArtifact()):
        """
        : parms data_transformation_config : configuration for datatransformation
        """
        try:
            self.data_transformation_config = data_transformation_config
            self.data_ingestion_artifact = data_ingestion_artifact
        except Exception as e:
            raise CustomException(e,sys)
        
    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise CustomException(e, sys)
        
    def get_data_transfromation_obj(self):
        """This method will retrun data transformation object."""
        try:
            ohe_column=["address","propert_type"]
            minmax_column=["bedroom","bathroom","handover","project_name"]
            ct=ColumnTransformer([
                ("OHE",OneHotEncoder(sparse_output=True,handle_unknown="ignore"),ohe_column),
                ("minmax_scaler",MinMaxScaler(feature_range=(0,1)),minmax_column)
            ],remainder="passthrough")

            logging.info("Data Transformation obj created.")
            return ct
            
        except Exception as e:
            raise CustomException(e,sys)
        
    def get_feature_engineering_obj(self):
        """This method will help us to get the feature engineering obj."""
        try:
            feature_engineering_obj=FeatureEngineering()

            logging.info("Feature Engineering obj created..")
            return feature_engineering_obj
        except Exception as e:
            raise CustomException(e,sys)
        
    def initiate_data_transfromation(self,) -> DataTrasformationArtifact:
        """
        Method Name :   initiate_data_transformation
        Description :   This method initiates the data transformation component for the pipeline 
        
        Output      :   data transformer steps are performed and preprocessor object is created  
        On Failure  :   Write an exception log and then raise an exception
        """
        try:
            logging.info("Data Transformation Started")
            train_data=DataTransformation.read_data(file_path=self.data_ingestion_artifact.training_file_path)
            test_data=DataTransformation.read_data(file_path=self.data_ingestion_artifact.test_file_path)

            logging.info("Training and Testing Data obtained")
            logging.info("Feature Engineering started.")

            fe_obj=self.get_feature_engineering_obj()
            logging.info("Feature Enginnering obj obtained.")
            train_data=fe_obj.fit_transform(train_data)
            test_data=fe_obj.transfrom(test_data)

            dir_path=dir_path = self.data_transformation_config.data_transformation_dir
            os.makedirs(dir_path,exist_ok=True)

            train_data.to_csv(self.data_transformation_config.feature_enginerring_train_data_file_path,index=False)
            test_data.to_csv(self.data_transformation_config.feature_enginerring_test_data_file_path,index=False)


            X_train=train_data.drop(columns=[TARGET_COLUMN],axis=1)
            y_train=train_data[TARGET_COLUMN]

            X_test=test_data.drop(columns=[TARGET_COLUMN],axis=1)
            y_test=test_data[TARGET_COLUMN]

            logging.info("Input feature and target feature seperated.")

            preprocessor=self.get_data_transfromation_obj()

            X_train=preprocessor.fit_transform(X_train)
            X_test=preprocessor.transform(X_test)

            logging.info("X_train,X_test transfromed.")

            train_arr=np.c_(X_train,np.array(y_train))
            test_arr=np.c_(X_test,np.array(y_test))

            logging.info("training and test arr obtained.")

            save_numpy_array_data(file_path=self.data_transformation_config.transformed_train_data_file_path,array=train_arr)
            save_numpy_array_data(file_path=self.data_transformation_config.transformed_test_data_file_path,array=test_arr)

            logging.info("Train and test arr saved....")

            save_object(file_path=self.data_transformation_config.feature_engiineering_model_file_path,obj=fe_obj)
            save_object(file_path=self.data_transformation_config.data_transformation_model_file_path,obj=preprocessor)

            logging.info("Saved FE and preprocess obj ....")

            data_transformation_artifact=DataTrasformationArtifact(
                transformed_train_data_file_path=self.data_transformation_config.transformed_train_data_file_path,
                transformed_test_data_file_path=self.data_transformation_config.transformed_test_data_file_path,
                data_transformation_model_file_path=self.data_transformation_config.data_transformation_model_file_path
            )
            return data_transformation_artifact
        except Exception as e:
            raise CustomException(e,sys)

    

