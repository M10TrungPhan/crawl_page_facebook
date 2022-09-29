from object.singleton import Singleton
import os
from common.common_keys import *


class Config(metaclass=Singleton):
    path_save_data = os.getenv(PATH_SAVE_DATA, "//172.29.13.24/tmtaishare/Data/facebook/")
    number_of_crawler = os.getenv(NUMBER_OF_CRAWLER, 20)
    logging_folder = "log/"