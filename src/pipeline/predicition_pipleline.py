from src.logger import logging
from src.exception import CustomException
from src.entity.artifact_entity import DataTrasformationArtifact,ModelTrainerArtifact
from src.entity.config_entity import DataTransformationConfig,ModelTrainerConfig

from src.utils import load_object
import pandas as pd
import numpy as np
import sys

class PredictionData:
    def __init__(self,
                 bedroom : str
                 ,bathroom : int
                 ,area:float 
                 ,address : str
                 ,propert_type : str 
                 ,furnishing : str
                 ,completion : str
                 ,handover : str
                 ,project_name : str
                 ,country : str ="UAE"
                 ,city : str ="Dubai"
                 ,purpose :str ="Sale"):
        try:
            if str(bedroom).isdigit():
                self.bedroom = f"{bedroom} bed"
            else:
                self.bedroom = bedroom
            
            if str(bathroom).isdigit():
                self.bathroom = f'{bathroom} bath'
            else :
                self.bathroom = bathroom

            self.area = f"{area} sqft"
            self.country = country 
            self.city = city
            self.address = address
            self.propert_type = propert_type
            self.purpose = purpose
            self.furnishing = furnishing
            self.completion = completion
            self.handover = handover
            self.project_name =project_name
        
        except Exception as e:
            raise CustomException(e,sys)
        
    def get_data_to_df(self,) ->pd.DataFrame :
        """This method will conver imported data to df.. """
        try:
            logging.info("Converting to df.")
            input_data={
                "bedroom":self.bedroom,
                "bathroom":self.bathroom,
                "area(sqft)":self.area,
                "country":self.country,
                "city":self.city,
                "address":self.address,
                "propert_type":self.propert_type,
                "purpose":self.purpose,
                "furnishing": self.furnishing,
                "completion_status":self.completion,
                "handover":self.handover,
                "project_name":self.project_name
            }

            input_df=pd.DataFrame([input_data])

            return input_df
        
        except Exception as e:
            raise CustomException(e,sys)
        

class PredictPrice:
    def __init__(self,data_transformation_config : DataTransformationConfig = DataTransformationConfig(), model_trainer_config:ModelTrainerConfig = ModelTrainerConfig()):
        
        try:    
            self.data_transformation_config = data_transformation_config
            self.model_trainer_config = model_trainer_config
        except Exception as e:
            raise CustomException(e,sys)
        
    def get_data_scaled_transformed(self,input_df : pd.DataFrame):
        """This method will scaled and tranfrom the input data.."""
        try:
            logging.info("Input data transfromation started...")

            logging.info("loading the fe obj and preprocessor obj...")

            fe_obj_path=self.data_transformation_config.feature_eng_obj
            preprocer_obj_path=self.data_transformation_config.transformed_model_obj

            fe_obj=load_object(fe_obj_path)
            
            preprocessor=load_object(preprocer_obj_path)

            fe_data=fe_obj.transfrom(input_df)

            preproced_data=preprocessor.transform(fe_data)

            return preproced_data

        except Exception as e:
            raise CustomException(e,sys)
        
    def get_price_predicited(self,preprocessdata_data):
        """This will predict the final price.."""
        try:
            logging.info("Price prediciton statreted")
            
            model_obj_path =self.model_trainer_config.model_trained_obj   
            model_obj=load_object(model_obj_path)

            predicted_price=model_obj.predict(preprocessdata_data)            
            actual_price=round(np.exp(predicted_price[0])-1)

            return actual_price

        except Exception as e:
            raise CustomException(e,sys)

    def initiate_price_prediciton(self,input_df):
        """This predict the price"""
        try:
            logging.info("price prediciton initiated")

            scaled_transfromed_data=self.get_data_scaled_transformed(input_df)
            actual_price_prediction=self.get_price_predicited(scaled_transfromed_data)

            return actual_price_prediction

        except Exception as e:
            raise CustomException(e,sys)

        