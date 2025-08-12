from etl_project.components.data_validation import DataValidation
from etl_project.components.data_ingestion import DataIngestion
from etl_project.exception.exception import ETLPipelineException
from etl_project.logging.logger import logging
from etl_project.entity.config_entity import DataIngestionConfig, TrainingPipelineConfig, DataValidationConfig
import sys

if __name__ == "__main__":
    try:
        logging.info("Enter the try block")

        training_pipeline_config = TrainingPipelineConfig()
        data_ingestion_config = DataIngestionConfig(training_pipeline_config)
        data_ingestion = DataIngestion(data_ingestion_config)

        logging.info("Initiate Data Ingestion")
        data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
        print(data_ingestion_artifact)
        data_validation_config = DataValidationConfig(training_pipeline_config)
        data_validation = DataValidation(data_ingestion_artifact, data_validation_config)
        
        logging.info("Initiate Data Validation")
        data_validation_artifact = data_validation.initiate_data_validation()
        logging.info("Data validation completed")
        print(data_validation_artifact)

    
    except Exception as e:
        raise ETLPipelineException(e, sys) 