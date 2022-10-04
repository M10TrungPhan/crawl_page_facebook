import random
import hashlib

from object.account_fb_request import AccountFacebookRequest
from database.mongo_client import MongoDatabase
from config.config import Config


class FacebookCollection:
    def __init__(self):
        self.config = Config()
        self.mongodb = MongoDatabase()
        self.database = self.mongodb.client[self.config.fb_database]
        self.data_col = self.database[self.config.data_fb_collection]

    def save_data(self, data):
        self.data_col.insert_one(data)

    def get_list_id_for_page(self, name_page):
        name_page_query = {"name_page": name_page}
        list_id_post = []
        for each in self.data_col.find(name_page_query):
            list_id_post.append(each["_id"])
        return list_id_post


class AccountFacebookCollection:
    def __init__(self):
        self.config = Config()
        self.mongodb = MongoDatabase()
        self.database = self.mongodb.client[self.config.fb_database]
        self.data_col = self.database[self.config.account_fb_collection]

    def create_account(self, data):
        self.data_col.insert_one(data)

    def remove_account(self, data):
        self.data_col.delete_one(data)

    def random_account(self):
        list_account = []
        for x in self.data_col.find():
            list_account.append(x)
        if not len(list_account):
            return None

        return list_account[random.randint(0, len(list_account)-1)]

    def query_account_follow_id(self, account_id):
        account = None
        query_condition = {"_id": account_id}
        for x in self.data_col.find(query_condition):
            account = x
        if account is None:
            return
        return account

    def update_information_account(self, account: AccountFacebookRequest):
        id_user = hashlib.md5(account.username.encode("utf-8")).hexdigest()
        account_in_db = self.query_account_follow_id(id_user)
        if account_in_db is None:
            return f"User not existed"
        old_password = account_in_db["password"]
        old_status = account_in_db["status"]
        if account.password is None:
            update_password = old_password
        else:
            update_password = account.password
        if account.status is None:
            update_status = old_status
        else:
            update_status = account.status
        query_condition = {"_id": id_user}
        new_values = {"$set": {"password": update_password, "status": update_status}}
        self.data_col.update_one(query_condition, new_values)
        return f"UPDATE SUCCESSFUL FOR USER {account.username}"

    def get_information_all_account(self):
        list_account = []
        for x in self.data_col.find():
            list_account.append(x)
        return list_account
