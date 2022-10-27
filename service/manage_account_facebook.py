from config.config import Config
from object.singleton import Singleton
from object.account_fb_request import AccountFacebookRequest
from database.facebook_db import AccountFacebookCollection
import hashlib


class ManageAccountFacebook(metaclass=Singleton):

    def __init__(self):
        self.config = Config()
        self.account_fb_collection = AccountFacebookCollection()

    def add_account_facebook(self, account: AccountFacebookRequest):
        id_user = hashlib.md5(account.username.encode("utf-8")).hexdigest()
        if self.account_fb_collection.query_account_follow_id(id_user) is not None:
            return "ACCOUNT EXISTED"
        username = account.username
        password = account.password
        data = {"_id": id_user, "user": username, "password": password, "status": account.status}
        self.account_fb_collection.create_account(data)
        return "ACCOUNT HAVE CREATED SUCCESSFULLY"

    def remove_account_facebook(self, account: AccountFacebookRequest):
        id_user = hashlib.md5(account.username.encode("utf-8")).hexdigest()
        self.account_fb_collection.remove_account({"_id": id_user})
        return "ACCOUNT HAVE REMOVED SUCCESSFULLY"

    def select_random_account(self):
        account = self.account_fb_collection.random_account()
        if account is None:
            return None
        return account

    def update_information_account(self, account: AccountFacebookRequest):
        return self.account_fb_collection.update_information_account(account)

    def check_information_account(self, account: AccountFacebookRequest):
        id_user = hashlib.md5(account.username.encode("utf-8")).hexdigest()
        account_query = self.account_fb_collection.query_account_follow_id(id_user)
        if account_query is None:
            return "ACCOUNT IS NOT EXISTED"
        return account_query

    def get_information_all_account(self):
        return self.account_fb_collection.get_information_all_account()
