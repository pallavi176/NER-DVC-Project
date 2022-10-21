import os
import sys
import logging
from from_root import from_root
from ner.entity.config_entity import DataIngestionConfig
from ner.utils.common import read_config
from ner.exception.exception import CustomException
from ner.constants import *


logger = logging.getLogger(__name__)


class Configuration:
    def __init__(self):
        try:
            logger.info("Reading Config file")
            self.config = read_config(file_name=CONFIG_FILE_NAME)
        except Exception as e:
            logger.exception(e)
            raise CustomException(e, sys)

    def get_data_ingestion_config(self) -> DataIngestionConfig:
        try:
            dataset_name = self.config[DATA_INGESTION_KEY][DATASET_NAME]
            subset_name = self.config[DATA_INGESTION_KEY][SUBSET_NAME]

            data_store = os.path.join(from_root(), self.config[PATH_KEY][ARTIFACTS_KEY],
                                      self.config[PATH_KEY][DATA_STORE_KEY])

            data_ingestion_config = DataIngestionConfig(
                dataset_name=dataset_name,
                subset_name=subset_name,
                data_path=data_store
            )
            return data_ingestion_config
        except Exception as e:
            logger.exception(e)
            raise CustomException(e, sys)
