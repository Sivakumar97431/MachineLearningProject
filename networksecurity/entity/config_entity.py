import os
import sys
from datetime import datetime
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.constant import training_pipeline

class TrainingPipelineConfig:
    def __init__(self):
        self.pipeline=training_pipeline.PIPELINE_NAME
        self.artifact=training_pipeline.ARTIFACT_DIR
        self.artifact_dir=os.path.join(self.artifact,f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}")



class DataIngestionConfig:
    def __init__(self,training_pipeline_config:TrainingPipelineConfig):
        self.data_ingestion_dir: str = os.path.join(
            training_pipeline_config.artifact_dir,training_pipeline.DATA_INGESTION_DIR_NAME
        )
        self.feature_store_file_path: str = os.path.join(self.data_ingestion_dir,
                                                  training_pipeline.DATA_INGESTION_FEATURE_STORE_DIR_NAME,
                                                  training_pipeline.FILE_NAME
                                                  )
        self.ingested_train_file_path: str = os.path.join(self.data_ingestion_dir,
                                                         training_pipeline.DATA_INGESTION_INGESTED_DATA_DIR_NAME,
                                                         training_pipeline.TRAIN_FILE_PATH
                                                         )
        self.ingested_test_file_path: str = os.path.join(self.data_ingestion_dir,
                                                         training_pipeline.DATA_INGESTION_INGESTED_DATA_DIR_NAME,
                                                         training_pipeline.TEST_FILE_PATH
                                                         )
        self.train_test_split_ratio: str = training_pipeline.DATA_INGESTION_TRAIN_TEST_SPLIT_RATION
        self.collection_name: str = training_pipeline.DATA_INGESTION_COLLECTION_NAME
        self.database_name: str = training_pipeline.DATA_INGESTION_DATABASE_NAME