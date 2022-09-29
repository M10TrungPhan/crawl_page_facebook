import logging
import os
import json
import re
import requests
import time
from queue import Queue
from threading import Thread
import concurrent.futures

from bs4 import BeautifulSoup

from config.config import Config
from utils.utils import setup_selenium_firefox
from object.token_and_cookies import TokenAndCookies
from object.post_facebook import PostFacebook


class PageFacebook:

    def __init__(self, url, token_and_cookies: TokenAndCookies, path_save_data):
        self.url = url
        self.config = Config()
        self.type = None
        self.id_page = None
        self.name_page = None
        self.logger = logging.getLogger(self.__class__.__name__)
        self.get_name()
        self.token_and_cookies = token_and_cookies
        self.token_and_cookies.get_token_and_cookies()
        self.get_id()
        self.next_page = ""
        self.path_save_data = path_save_data
        self.post_queue = Queue()
        self.post_id_crawled = []
        self.flag_post = False
        self.flag_update_token = False
        self.number_post = 0

    def get_name(self):
        _, end = re.search(r"www.facebook.com/", self.url).span()
        name = self.url[end:].replace("/", "_")
        if name[-1] == "_":
            name = name[:-1]
        self.name_page = name
        return self.name_page

    def get_id(self):
        driver = setup_selenium_firefox()
        driver.get("https://www.facebook.com/")
        cookies_file = self.token_and_cookies.load_cookies()
        for cook in cookies_file:
            driver.add_cookie(cook)
        driver.get("view-source:" + self.url)
        time.sleep(2)
        soup = BeautifulSoup(driver.page_source, "lxml")
        driver.close()
        string_ss = soup.text
        regex_page_id = re.search(r"(\"pageID\"\:\"\w+\")", string_ss)
        if regex_page_id is None:
            regex_page_id = re.search(r"(\"profile_delegate_page_id\"\:\"\w+\")", string_ss)
        start, end = regex_page_id.span()
        dict_id = string_ss[start:end]
        start_id, end_id = re.search(r"(\:\"\w+\")", dict_id).span()
        id_objects = dict_id[start_id + 2: end_id - 1]
        self.id_page = id_objects
        return id_objects

    def load_post_id_have_crawled(self):
        name_folder = self.path_save_data + self.name_page + "/"
        list_id = os.listdir(name_folder)
        list_id = [each.replace(".json", "") for each in list_id]
        self.post_id_crawled = list_id
        return self.post_id_crawled

    def request_first_page(self):
        if self.type == "Page":
            url = f"https://graph.facebook.com/v15.0/{self.id_page}/posts?" \
                  f"&access_token={self.token_and_cookies.load_token_access()}&limit=100"
        else:
            url = f"https://graph.facebook.com/v15.0/{self.id_page}/feed?" \
                  f"&access_token={self.token_and_cookies.load_token_access()}&limit=100"
        requestJar = requests.cookies.RequestsCookieJar()
        for each in self.token_and_cookies.load_cookies():
            requestJar.set(each["name"], each["value"])
        jsonformat = None
        for i in range(1000):
            try:
                response = requests.get(url, cookies=requestJar)
                jsonformat = json.loads(response.text)
                if self.check_token_valid(jsonformat):
                    continue
                break
            except:
                continue
        if jsonformat is None:
            return
        try:
            self.next_page = jsonformat["paging"]["next"]
        except KeyError:
            self.next_page = None
        try:
            for each in jsonformat["data"]:
                if each["id"] in self.post_id_crawled:
                    continue
                postfb = PostFacebook(each["id"], self.token_and_cookies, self.path_save_data + self.name_page + "/")
                postfb.content = each["message"]
                self.post_queue.put(postfb)
        except KeyError:
            pass
        return jsonformat

    def request_next_page(self):
        while self.next_page is not None:
            requestJar = requests.cookies.RequestsCookieJar()
            for each in self.token_and_cookies.load_cookies():
                requestJar.set(each["name"], each["value"])
            jsonformat = None
            for i in range(5):
                try:
                    response = requests.get(self.next_page, cookies=requestJar)
                    jsonformat = json.loads(response.text)
                    if self.check_token_valid(jsonformat):
                        continue
                    break
                except:
                    continue
            if jsonformat is None:
                continue
            try:
                self.next_page = jsonformat["paging"]["next"]
            except KeyError:
                self.next_page = None
            try:
                for each in jsonformat["data"]:
                    if each["id"] in self.post_id_crawled:
                        continue
                    postfb = PostFacebook(each["id"], self.token_and_cookies, self.path_save_data + self.name_page + "/")
                    postfb.content = each["message"]
                    self.post_queue.put(postfb)
            except KeyError:
                pass
        self.logger.info(f"NUMBER OF POST IN {self.name_page}: {self.post_queue.qsize()}")

    def check_token_valid(self, jsonformat):
        if "error" in jsonformat.keys():
            self.token_and_cookies.update_new_token()
            return True
        return False

    def create_folder_save_data(self):
        os.makedirs(self.path_save_data + self.name_page + "/", exist_ok=True)

    def crawl_post(self):
        if not self.post_queue.qsize():
            return
        post_process = self.post_queue.get()
        post_process.process_post()
        if post_process:
            self.number_post += 1

    def thread_check_status(self):
        while (self.post_queue.qsize() > 0) or (self.next_page is not None):
            self.logger.info(f"NUMBER POST HAVE CRAWLED: {self.number_post}")
            time.sleep(60*30)

    def process_page(self):
        self.create_folder_save_data()
        self.load_post_id_have_crawled()
        self.request_first_page()
        self.logger.info(f"CRAWL PAGE: {self.name_page}. ID PAGE: {self.id_page}")
        thread_request_next_page = Thread(target=self.request_next_page)
        thread_request_next_page.start()
        thread_status = Thread(target=self.thread_check_status)
        thread_status.start()
        time.sleep(10)
        while (self.post_queue.qsize() > 0) or (self.next_page is not None):
            with concurrent.futures.ThreadPoolExecutor(max_workers=self.config.number_of_crawler) as executor:
                [executor.submit(self.crawl_post) for _ in range(self.config.number_of_crawler)]
        thread_request_next_page.join()
        self.logger.info(f"FINISHED CRAWL PAGE {self.name_page}. NUMBER POST HAVE CRAWLED: {self.number_post}")

