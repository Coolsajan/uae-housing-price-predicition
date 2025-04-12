import os ,datetime

#MONGO DB RELATED CONSTATNT#
DATABASE_NAME = "UAE-housing"
COLLECTION_NAME = "uaedata"
CONNECTION_URL = "UAEHOUSING"

COLUMN_TO_DROP = ['country','city','purpose']

PIPELINE_NAME : str = "uaehosuingpredicition"
ARTIFACT_DIR : str = "artifact"

MODEL_FILE_NAME = "model.pkl"

TARGET_COLUMN = "price"

DATA_PREPROSSING_OBJ_FILE_NAME = "preprocessing.pkl"
FEATURE_ENGINEERING_FILE_NAME = "feature_eng.pkl"

FILE_NAME = "uae-housing_dataset"
TRAIN_FILE_NAME = "train.csv"
TEST_FILE_NAME = "test.csv"

"""
DATA INGESTIOIN RELATED CONSTANT
"""
DATA_INGESTION_COLLECTION_NAME = "uaedata"
DATA_INGESTION_DIR_NAME : str ="Data_Ingestion"
DATA_INGESTION_FEATURE_STORE : str ="feature_store"
DATA_INGESTION_INGESTED_DIR : str ="ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO : float = 0.3


"""
DATA TRANSFORMATION RELATED CONSTANT
"""
DATA_TRANSFORMATION_COLLECTION_NAME : str = "Data_transformation"
DATA_TRANSFORMATION_OBJ_DIR : str = "preprocessing"
FEATURE_ENGEENERING_DATA_DIR :str ="feature_engeerring"
DATA_TRANSFORMATION_DATA_DIR : str ="transformation"
DATA_TRANFORMATION_MODEL_OBJ :str = "transform_obj"



