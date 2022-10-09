import scrapy

from pep_parse.items import PepParseItem


class PepSpider(scrapy.Spider):
    name = 'pep'
    allowed_domains = ['peps.python.org']
    start_urls = ['https://peps.python.org/']

    def parse(self, response):
        tabels = response.css('section[id=index-by-category]')
        all_peps = tabels[0].css('a[href^="/pep-"]')
        for pep_link in all_peps:
            yield response.follow(pep_link, callback=self.parse_pep)

    def parse_pep(self, response):
        title_name = response.css('h1.page-title::text').get().split(' – ')
        data = {
            'number': title_name[0].replace('PEP ', ''),
            'name': title_name[1],
            'status': response.css('dt:contains("Status") + dd::text').get(),
        }
        yield PepParseItem(data)
