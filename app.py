from service.crawl_facebook import CrawlFacebook
import uvicorn
from common.common_keys import *
from database.facebook_db import AccountFacebookCollection

if __name__ == "__main__":
    #
    list_url = ["https://www.facebook.com/ShopITBooks/",
                "https://www.facebook.com/dabaoconceptheritage",
                "https://www.facebook.com/1phutSaiGon/",
                "https://www.facebook.com/cheanhsnsd",
                "https://www.facebook.com/yantv/",
                "https://www.facebook.com/20thCenturyStudiosVN/",
                "https://www.facebook.com/tuyetcollection/",
                "https://www.facebook.com/ItrekTravel/",
                "https://www.facebook.com/fan24h/",
                "https://www.facebook.com/VTVcab.Tintuc/",
                "https://www.facebook.com/khongsocho.official/",
                "https://www.facebook.com/khoetunhien1/",
                "https://www.facebook.com/MOHVIETNAM",
                "https://www.facebook.com/khoevadep.eva/",
                "https://www.facebook.com/FoodyVietnam/",
                "https://www.facebook.com/RunningManVietNamFC",
                "https://www.facebook.com/SGTT247/",
                "https://www.facebook.com/cuoingacuoinghieng/",
                "https://www.facebook.com/news.7vietcom/",
                "https://www.facebook.com/profile.php?id=1000848684557",
                "https://www.facebook.com/N%C3%A3o-ri-n%C3%A3o-com%C3%A9dia--111383100220197/"]
    #
    for url_page in list_url:
        crawl_fb = CrawlFacebook(url_page)
        crawl_fb.start()
        crawl_fb.join()

    # uvicorn.run("apis.api:app", host=HOST_API, port=8003, reload=False, log_level="debug",
    #             debug=False, workers=1, factory=False, loop="asyncio", timeout_keep_alive=120)


