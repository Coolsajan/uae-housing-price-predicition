from dataclasses import dataclass
from src.Constant import *
from datetime import datetime



@dataclass
class TrainingPipelineConfig:
    pipeline_name: str = PIPELINE_NAME
    artifact_dir: str = ARTIFACT_DIR


training_pipeline_config: TrainingPipelineConfig = TrainingPipelineConfig()


@dataclass
class DataIngestionConfig:
    data_ingestion_dir: str = os.path.join(training_pipeline_config.artifact_dir, DATA_INGESTION_DIR_NAME)   
    feature_store_dir: str = os.path.join(data_ingestion_dir, DATA_INGESTION_FEATURE_STORE)
    feature_store_file_path: str = os.path.join(feature_store_dir, FILE_NAME)
    ingested_dir: str = os.path.join(feature_store_dir, DATA_INGESTION_INGESTED_DIR)
    training_file_path: str = os.path.join(ingested_dir, TRAIN_FILE_NAME)
    testing_file_path: str = os.path.join(ingested_dir, TEST_FILE_NAME)
    train_test_split_ratio: float = DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO
    collection_name: str = DATA_INGESTION_COLLECTION_NAME



@dataclass
class DataTransformationConfig:
    data_transformation_dir:str = os.path.join(training_pipeline_config.artifact_dir,DATA_TRANSFORMATION_COLLECTION_NAME)
    transformed_train_data_file_path :str = os.path.join(data_transformation_dir,DATA_TRANSFORMATION_DATA_DIR,TRAIN_FILE_NAME.replace("csv","npy")) 
    transformed_test_data_file_path :str = os.path.join(data_transformation_dir,DATA_TRANSFORMATION_DATA_DIR,TEST_FILE_NAME.replace("csv","npy"))
    transformed_model_obj :str =os.path.join(data_transformation_dir,DATA_TRANSFORMATION_DATA_DIR,DATA_TRANFORMATION_MODEL_OBJ,DATA_PREPROSSING_OBJ_FILE_NAME)

    feature_eng_train_data_file_path :str = os.path.join(data_transformation_dir,FEATURE_ENGEENERING_DATA_DIR,TRAIN_FILE_NAME) 
    feature_eng_test_data_file_path :str = os.path.join(data_transformation_dir,FEATURE_ENGEENERING_DATA_DIR,TEST_FILE_NAME)
    feature_eng_obj :str = os.path.join(data_transformation_dir,FEATURE_ENGEENERING_DATA_DIR,DATA_TRANFORMATION_MODEL_OBJ,FEATURE_ENGINEERING_FILE_NAME)


@dataclass
class ModelTrainerConfig:
    model_trainer_dir : str = os.path.join(training_pipeline_config.artifact_dir,MODEL_TRANING_DIR)
    model_trainer_trained_dir : str = os.path.join(model_trainer_dir,MODEL_TRAINER_TRAINED_DIR)
    model_trained_obj : str = os.path.join(model_trainer_trained_dir,MODEL_FILE_NAME)

