import os 
import sys
import numpy as np
import pandas as pd

DATA_INGESTION_COLLECTION_NAME              : str   = "NETWORK_SECURITY_DATA"
DATA_INGESTION_DATABASE_NAME                : str   = "ETL_PIPELINE"
DATA_INGESTION_DIR_NAME                     : str   = "data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR            : str   = "feature_store"
DATA_INGESTION_INGESTED_DIR                 : str   = "ingested"
DATA_INGESTION_TRAIN_TEST_SPLIT_RATIO       : float = 0.2


##################################################################################
## Common Constant Variables 
##################################################################################

SCHEMA_FILE_PATH      = os.path.join("data_schema", "schema.yaml")
TARGET_COLUMN         = "Result"
PIPELINE_NAME :  str  = "training_pipeline"
ARTIFACT_DIR  :  str  = "artifacts"
FILE_NAME     :  str  = "phisingData.csv"

TRAIN_FILE_NAME = "train.csv"
TEST_FILE_NAME  = "test.csv"



##################################################################################
## Data Validation Constant Variables 
##################################################################################

DATA_VALIDATION_DIR_NAME               : str    = "data_validation"
DATA_VALIDATION_VALID_DIR              : str    = "validated"
DATA_VALIDATION_INVALID_DIR            : str    = "invalid"
DATA_VALIDATION_DRIFT_REPORT_DIR       : str    = "drift_report"
DATA_VALIDATION_DRIFT_REPORT_FILE_NAME : str    = "report.yaml"
