from src.Constant import *
from src.exception import CustomException
from src.logger import logging
from src.entity.artifact_entity import DataIngestionArtifact ,DataTrasformationArtifact,ModelTrainerArtifact
from src.entity.config_entity import ModelTrainerConfig
import os,sys
from src.utils import save_object,evaluate_model,load_numpy_array_data
import numpy as np
import pandas as pd

from sklearn.linear_model import LinearRegression,Ridge ,Lasso
from sklearn.svm import SVR
from sklearn.ensemble import RandomForestRegressor,GradientBoostingRegressor

class ModelTraining:
    def __init__(self,data_transformation_artifact : DataTrasformationArtifact, model_trainer_config : ModelTrainerConfig):
        """
        :param data_ingestion_artifact: Output reference of data ingestion artifact stage
        :param data_transformation_config: Configuration for data transformation
        """

        self.data_transformation_artifact = data_transformation_artifact
        self.model_trainer_config =model_trainer_config

    def initiate_model_trainer(self)  -> ModelTrainerArtifact:
        """
        This will initiate the model traning 
        """
        try:
            logging.info("Initiatzing Model Traning.")
            logging.info("Splting train and test arry into dependent and target feature..")

            train_arr=load_numpy_array_data(file_path=self.data_transformation_artifact.transformed_train_data_file_path)
            test_arr=load_numpy_array_data(file_path=self.data_transformation_artifact.transformed_test_data_file_path)

            X_train,y_train,X_test,y_test = (train_arr[:,:-1],train_arr[:,-1],test_arr[:,:-1],test_arr[:,-1])
            
            logging.info(f"training and test {train_arr.shape},{test_arr.shape}.")
            logging.info(f"training and test {X_train.shape},{y_train.shape}.")
            logging.info(f"training and test {X_test.shape},{y_test.shape}.")

            y_train = y_train.ravel()
            y_test = y_test.ravel()
            models={
                "Linear Regression" : LinearRegression(),
                "Lasso" : Lasso(),
                "Ridge" : Ridge(),
                "SVR" : SVR(),
                "Random Forest Regressor" : RandomForestRegressor(),
                "Gradian Boosting Regressor" : GradientBoostingRegressor()
            }

            logging.info("Model evalutaion started")
            model_report : dict = evaluate_model(X_train,y_train,X_test,y_test,models)

            best_model_name = max(model_report, key=model_report.get)
            best_model_score = model_report[best_model_name]
            best_model = models[best_model_name]

            logging.info(f"Best model found , Model name :{best_model_name}, R2score:{best_model_score}")
            

            model_save_dir=self.model_trainer_config.model_trainer_trained_dir
            os.makedirs(model_save_dir,exist_ok=True)
            save_object(self.model_trainer_config.model_trained_obj,best_model)

            logging.info(f"Best model saved in {model_save_dir}")

            model_trainer_artifact=ModelTrainerArtifact(model_trained_obj=self.model_trainer_config.model_trainer_trained_dir)

            return model_trainer_artifact
        except Exception as e:
            raise CustomException(e,sys)


    