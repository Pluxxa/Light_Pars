import scrapy


class LParsSpider(scrapy.Spider):
    name = "l_pars"
    allowed_domains = ["https://www.divan.ru/"]
    start_urls = ["https://www.divan.ru/category/svet/page-1"]

    def parse(self, response):
        lights = []
        try:
            for i in range(100):
                url = f"https://www.divan.ru/category/svet/page-{i + 1}"
                light = response.css('div.lsooF')
                lights.append(light)
        except IndexError:
            return 0
        a = []
        for li in lights:
            for l in li:
                a.append(l)
                yield {
                    "name": l.css('div.lsooF span::text').get(),
                    "price": l.css('div.q5Uds span::text').get(),
                    "url": l.css('a').attrib['href']
                }
        print(len(a))