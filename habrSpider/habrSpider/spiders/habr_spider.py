import scrapy
from bs4 import BeautifulSoup
from habrSpider.items import ArticleItem

class HabrSpider(scrapy.Spider):
    name = "habr_spider"
    start_urls = ['https://habr.com/ru/search/?q=flutter%20оптимизация&target_type=posts&order=relevance']

    def parse(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')

        for article in soup.select('article'):
            item = ArticleItem()
            try:
                item['title'] = article.find('h2', class_='tm-title').text.strip()
            except AttributeError:
                item['title'] = 'N/A'

            try:
                item['author'] = article.find('a', class_='tm-user-info__username').text.strip()
            except AttributeError:
                item['author'] = 'N/A'

            try:
                item['date'] = article.find('time')['datetime']
            except (AttributeError, TypeError):
                item['date'] = 'N/A'

            try:
                item['url'] = "https://habr.com" + article.find('h2', class_='tm-title').find('a')['href']
            except (AttributeError, TypeError):
                item['url'] = 'N/A'

            yield item

        try:
            next_page = soup.select_one('a.tm-pagination__navigation-link.tm-pagination__navigation-link_active')['href']
            yield response.follow(next_page, self.parse)
        except (TypeError, AttributeError):
            pass