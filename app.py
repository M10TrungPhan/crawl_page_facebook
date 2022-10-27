from service.crawl_facebook import CrawlFacebook
import uvicorn
from common.common_keys import *
from object.post_group_facebook import PostGroupFacebook
from object.token_and_cookies import TokenAndCookies

if __name__ == "__main__":
    # #
    list_url = ["https://www.facebook.com/groups/khoahocxgr/"]
    for url_page in list_url:
        crawl_fb = CrawlFacebook(url_page)
        crawl_fb.start()
        crawl_fb.join()

    # token = TokenAndCookies()
    # token.get_token_and_cookies()
    # post = PostGroupFacebook("https://www.facebook.com/groups/khoahocxgr/", "441249175921600_5132557856790685", token, "//172.29.13.24/tmtaishare/Data/Data_GROUP_FACEBOOK/", "Cộng Đồng Chia Sẻ - Nâng Tầm Kiến Thức _XGR_")
    # post.process_post()


    #
    # uvicorn.run("apis.api:app", host=HOST_API, port=8003, reload=False, log_level="debug",
    #             debug=False, workers=1, factory=False, loop="asyncio", timeout_keep_alive=120)


