from dataclasses import dataclass
from src.Constant import *
from datetime import datetime


TIME_STAMP :str = datetime.now().strftime("%m_%d_%Y_%H_%M_%S") 


@dataclass
class TrainingPipelineConfig:
    pipeline_name : str =PIPELINE_NAME
    artifact_dir : str =os.path.join(ARTIFACT_DIR,TIME_STAMP) 
    timestamp : str =TIME_STAMP

training_pipeline_config: TrainingPipelineConfig = TrainingPipelineConfig()

@dataclass
class DataIngestionConfig:
    data_ingestion_dir : str =os.path.join(training_pipeline_config.artifact_dir,DATA_INGESTION_DIR_NAME)
    feature_store_file_path : str = os.path.join(data_ingestion_dir,DATA_INGESTION_FEATURE_STORE ,FILE_NAME)
    training_file_path : str = os.path.join(feature_store_file_path,DATA_INGESTION_INGESTED_DIR,TRAIN_FILE_NAME)
    testing_file_path : str = os.path.join(feature_store_file_path,DATA_INGESTION_INGESTED_DIR,TEST_FILE_NAME)
    train_test_split_ratio : float = DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO
    collection_name : str = DATA_INGESTION_COLLECTION_NAME


@dataclass
class DataTransformationConfig:
    data_transformation_dir : str =os.path.join(training_pipeline_config.artifact_dir,DATA_TRANSFORMATION_COLLECTION_NAME)
    data_transformation_model_file_path : str = os.path.join(data_transformation_dir,DATA_TRANSFORMATION_OBJ_DIR,DATA_PREPROSSING_OBJ_FILE_NAME)
    feature_engiineering_model_file_path : str = os.path.join(data_transformation_dir,FEATURE_ENGEENERING_OBJ_DIR,FEATURE_ENGINEERING_FILE_NAME)
    feature_enginerring_train_data_file_path :str =os.path.join(data_transformation_dir,DATA_TRANSFORMATION_DATA_DIR,TRAIN_FILE_NAME) 
    feature_enginerring_test_data_file_path :str =os.path.join(data_transformation_dir,DATA_TRANSFORMATION_DATA_DIR,TEST_FILE_NAME) 
    transformed_train_data_file_path :str =os.path.join(data_transformation_dir,DATA_TRANSFORMATION_DATA_DIR,TRAIN_FILE_NAME.replace("csv","npy")) 
    transformed_test_data_file_path :str =os.path.join(data_transformation_dir,DATA_TRANSFORMATION_DATA_DIR,TEST_FILE_NAME.replace("csv","npy")) 
    


