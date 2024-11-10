from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
import os
import sys
from networksecurity.entity.config_entity import DataIngestionConfig
from networksecurity.entity.artifact_entity import DataIngestionArtifact
import numpy as np
import pandas as pd
import pymongo
from sklearn.model_selection import train_test_split
from dotenv import load_dotenv
load_dotenv()

DATABASE_URL=os.getenv("MONGO_DB_URL")

class DataIngestion:
    def __init__(self,data_ingestion_config:DataIngestionConfig):
        try:
            self.data_ingestion_config=data_ingestion_config
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    def export_collection_as_dataframe(self)->pd.DataFrame:
        try:
            database_name=self.data_ingestion_config.database_name
            collection_name=self.data_ingestion_config.collection_name
            mongo_client=pymongo.MongoClient(DATABASE_URL)
            collection=mongo_client[database_name][collection_name]
            dataframe=pd.DataFrame(list(collection.find()))
            if "_id" in dataframe.columns.to_list():
                dataframe=dataframe.drop(columns=['_id'],axis=1)
            dataframe.replace('na',np.nan,inplace=True)
            return dataframe
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    def export_dataframe_to_feature_store(self,dataframe: pd.DataFrame)->pd.DataFrame:
        try:
            feature_store_file_path=self.data_ingestion_config.feature_store_file_path
            dir_path=os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path,exist_ok=True)
            dataframe.to_csv(feature_store_file_path,index=False,header=True)
            return dataframe
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    def split_data_as_train_test(self,dataframe: pd.DataFrame):
        try:
            train_data,test_data=train_test_split(
                dataframe,test_size=self.data_ingestion_config.train_test_split_ratio
            )
            logging.info('dataframe is splitted into train data and test data')
            ingested_dir=os.path.dirname(self.data_ingestion_config.ingested_train_file_path)
            os.makedirs(ingested_dir,exist_ok=True)
            logging.info("exporting train data and test data to ingested dir")
            train_data.to_csv(self.data_ingestion_config.ingested_train_file_path,index=False,header=True)
            test_data.to_csv(self.data_ingestion_config.ingested_test_file_path,index=False,header=True)
            logging.info("exported train and test data to ingested dir")
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    def initiate_data_ingestion(self):
        try:
            dataframe=self.export_collection_as_dataframe()
            dataframe=self.export_dataframe_to_feature_store(dataframe)
            self.split_data_as_train_test(dataframe=dataframe)
            data_ingestion_artifact=DataIngestionArtifact(
                trained_file_path=self.data_ingestion_config.ingested_train_file_path,
                test_file_path=self.data_ingestion_config.ingested_test_file_path
            )
            return data_ingestion_artifact
        except Exception as e:
            raise NetworkSecurityException(e,sys)
            