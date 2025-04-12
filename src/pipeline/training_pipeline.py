from src.logger import logging
from src.exception import CustomException

from src.entity.artifact_entity import DataIngestionArtifact,DataTrasformationArtifact,ModelTrainerArtifact

from src.entity.config_entity import DataIngestionConfig,DataTransformationConfig,ModelTrainerConfig

from src.components.data_ingestion import DataIngestion
from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTraning

import os,sys

class ModelTraining:
    def __init__(self):
        self.data_ingestion_config = DataIngestionConfig()
        self.data_transformation_config = DataTransformationConfig()
        self.model_trainer_config = ModelTrainerConfig()

    def start_data_ingestion(self) -> DataIngestionArtifact:
        """This method is responsible for data ingestion process in traning pipeline"""
        try:
            logging.info("Data ingestion traning pipeline started")
            logging.info("Acessing MongoDB for data extraction.")

            data_ingestion=DataIngestion(data_ingestion_config=self.data_ingestion_config)
            data_ingestion_artifacts=data_ingestion.initiate_data_ingestion()

            logging.info("Dataframe extracted and Dataingestion completed..")

            return data_ingestion_artifacts
        
        except Exception as e:
            raise CustomException(e,sys)
        
    def start_data_transformation(self,data_ingestion_artifacts:DataIngestionArtifact) -> DataTrasformationArtifact:
        """"This method is responsible for data transformation section in traning pipleline.."""
        try:
            logging.info("Entering into data transformation section..")
            data_transforamtion=DataTransformation(data_transformation_config=self.data_transformation_config,
                                                   data_ingestion_artifact=data_ingestion_artifacts)
            
            data_transformation_artifacts=data_transforamtion.initiate_data_transfromation()
            logging.info("Data transformation Completed...")

            return data_transformation_artifacts

        except Exception as e:
            raise CustomException(e,sys)
        
    def start_model_trainer(self,data_transformation_artifacts : DataTrasformationArtifact) -> ModelTrainerArtifact:
        """"This method is responsible for model trainer section in traning pipleline.."""
        try:
            model_trainer=ModelTraning(data_transformation_artifact=data_transformation_artifacts,model_trainer_config=self.model_trainer_config)

            model_trainer_artifacts=model_trainer.initiate_model_trainer()

            return model_trainer_artifacts          
        except Exception as e:
            raise CustomException(e,sys)
        


    def run_piple(self,) -> None:
        """This method of Trainpipleine is responsible to complete pipeline"""
        try:
            data_ingestion_artifact = self.start_data_ingestion()

            data_transformation_artifact=self.start_data_transformation(data_ingestion_artifacts=data_ingestion_artifact)

            model_trainer_artifact=self.start_model_trainer(data_transformation_artifacts=data_transformation_artifact)

            
        except Exception as e:
            raise CustomException(e,sys)
