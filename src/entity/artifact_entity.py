from dataclasses import dataclass

@dataclass
class DataIngestionArtifact:
    training_file_path : str
    testing_file_path : str


@dataclass
class DataTrasformationArtifact:
    transformed_train_data_file_path : str
    transformed_test_data_file_path : str
    data_transformation_model_file_path :str

@dataclass
class ModelTrainerArtifact:
    model_trained_obj : str 