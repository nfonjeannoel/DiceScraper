import scrapy
from ..helpers.dbconnect import Dbconnect


def get_urls_from_db():
    with Dbconnect() as client:
        data = client.get_CompanyUrl()
    return data


class DicebotSpider(scrapy.Spider):
    name = 'dicebot'

    def start_requests(self):
        data = get_urls_from_db()
        for dt in data:
            url = dt.get("companyPageUrl")
            company_id = dt.get("id")
            yield scrapy.Request(url=url, callback=self.parse, meta={"id": company_id})

    def parse(self, response):
        company_id = response.meta.get('id')
        key_urls = response.css(".company-right:nth-child(1) a")
        urls_data = {}
        for site in key_urls:
            urls_data.update({
                "company_id": company_id,
                site.css("::text").get(default="NA").strip(): site.css("::attr(href)").get(default="NA")
            })
        with Dbconnect() as client:
            client.SaveToDB(urls_data)
