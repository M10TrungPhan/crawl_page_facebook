import json
import re
import time
import requests
import logging
from threading import Thread

from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By

from object.token_and_cookies import TokenAndCookies
from database.facebook_db import FacebookCollection
from utils.utils import setup_selenium_firefox


class PostGroupFacebook:

    def __init__(self, url_page, id_post, token_and_cookies: TokenAndCookies, path_save_data, name_page):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.url_page = url_page
        self.name_page = name_page
        self.path_save_data = path_save_data
        self.id_post = id_post
        self.token_and_cookies = token_and_cookies
        self.driver = None
        self.fb_data = FacebookCollection()
        self.content = None
        self.image = None
        self.link_image = []
        self.comment = []
        self.flag_driver = False
        self.flag_time_out = False
        self.number_comment = None

    @staticmethod
    def preprocess_id_post(id_post):
        result_regex = re.search(r"\d_", id_post)
        if result_regex is not None:
            _, end = result_regex.span()
            id_post = id_post[end:]
        # print(id_post)
        return id_post

    def get_data_image_for_post(self):
        url = f"https://graph.facebook.com/v15.0/{self.id_post}/attachments?" \
              f"access_token={self.token_and_cookies.load_token_access()}"
        requestJar = requests.cookies.RequestsCookieJar()
        for each in self.token_and_cookies.load_cookies():
            requestJar.set(each["name"], each["value"])
        response = requests.get(url, cookies=requestJar)
        jsonformat = json.loads(response.text)
        return jsonformat

    def get_image_for_post(self):
        data_image = self.get_data_image_for_post()
        try:
            list_image = data_image["data"][0]["subattachments"]["data"][0]
            for each in list_image:
                self.link_image.append(each["media"]["image"]["src"])
            return self.link_image
        except:
            pass
        try:
            self.link_image.append(data_image["data"][0]["media"]["image"]["src"])
        except :
            pass
        return self.link_image

    def access_website(self):
        self.driver = setup_selenium_firefox()
        res = ""
        for _ in range(5):
            try:
                res = ""
                self.driver.get("https://www.facebook.com/")
                cookies = self.token_and_cookies.load_cookies()
                for each in cookies:
                    self.driver.add_cookie(each)
                self.driver.get(self.url_page + self.preprocess_id_post(self.id_post))
                break
            except Exception as e:
                print(f"Error in requests {e}")
                res = None
                continue
        if res is None:
            self.driver.close()
            return None
        time.sleep(3)
        return self.parse_html()

    def parse_html(self):
        return BeautifulSoup(self.driver.page_source, "lxml")

    def select_mode_view_all_comment(self):
        try:
            box_menu = self.driver.find_element(By.CLASS_NAME, value="x6s0dn4 x78zum5 xdj266r x11i5rnm xat24cr x1mh8g0r xe0p6wg".replace(" ", "."))
        except:
            return
        button_menu = box_menu.find_elements(By.CLASS_NAME, value="x1i10hfl xjbqb8w x6umtig x1b1mbwd xaqea5y xav7gou x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1o1ewxj x3x9cwd x1e5q0jg x13rtm0m x1n2onr6 x87ps6o x1lku1pv x1a2a7pz".replace(" ", "."))
        for each in button_menu:
            if each.get_attribute("role") == "button":
                each.click()
                break
        menu_item = self.driver.find_elements(By.CLASS_NAME, value="x1i10hfl xjbqb8w x6umtig x1b1mbwd xaqea5y xav7gou xe8uvvx x1hl2dhg xggy1nq x1o1ewxj x3x9cwd x1e5q0jg x13rtm0m x87ps6o x1lku1pv x1a2a7pz xjyslct x9f619 x1ypdohk x78zum5 x1q0g3np x2lah0s x1w4qvff x13mpval xdj266r xat24cr xz9dl7a x1sxyh0 xsag5q8 xurb0ha x1n2onr6 x16tdsg8 x1ja2u2z x6s0dn4".replace(" ","."))
        for each in menu_item:
            if re.search(r"Tất cả|All", each.text) is not None:
                each.click()
                time.sleep(3)

    def show_all_comments(self):
        list_button_more = self.driver.find_elements(By.CLASS_NAME,
                                                     value="x78zum5 x1w0mnb xeuugli".replace(" ", "."))
        while len(list_button_more) > 0:
            if re.search(r"Xem|View|Views|^\d+ phản hồi|^\d (Replies|Reply)", list_button_more[-1].text,
                         flags=re.IGNORECASE) is None:
                if re.search(r"Xem|View|Views|^\d+ phản hồi|^\d (Replies|Reply)", list_button_more[0].text,
                             flags=re.IGNORECASE) is None:
                    print("XXXXXXXX")
                    break
            for each in list_button_more:
                try:
                    if re.search(r"Ẩn|Hide", each.text) is not None:
                        continue
                    each.click()
                except:
                    continue
            time.sleep(5)
            for _ in range(5):
                try:
                    list_button_more = self.driver.find_elements(By.CLASS_NAME,
                                                         value="x78zum5 x1w0mnb xeuugli".replace(
                                                             " ", "."))
                    self.scroll(1000)
                except:
                    time.sleep(1)
                    continue
        print("DONE LOAD ALL COMMENT")

    def scroll(self, pixel):
        javascript = f"window.scrollBy(0,{pixel});"
        self.driver.execute_script(javascript)

    def show_more_text(self):
        list_button_more = self.driver.find_elements(By.CLASS_NAME,
                                                     value="x1i10hfl xjbqb8w x6umtig x1b1mbwd xaqea5y xav7gou x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz xt0b8zv xzsf02u x1s688f".replace(
                                                         " ", "."))
        while len(list_button_more):
            for each in list_button_more:
                try:
                    if each.get_attribute("role") == "button":
                        if re.search(r"Xem thêm|See more", each.text) is None:
                            continue
                        each.click()
                        self.scroll(1000)
                except:
                    pass
            number_button_more_old = len(list_button_more)
            list_button_more = self.driver.find_elements(By.CLASS_NAME,
                                                         value="x1i10hfl xjbqb8w x6umtig x1b1mbwd xaqea5y xav7gou x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz xt0b8zv xzsf02u x1s688f".replace(
                                                             " ", "."))
            if number_button_more_old == len(list_button_more):
                break
            time.sleep(2)

    def get_content(self):

        soup = self.parse_html()
        content = ""
        content_tag = soup.find("div", class_="x1swvt13 x1l90r2v x1pi30zi x1iorvi4")
        if content_tag is not None:
            print("CONTENT TYPE 1")
            paragraph_content_tag = content_tag.find_all("div", attrs={"style": "text-align: start;"})
            print(f"NUMBER PARAGRAHPH {len(paragraph_content_tag)}")
            if len(paragraph_content_tag):
                for each in paragraph_content_tag:
                    content += each.get_text(strip=False).strip() + "\n"
            content = content_tag.get_text(strip=False, separator="\n")
            return content.strip()
        content_tag_new = soup.find_all("div", class_="x1iorvi4 x1pi30zi x1l90r2v x1swvt13")
        if len(content_tag_new):
            print("CONTENT TYPE 2")
            for each in content_tag_new:
                content += each.get_text(strip=False).strip() + "\n"
            return content.strip()

        content_tag_new = soup.find_all("span",
                                    class_="x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xudqn12 x3x7a5m x1f6kntn xvq8zen xo1l8bm xzsf02u x1yc453h")

        if len(content_tag_new):
            print("CONTENT TYPE 3")
            for each in content_tag_new:
                content += each.get_text(separator="\n", strip=True) + "\n"
            return content.strip()
        content_tag_new = soup.find("span", class_="x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xudqn12 x3x7a5m x6prxxf xvq8zen xo1l8bm xzsf02u x1yc453h")
        if content_tag_new is not None:
            print("CONTENT TYPE 4")
            content = content_tag_new.get_text(separator="\n", strip=True)
            return content
        return content

    def get_number_comment(self):
        soup = self.parse_html()
        box_number_comment = soup.find("div", class_="x6s0dn4 x78zum5 x2lah0s x17rw0jw")
        if box_number_comment is None:
            return None
        box_text = box_number_comment.find("span",
                                      class_="x4k7w5x x1h91t0o x1h9r5lt x1jfb8zj xv2umb2 x1beo9mf xaigb6o x12ejxvf x3igimt xarpa2k xedcshv x1lytzrv x1t2pt76 x7ja8zs x1qrby5j")
        if box_text is None:
            return None
        text_number_comment = box_text.text
        result_regex = re.search(r"\d+", text_number_comment)
        if result_regex is None:
            return None
        start, end = result_regex.span()
        return int(text_number_comment[start:end].strip())

    def get_data_for_box_comment(self, box_comment):
        user_main_comment = box_comment.find("span", class_="xt0psk2")
        text_main_comment_box = box_comment.find("div", class_="xdj266r x11i5rnm xat24cr x1mh8g0r x1vvkbs")
        text_comment = self.get_text_for_box_comment(text_main_comment_box)
        tags = self.get_tags_for_box_comment(text_main_comment_box)
        attachment = self.get_attachment_for_box_comment(box_comment)
        data = {"user": user_main_comment.text, "attachment": attachment, "text": text_comment, "tags": tags}
        return data

    @staticmethod
    def get_attachment_for_box_comment(box_comment):
        box_attachment = box_comment.findChild("div", class_="x78zum5 xv55zj0 x1vvkbs", recursive=False)
        data_image = None
        data_link = None
        if box_attachment is None:
            return {"image": data_image, "link": data_link}
        box_image_attachment = box_attachment.find("a",
                                                   class_="x1i10hfl xjbqb8w x6umtig x1b1mbwd xaqea5y xav7gou x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz")
        box_link_attachment = box_attachment.find("a",
                                                  class_="x1i10hfl xjbqb8w x6umtig x1b1mbwd xaqea5y xav7gou x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz x1ey2m1c xds687c x10l6tqk x17qophe x13vifvy xi2jdih")
        if box_image_attachment is not None:
            image_element = box_image_attachment.find("img")
            if image_element is not None:
                image_source = image_element["src"]
                image_description = image_element["alt"]
                data_image = {"source": image_source, "description": image_description}

        if box_link_attachment is not None:
            link_element = box_link_attachment.find("span")
            if link_element is not None:
                link = box_link_attachment["href"]
                link_description = link_element.text
                data_link = {"source": link, "description": link_description}
        return {"image": data_image, "link": data_link}

    @staticmethod
    def get_text_for_box_comment(box_text_comment):
        text_comment = ""
        if box_text_comment is None:
            return None
        list_paragraph_element = box_text_comment.findAll("div", attrs={"style": "text-align: start;"})
        for each in list_paragraph_element:
            text_comment += each.get_text(strip=False).strip() + "\n"
        return text_comment.strip()

    @staticmethod
    def get_tags_for_box_comment(box_text_comment):
        tags = []
        if box_text_comment is None:
            return tags
        tags_element = box_text_comment.findAll("a",
                                                class_="x1i10hfl xjbqb8w x6umtig x1b1mbwd xaqea5y xav7gou x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz xt0b8zv xzsf02u x1s688f")
        for tag in tags_element:
            tags.append(tag.text)
        return tags

    def get_data_for_each_comment(self, box_each_comment):
        main_comment = self.get_main_comment(box_each_comment)
        list_reply = self.get_main_reply(box_each_comment)
        main_comment["replies"] = list_reply
        return main_comment

    def get_main_comment(self, box_comment):
        comment_tag = box_comment.find("div", class_="x1n2onr6")
        comment_tag = comment_tag.find("div", class_="x1r8uery x1iyjqo2 x6ikm8r x10wlt62 x1pi30zi")
        main_comment = self.get_data_for_box_comment(comment_tag)
        return main_comment

    def get_main_reply(self, box_main_reply):
        list_reply = []
        reply_tag = box_main_reply.find("div", class_="xdj266r xexx8yu x4uap5 x18d9i69 xkhd6sd")
        reply_tag = reply_tag.find("ul")
        if reply_tag is None:
            return list_reply
        list_main_reply_tag = reply_tag.findAll("li")
        for each_main_reply in list_main_reply_tag:
            box_main_reply = each_main_reply.find("div", class_="x1n2onr6 x46jau6")
            if box_main_reply is None:
                continue
            tag_main_reply = box_main_reply.find("div", class_="x1r8uery x1iyjqo2 x6ikm8r x10wlt62 x1pi30zi")
            main_reply = self.get_data_for_box_comment(tag_main_reply)
            box_mini_reply = box_main_reply.find_next_sibling("div")
            if box_mini_reply is None:
                # data_each_main_reply = {"main_reply": main_reply, "mini_replies": []}
                main_reply["replies"] = []
                list_reply.append(main_reply)
                continue
            mini_reply = self.get_mini_reply(box_mini_reply)
            # data_each_main_reply = {"main_reply": main_reply, "mini_replies": mini_reply}
            main_reply["replies"] = mini_reply
            list_reply.append(main_reply)
        return list_reply

    def get_mini_reply(self, box_mini_reply):
        list_mini_reply = []
        reply_tag = box_mini_reply.find("ul")
        if reply_tag is None:
            return list_mini_reply
        list_mini_reply_tag = reply_tag.findAll("li")
        for each in list_mini_reply_tag:
            tag_mini_reply = each.find("div",
                                       class_="x1n2onr6 x1iorvi4 x4uap5 x18d9i69 xurb0ha x78zum5 x1q0g3np x1a2a7pz")
            if tag_mini_reply is None:
                continue
            tag_mini_reply = tag_mini_reply.find("div", class_="x1r8uery x1iyjqo2 x6ikm8r x10wlt62 x1pi30zi")
            if tag_mini_reply is None:
                continue
            mini_reply = self.get_data_for_box_comment(tag_mini_reply)
            list_mini_reply.append(mini_reply)
        return list_mini_reply

    def get_all_comment_in_post(self):
        soup = self.parse_html()
        box_comment = soup.find("div", class_="x1jx94hy x12nagc")
        box_comment = box_comment.findChild("ul", recursive=False)
        if box_comment is None:
            return []
        list_comment = box_comment.findChildren("li", recursive=False)
        list_total_comment = []
        for each_comment in list_comment:
            data_each_comment = self.get_data_for_each_comment(each_comment)
            list_total_comment.append(data_each_comment)
        return list_total_comment

    def time_out_for_driver(self):
        for _ in range(600):
            if self.flag_time_out:
                print("END TIMER 1")
                return
            time.sleep(1)
        self.flag_driver = True
        print("END TIMER 2")

    def close_driver(self):
        thread_time_out = Thread(target=self.time_out_for_driver)
        thread_time_out.start()
        while True:
            if self.flag_driver:
                self.driver.close()
                print(f"CLOSE SELENIUM FOR {self.url_page + self.preprocess_id_post(self.id_post)}")
                break

    @property
    def dict_post(self):
        return {"_id": self.id_post,
                "url_post": self.url_page + self.preprocess_id_post(self.id_post),
                "name_page": self.name_page,
                "image": self.link_image,
                "content": self.content,
                "number_comment": self.number_comment,
                "comment": self.comment}

    def process_post(self):
        self.get_image_for_post()
        if self.access_website() is None:
            return
        thread_check_not_working = Thread(target=self.close_driver)
        thread_check_not_working.start()
        self.scroll(1000)
        print(self.url_page + self.preprocess_id_post(self.id_post))
        self.content = self.get_content()
        self.number_comment = self.get_number_comment()
        print(self.content)
        print(self.number_comment)
        try:
            self.select_mode_view_all_comment()
            print(2)
            self.show_all_comments()
            print(3)
            self.show_more_text()
            self.comment = self.get_all_comment_in_post()
            json.dump(self.dict_post, open(self.path_save_data + self.id_post+".json", "w", encoding="utf-8"),
                      ensure_ascii=False, indent=4)
            self.flag_driver = True
            self.flag_time_out = True
        except Exception as e:
            print(e)
        time.sleep(2)


