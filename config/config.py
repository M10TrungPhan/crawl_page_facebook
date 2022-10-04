from object.singleton import Singleton
import os
from common.common_keys import *


class Config(metaclass=Singleton):
    path_save_data = os.getenv(PATH_SAVE_DATA, "//172.29.13.24/tmtaishare/Data/facebook/")
    number_of_crawler = os.getenv(NUMBER_OF_CRAWLER, 20)
    logging_folder = "log/"
    mongodb_host = os.getenv(MONGODB_HOST, '172.28.0.23')
    mongodb_port = int(os.getenv(MONGODB_PORT, '20253'))
    mongodb_username = os.getenv(MONGODB_USERNAME, 'admin')
    mongodb_password = os.getenv(MONGODB_PASSWORD, 'admin')
    fb_database = os.getenv(FB_DATABASE, "facebook")
    data_fb_collection = os.getenv(DATA_FB_COLLECTION, "fb_data")
    account_fb_collection = os.getenv(ACCOUNT_FB_COLLECTION, "account_fb")

