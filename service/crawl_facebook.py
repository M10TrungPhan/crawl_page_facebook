import os
import logging
from threading import Thread

from object.page_facebook import PageFacebook
from object.token_and_cookies import TokenAndCookies
from config.config import Config


class CrawlFacebook(Thread):

    def __init__(self, url_page):
        super(CrawlFacebook, self).__init__()
        self.config = Config()
        self.logger = logging.getLogger(self.__class__.__name__)
        self.token_and_cookies = TokenAndCookies()
        self.url_page = url_page
        self.path_save_data = self.config.path_save_data

    def create_folder_save_data(self):
        os.makedirs(self.path_save_data + "/", exist_ok=True)

    def run(self):
        self.logger.info(f"START CRAWL {self.url_page}")
        page = PageFacebook(self.url_page, self.token_and_cookies, self.path_save_data)
        page.process_page()
        self.logger.info(f"FINISHED CRAWL {self.url_page}")
