import scrapy


def get_urls_from_db():
    return ["https://www.dice.com/company/10110693a"]


class DicebotSpider(scrapy.Spider):
    name = 'dicebot'

    def start_requests(self):
        urls = get_urls_from_db()
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        key_urls = response.css(".company-right:nth-child(1) a")
        sites = []
        for site in key_urls:
            sites.append({
                "name": site.css("::text").get(default="NA").strip(),
                "url": site.css("::attr(href)").get(default="NA")
            })
        yield {
            "location": response.css(".location ::text").get(),
            "key_urls": sites
        }
