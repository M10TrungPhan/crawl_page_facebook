from service.crawl_facebook import CrawlFacebook


if __name__ == "__main__":
    user = "hieudan3123@outlook.com.vn"
    password = "A@123B@123"
    dir_data = "//172.29.13.24/tmtaishare/Data/facebook/"
    list_url = ["https://www.facebook.com/divodivavietnam", "https://www.facebook.com/neuconfessions/",
                "https://www.facebook.com/Biettheeodilam"]

    for url_page in list_url:
        crawl_fb = CrawlFacebook(user, password, url_page)
        crawl_fb.start()
        crawl_fb.join()
