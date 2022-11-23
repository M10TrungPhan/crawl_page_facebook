import time
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import re
import pymongo
import random
from selenium.webdriver.common.keys import Keys


class AutoCommentService:
    def __init__(self):
        pass

    @staticmethod
    def setup_selenium_firefox():
        ser = Service("D:/trungphan/crawl_page_facebook/driverbrower/geckodriver.exe")
        firefox_options = FirefoxOptions()
        firefox_options.set_preference("media.volume_scale", "0.0")
        firefox_options.set_preference('devtools.jsonview.enabled', False)
        firefox_options.set_preference('dom.webnotifications.enabled', False)
        firefox_options.add_argument("--test-type")
        firefox_options.add_argument('--ignore-certificate-errors')
        firefox_options.add_argument('--disable-extensions')
        firefox_options.add_argument('disable-infobars')
        firefox_options.add_argument("--incognito")
        # firefox_options.add_argument("--headless")
        driver = webdriver.Firefox(service=ser, options=firefox_options)
        return driver

    @staticmethod
    def get_random_account_active():
        client = pymongo.MongoClient(host="172.29.13.23", port=20253, username="admin", password="admin")
        database = client["facebook"]
        facebook_col = database["account_fb"]
        myquery = {"status": "active"}
        list_account = []
        for x in facebook_col.find(myquery):
            list_account.append(x)
        return list_account[random.randint(0, len(list_account) - 1)]

    def access_url_comment(self, url_comment):
        account = self.get_random_account_active()
        driver = self.setup_selenium_firefox()
        res = ""
        for _ in range(5):
            try:
                res = ""
                driver.get("https://www.facebook.com/")
                cookies = account["cookies"]
                for cook in cookies:
                    driver.add_cookie(cook)
                driver.get(url_comment)
                break
            except:
                res = None
                continue
        if res is None:
            driver.close()
            return None
        time.sleep(3)
        return driver

    @staticmethod
    def show_more_text(driver):
        list_button_more = driver.find_elements(By.CLASS_NAME,
                                                value="x1i10hfl xjbqb8w x6umtig x1b1mbwd xaqea5y xav7gou x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz xt0b8zv xzsf02u x1s688f".replace(
                                                    " ", "."))
        while len(list_button_more):
            for each in list_button_more:
                try:
                    if each.get_attribute("role") == "button":
                        if re.search(r"Xem thêm|See more", each.text) is None:
                            continue
                        each.click()
                except:
                    pass
            number_button_more_old = len(list_button_more)
            list_button_more = driver.find_elements(By.CLASS_NAME,
                                                    value="x1i10hfl xjbqb8w x6umtig x1b1mbwd xaqea5y xav7gou x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz xt0b8zv xzsf02u x1s688f".replace(
                                                        " ", "."))
            if number_button_more_old == len(list_button_more):
                break

    @staticmethod
    def detect_box_comment_to_reply(driver, content_comment):
        list_comment = driver.find_elements(By.CLASS_NAME,
                                            value="x1r8uery x1iyjqo2 x6ikm8r x10wlt62 x1pi30zi".replace(" ", "."))
        for each in list_comment:
            if content_comment in each.text:
                box_comment_select = each
                break
            if content_comment.replace("  ", " ") in each.text:
                box_comment_select = each
                break
        return box_comment_select

    @staticmethod
    def click_reply_button(comment_select):
        list_button = comment_select.find_elements(By.CLASS_NAME,
                                                   value="x1i10hfl xjbqb8w x6umtig x1b1mbwd xaqea5y xav7gou x9f619 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz xi81zsa x1ypdohk x1rg5ohu x117nqv4 x1n2onr6 xt0b8zv".replace(
                                                       " ", "."))
        for each in list_button:
            if re.search(r"Phản hồi|Reply", each.text, flags=re.IGNORECASE) is not None:
                button_select = each
        button_select.click()

    @staticmethod
    def detect_box_reply(driver, user_comment):
        list_box_reply = driver.find_elements(By.CLASS_NAME,
                                              value="xzsf02u x1a2a7pz x1n2onr6 x14wi4xw notranslate".replace(" ", "."))
        for each in list_box_reply:
            if user_comment in each.text:
                reply_box_select = each
        return reply_box_select

    @staticmethod
    def send_reply_comment(box_reply, content_reply):
        for each in content_reply:
            box_reply.send_keys(each)
        box_reply.send_keys(Keys.ENTER)
        box_reply.send_keys(Keys.ENTER)

    def auto_post_comment(self, user_comment, url_comment, content_comment, content_reply):
        content_reply = " " + content_reply
        driver = self.access_url_comment(url_comment)
        try:
            self.show_more_text(driver)
            box_comment_select = self.detect_box_comment_to_reply(driver, content_comment)
            self.click_reply_button(box_comment_select)
            box_send_reply = self.detect_box_reply(driver, user_comment)
            self.send_reply_comment(box_send_reply, content_reply)
            time.sleep(5)
            driver.close()
        except:
            driver.close()


auto_post_comment_tool = AutoCommentService()
user_comment = "Tuấn Vũ"
url_comment = "https://www.facebook.com/groups/phanbien/posts/4140874695980372/?comment_id=4140883375979504&__cft__[0]=AZWitJBcSSLpAXzc3M36A3qQYWMlNELgpwp2skYPuC-8LNK3IoVJv1nquXSz3CeiMD3w8s4LeuNsGqvtxc-2kgBzXIOKkoLf1tcpCS8g2ovdh8r7I2hAqoUqUfZUPyieT0Djvoslmoc41dDg4fyyI4RY&__tn__=R]-R"
content_comment = "ủng hộ nha, ông nào phản đối thì thay mấy con vật kia làm thí nghiệm đi."
content_reply = " gọi là các *bé đi, nói vậy chứ được miếng bò nầm các bé vẫn ăn ngon ơ à"
auto_post_comment_tool.auto_post_comment(user_comment, url_comment, content_comment, content_reply)