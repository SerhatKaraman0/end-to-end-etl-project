from etl_project.components.data_validation import DataValidation
from etl_project.components.data_ingestion import DataIngestion
from etl_project.components.data_transformation import DataTransformation
from etl_project.exception.exception import ETLPipelineException
from etl_project.logging.logger import logging
from etl_project.entity.config_entity import (DataIngestionConfig, 
                                              TrainingPipelineConfig, 
                                              DataValidationConfig, 
                                              DataTransformationConfig)
import sys

if __name__ == "__main__":
    try:
        logging.info("Enter the try block")

        training_pipeline_config = TrainingPipelineConfig()
        data_ingestion_config = DataIngestionConfig(training_pipeline_config)
        data_ingestion = DataIngestion(data_ingestion_config)
        data_transformation_config = DataTransformationConfig(training_pipeline_config)

        logging.info("Initiate Data Ingestion")
        data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
        print(data_ingestion_artifact)
        data_validation_config = DataValidationConfig(training_pipeline_config)
        data_validation = DataValidation(data_ingestion_artifact, data_validation_config)
        
        logging.info("Initiate Data Validation")
        data_validation_artifact = data_validation.initiate_data_validation()
        logging.info("Data validation completed")
        print(data_validation_artifact)


        logging.info("Initiate Data Transformation")
        if data_validation_artifact is None:
            raise ETLPipelineException("Data validation artifact is None. Cannot proceed to data transformation.", sys)
        data_transformation = DataTransformation(data_validation_artifact, data_transformation_config)
        data_transformation_artifact = data_transformation.initiate_data_transformation()
        logging.info("Data Transformation Completed")
        print(data_transformation_artifact)

    
    except Exception as e:
        raise ETLPipelineException(e, sys) 