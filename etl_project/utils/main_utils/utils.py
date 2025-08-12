from etl_project.exception.exception import ETLPipelineException
from etl_project.logging.logger import logging
import numpy as np
import os
import sys
import dill
import pickle
import yaml


def read_yaml_file(file_path: str) -> dict:
    try:
        with open(file_path, "rb") as file:
            return yaml.safe_load(file)
    except Exception as e:
        raise ETLPipelineException(e, sys) 

def write_yaml_file(file_path: str, content: object, replace: bool = False) -> None:
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w") as file:
            yaml.dump(content, file)

    except Exception as e:
        raise ETLPipelineException(e, sys)


def save_numpy_array_data(file_path: str, array: np.array):
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, "wb") as file:
            np.save(file, array)

    except Exception as e:
        raise ETLPipelineException(e, sys)
    
def save_object(file_path: str, obj: object):
    try:
        logging.info("Entered save_object method in /utils/main_utils/utils.py")
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "wb") as file:
            pickle.dump(obj, file)
        logging.info("Exited save_obj method")
    except Exception as e:
        raise ETLPipelineException(e, sys)
