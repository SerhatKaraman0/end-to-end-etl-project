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

TARGET_COLUMN         = "Result"
PIPELINE_NAME :  str  = "training_pipeline"
ARTIFACT_DIR  :  str  = "artifacts"
FILE_NAME     :  str  = "phisingData.csv"

TRAIN_FILE_NAME = "train.csv"
TEST_FILE_NAME  = "test.csv"
