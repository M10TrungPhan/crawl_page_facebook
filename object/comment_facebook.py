import requests
import json

from object.token_and_cookies import TokenAndCookies


class CommentFacebook:

    def __init__(self, id_comment, token_and_cookies: TokenAndCookies):
        self.id_comment = id_comment
        self.token_and_cookies = token_and_cookies
        self.main_comment = None
        self.user_comment = None
        self.reply = []
        self.next_comment = ""

    def requests_first_comment(self):
        url = f"https://graph.facebook.com/v15.0/{self.id_comment}/comments?filter=stream" \
              f"&access_token={self.token_and_cookies.load_token_access()}"
        requestJar = requests.cookies.RequestsCookieJar()
        for each in self.token_and_cookies.load_cookies():
            requestJar.set(each["name"], each["value"])
        jsonformat = None
        for i in range(5):
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
            self.next_comment = jsonformat["paging"]["next"]
        except KeyError:
            self.next_comment = None

        try:
            for each in jsonformat["data"]:
                new_reply = {"user": each["from"]["name"], "text": each["message"]}
                self.reply.append(new_reply)
        except KeyError:
            pass

    def request_next_comment(self):
        while self.next_comment is not None:
            requestJar = requests.cookies.RequestsCookieJar()
            for each in self.token_and_cookies.load_cookies():
                requestJar.set(each["name"], each["value"])
            jsonformat = None
            for i in range(5):
                try:
                    response = requests.get(self.next_comment, cookies=requestJar)
                    jsonformat = json.loads(response.text)
                    if self.check_token_valid(jsonformat):
                        continue
                    break
                except:
                    continue
            if jsonformat is None:
                return

            try:
                self.next_comment = jsonformat["paging"]["next"]
            except KeyError:
                self.next_comment = None
            try:
                for each in jsonformat["data"]:
                    if len(each["message"]) < 1:
                        continue
                    new_reply = {"user": each["from"]["name"], "text": each["message"]}
                    self.reply.append(new_reply)
            except KeyError:
                pass

    def check_token_valid(self, jsonformat):
        if "error" in jsonformat.keys():
            self.token_and_cookies.update_new_token()
            return True
        return False

    @property
    def dict_comment(self):
        return {"main_comment": {"user": self.user_comment, "text": self.main_comment},
                "replies": self.reply}

    def process_comment(self):
        self.requests_first_comment()
        self.request_next_comment()
        return self.dict_comment



