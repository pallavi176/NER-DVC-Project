import os
import sys
import logging
from from_root import from_root
from transformers import AutoTokenizer, AutoConfig
from ner.entity.config_entity import (DataIngestionConfig, DataValidationConfig, 
DataPreprocessingConfig, ModelTrainConfig, PredictPipelineConfig)
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

    def get_data_preprocessing_config(self) -> DataPreprocessingConfig:
        try:
            model_name = self.params[BASE_MODEL_CONFIG][BASE_MODEL_NAME]
            tags = self.params[DATA_PREPROCESSING_KEY][NER_TAGS_KEY]

            index2tag = {idx: tag for idx, tag in enumerate(tags)}
            tag2index = {idx: tag for idx, tag in enumerate(tags)}

            tokenizer = AutoTokenizer.from_pretrained(self.params[BASE_MODEL_CONFIG][BASE_MODEL_NAME])

            data_preprocessing_config = DataPreprocessingConfig(
                model_name=model_name,
                tags=tags,
                index2tag=index2tag,
                tag2index=tag2index,
                tokenizer=tokenizer
            )
            return data_preprocessing_config
        except Exception as e:
            logger.exception(e)
            raise CustomException(e, sys)

    def get_model_train_pipeline_config(self) -> ModelTrainConfig:
        try:
            model_name = self.params[BASE_MODEL_CONFIG][BASE_MODEL_NAME]
            tokenizer = AutoTokenizer.from_pretrained(self.params[BASE_MODEL_CONFIG][BASE_MODEL_NAME])

            tags = self.params[DATA_PREPROCESSING_KEY][NER_TAGS_KEY]

            index2tag = {idx: tag for idx, tag in enumerate(tags)}
            tag2index = {idx: tag for idx, tag in enumerate(tags)}

            xlmr_config = AutoConfig.from_pretrained(self.params[BASE_MODEL_CONFIG][BASE_MODEL_NAME],
                                                     num_labels=self.params[BASE_MODEL_CONFIG][NUM_CLASSES],
                                                     id2label=index2tag,
                                                     label2id=tag2index)

            epochs = self.params[BASE_MODEL_CONFIG][NUM_EPOCHS]
            batch_size = self.params[BASE_MODEL_CONFIG][BATCH_SIZE]
            save_steps = self.params[BASE_MODEL_CONFIG][SAVE_STEPS]

            output_dir = os.path.join(from_root(), ARTIFACTS_KEY, MODEL_WEIGHT_KEY)

            model_train_config = ModelTrainConfig(
                model_name=model_name,
                index2tag=index2tag,
                tag2index=tag2index,
                tokenizer=tokenizer,
                xlmr_config=xlmr_config,
                epochs=epochs,
                batch_size=batch_size,
                save_steps=save_steps,
                output_dir=output_dir
            )

            return model_train_config
        except Exception as e:
            logger.exception(e)
            raise CustomException(e, sys)

    def get_model_predict_pipeline_config(self) -> PredictPipelineConfig:
        try:
            tokenizer = AutoTokenizer.from_pretrained(self.params[BASE_MODEL_CONFIG][BASE_MODEL_NAME])
            truncation = self.params[PREDICT_MODEL_CONFIG][TRUNCATION]
            is_split_into_words = self.params[PREDICT_MODEL_CONFIG][IS_SPLIT_INTO_WORDS]
            output_dir = os.path.join(from_root(), ARTIFACTS_KEY, MODEL_WEIGHT_KEY)
            tags = self.params[DATA_PREPROCESSING_KEY][NER_TAGS_KEY]

            index2tag = {idx: tag for idx, tag in enumerate(tags)}
            tag2index = {idx: tag for idx, tag in enumerate(tags)}
            predict_pipeline_config = PredictPipelineConfig(tokenizer=tokenizer,
                                                            truncation=truncation,
                                                            is_split_into_words=is_split_into_words,
                                                            output_dir=output_dir,
                                                            index2tag=index2tag,
                                                            tag2index=tag2index)
            return predict_pipeline_config
        except Exception as e:
            logger.exception(e)
            raise CustomException(e, sys)

