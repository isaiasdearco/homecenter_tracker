import re

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from ..items import HomecenterTrackerItem


class HomecenterSpiderSpider(CrawlSpider):
    name = "homecenter"
    allowed_domains = ["www.homecenter.com.co"]
    start_urls = ["https://www.homecenter.com.co/homecenter-co/"]

    rules = (
        Rule(
            LinkExtractor(allow=("category"), deny=("product")),
            callback="parse_category",
        ),
    )

    def parse_category(self, response):
        try:
            products = response.css(".product-wrapper")
            current_page = response.css(".page-item.active.page-index")

            for product in products:
                item = HomecenterTrackerItem()

                item["name"] = product.css(".product-title::text").get()
                item["price"] = product.css(".price ::text").get()
                item["id"] = product.css("#title-pdp-link::attr(href)").get()

                yield item

            pagination_elements = response.css(".page-item.page-index")

            n_pages = (
                len(pagination_elements) if len(pagination_elements) // 2 > 0 else 1
            )

            if n_pages > 1:
                current_page = response.css(
                    ".page-item.page-index.selected ::text"
                ).get()

                if current_page == str(n_pages):
                    return

                if (
                    "?" in response.url.split("/")[-1]
                    and "currentpage" not in response.url
                ):
                    next_page_url = response.url + f"&currentpage={int(current_page)+1}"
                elif (
                    "?" in response.url.split("/")[-1] and "currentpage" in response.url
                ):
                    pattern = r"(currentpage=)(\d+)"
                    next_page_url = re.sub(
                        pattern, rf"\g<1>{int(current_page) + 1}", response.url
                    )
                else:
                    next_page_url = response.url + f"?currentpage={int(current_page)+1}"

                yield response.follow(next_page_url, callback=self.parse_category)

        except Exception as e:
            self.logger.error(e)
