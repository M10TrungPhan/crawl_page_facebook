import time

from service.crawl_facebook import CrawlFacebook
import uvicorn
from common.common_keys import *
from service.manage_account_facebook import ManageAccountFacebook
from object.post_group_facebook import PostGroupFacebook
from object.token_and_cookies import TokenAndCookies
from service.manage_account_facebook import ManageAccountFacebook
from service.manage_account_facebook import ManageAccountFacebook


if __name__ == "__main__":
    # list_url = ["https://www.facebook.com/groups/khoahocxgr/"]
    # # # list_url = ["https://www.facebook.com/groups/maybefnews/"]
    manage_account = ManageAccountFacebook()
    manage_account.start()
    # for url_page in list_url:
    #     crawl_fb = CrawlFacebook(url_page)
    #     crawl_fb.start()
    #     time.sleep(5)
    #
    # uvicorn.run("apis.api:app", host=HOST_API, port=8002, reload=False, log_level="debug", debug=False,
    #             workers=1, factory=False, loop="asyncio", timeout_keep_alive=120)




