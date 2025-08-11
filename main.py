from etl_project.components.data_ingestion import DataIngestion
from etl_project.exception.exception import ETLPipelineException
from etl_project.logging.logger import logging
from etl_project.entity.config_entity import DataIngestionConfig, TrainingPipelineConfig
import sys

if __name__ == "__main__":
    try:
        logging.info("Enter the try block")

        training_pipeline_config = TrainingPipelineConfig()
        config = DataIngestionConfig(training_pipeline_config)
        data_ingestion = DataIngestion(config)

        artifact = data_ingestion.initiate_data_ingestion()

        print(artifact)
    
    except Exception as e:
        raise ETLPipelineException(e, sys) 