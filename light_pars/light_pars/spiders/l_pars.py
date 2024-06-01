import scrapy
from openpyxl import Workbook


class LParsSpider(scrapy.Spider):
    name = "l_pars"
    allowed_domains = ["divan.ru"]
    start_urls = ["https://www.divan.ru/category/svet/page-1"]
    custom_settings = {
        'FEEDS': {
            'output.json': {
                'format': 'json',
                'encoding': 'utf8',
                'store_empty': False,
                'fields': None,
                'indent': 4,
            },
        }
    }

    def __init__(self):
        self.workbook = Workbook()
        self.sheet = self.workbook.active
        self.sheet.append(["Name", "Price", "URL"])

    def parse(self, response):
        lights = response.css('div.lsooF')

        for light in lights:
            name = light.css('span::text').get()
            price = light.css('div.q5Uds span::text').get()
            url = response.urljoin(light.css('a').attrib['href'])

            # Сохраняем данные в XLSX
            self.sheet.append([name, price, url])

            # Возвращаем данные для экспорта в JSON
            yield {
                "name": name,
                "price": price,
                "url": url
            }

        # Переход на следующую страницу
        response.follow('https://www.divan.ru/category/svet/page-2')
        for i in range(7):
            pages = response.css('div.ui-jDl24')

            url = pages.css('a').attrib['href']
            print(url)
            url = response.urljoin(pages.css('a').attrib['href'])
            response.follow(url)
        next_page = response.css('a.next::attr(href)').get()
        #if next_page is not None:
         #   print(next_page)
          #  yield response.follow(next_page, self.parse)

    def closed(self, reason):
        self.workbook.save("output.xlsx")

