import os
import sys
import logging
from from_root import from_root
from ner.entity.config_entity import DataIngestionConfig, DataValidationConfig
from ner.utils.common import read_config, create_directories
from ner.exception.exception import CustomException
from ner.constants import *

logger = logging.getLogger(__name__)

class Configuration:
    def __init__(self, config_filepath=CONFIG_FILE_PATH, params_filepath=PARAMS_FILE_PATH):
        try:
            logger.info("Reading Config file")
            self.config = read_config(file_name=config_filepath)
            self.params = read_config(file_name=params_filepath)
            create_directories([self.config[PATH_KEY][ARTIFACTS_KEY]])
        except Exception as e:
            logger.exception(e)
            raise CustomException(e, sys)

    def get_data_ingestion_config(self) -> DataIngestionConfig:
        try:
            dataset_name = self.config[DATA_INGESTION_KEY][DATASET_NAME]
            subset_name = self.config[DATA_INGESTION_KEY][SUBSET_NAME]

            data_store = os.path.join(from_root(), self.config[PATH_KEY][ARTIFACTS_KEY],
                                      self.config[PATH_KEY][DATA_STORE_KEY])
            create_directories([data_store])
            data_ingestion_config = DataIngestionConfig(
                dataset_name=dataset_name,
                subset_name=subset_name,
                data_path=data_store
            )
            return data_ingestion_config
        except Exception as e:
            logger.exception(e)
            raise CustomException(e, sys)

    def get_data_validation_config(self) -> DataValidationConfig:
        try:

            # Load data from the disk location artifacts store
            # os.path.join(from_root(),-- path to the data_store)

            split = self.config[DATA_VALIDATION_KEY][DATA_SPLIT]
            columns = self.config[DATA_VALIDATION_KEY][COLUMNS_CHECK]

            null_value_check = self.config[DATA_VALIDATION_KEY][TYPE_CHECK]
            type_check = self.config[DATA_VALIDATION_KEY][NULL_CHECK]

            data_validation_config = DataValidationConfig(
                dataset=None,
                data_split=split,
                columns_check=columns,
                type_check=type_check,
                null_check=null_value_check
            )
            return data_validation_config
        except Exception as e:
            logger.exception(e)
            raise CustomException(e, sys)
