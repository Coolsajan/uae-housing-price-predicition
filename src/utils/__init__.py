import pandas as pd
from src.exception import CustomException
from src.logger import logging
import os ,sys
import numpy as np
import pickle


from sklearn.metrics import r2_score

def save_numpy_array_data(file_path: str, array: np.array):
    """
    Save numpy array data to file
    file_path: str location of file to save
    array: np.array data to save
    """
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, 'wb') as file_obj:
            np.save(file_obj, array)
    except Exception as e:
        raise CustomException(e, sys) from e


def load_numpy_array_data(file_path: str) -> np.array:
    """
    load numpy array data from file
    file_path: str location of file to load
    return: np.array data loaded
    """
    try:
        with open(file_path, 'rb') as file_obj:
            return np.load(file_obj,allow_pickle=True)
    except Exception as e:
        raise CustomException(e, sys) from e


def save_object(file_path: str, obj: object) -> None:
    logging.info("Entered the save_object method of utils")

    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "wb") as file_obj:
            pickle.dump(obj, file_obj)

        logging.info("Exited the save_object method of utils")

    except Exception as e:
        raise CustomException(e, sys) from e

def load_object(file_path: str) -> object:
    logging.info("Entered the load_object method of utils")

    try:

        with open(file_path, "rb") as file_obj:
            obj = pickle.load(file_obj,)

        logging.info("Exited the load_object method of utils")

        return obj

    except Exception as e:
        raise CustomException(e, sys) from e
    
    
def evaluate_model(X_train, y_train, X_test, y_test, models):
    try:
        report = {}
        for name, model in models.items():
            model.fit(X_train, y_train)
            y_test_pred = model.predict(X_test)
            test_model_score = r2_score(y_test, y_test_pred)
            report[name] = test_model_score
        return report

    except Exception as e:
        raise CustomException(e, sys)
    