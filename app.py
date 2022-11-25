from service.crawl_facebook import CrawlFacebook
import uvicorn
from common.common_keys import *
from object.post_group_facebook import PostGroupFacebook
from object.token_and_cookies import TokenAndCookies
from service.manage_account_facebook import ManageAccountFacebook

if __name__ == "__main__":
    # #
    # list_url = ["https://www.facebook.com/groups/khoahocxgr/"]
    list_url = ["https://www.facebook.com/groups/phanbien/"]
    # # list_url = ["https://www.facebook.com/groups/maybefnews/"]
    for url_page in list_url:
        crawl_fb = CrawlFacebook(url_page)
        crawl_fb.start()
        crawl_fb.join()

    # token = TokenAndCookies()
    # token.get_token_and_cookies()
    # mn = ManageAccountFacebook()
    # post = PostGroupFacebook("https://www.facebook.com/groups/phanbien/", "441249175921600_2949046651808494",  "//172.29.13.24/tmtaishare/Data/Data_GROUP_FACEBOOK/", "Cộng Đồng Chia Sẻ - Nâng Tầm Kiến Thức _XGR_")
    # post.account = mn.get_random_account_active()
    # try:
    #     post.process_post()
    # except:
    #     pass

    # #
    # uvicorn.run("apis.api:app", host=HOST_API, port=8003, reload=False, log_level="debug",
    #             debug=False, workers=1, factory=False, loop="asyncio", timeout_keep_alive=120)



