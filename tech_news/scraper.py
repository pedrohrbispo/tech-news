from parsel import Selector
from tech_news.database import create_news
import requests
import time


# Requisito 1
def fetch(url):
    """Faz o fetch da página e pega seu html"""
    try:
        response = requests.get(url, timeout=3)
        time.sleep(1)
        if response.status_code != 200:
            return None
        return response.text
    except requests.ReadTimeout or response.status_code != 200:
        # Retorna None
        return None


def shares_count(selector):
    count = 0
    share_selector = selector.css('.tec--toolbar__item::text').get()
    if share_selector is not None:
        count = share_selector.split()[0]
    return int(count)


def comments_count(selector):
    count = 0
    css_selector = '#js-comments-btn ::attr(data-count)'
    comments_selector = selector.css(css_selector).get()
    if comments_selector is not None:
        count = comments_selector.split()[0]
    return int(count)


def get_sources(selector):
    sources = selector.css('.z--mb-16 .tec--badge *::text').getall()
    sources_list = []
    if sources is not None:
        for source in sources:
            if isinstance(source, str):
                sources_list.append(source.strip())
    return sources_list


def get_categories(selector):
    categories = selector.css('#js-categories .tec--badge *::text').getall()
    categories_list = []
    if categories is not None:
        for categorie in categories:
            if isinstance(categorie, str):
                categories_list.append(categorie.strip())
    return categories_list


def get_writer(selector):
    try_get_writer = selector.css('.z--font-bold *::text').get()

    if try_get_writer is not None:
        return try_get_writer.strip()
    else:
        return None


# Requisito 2
#   #https://pt.stackoverflow.com/questions/178439/transformar-um-array-para-string-no-python
def scrape_noticia(html_content):
    """Seu código deve vir aqui"""
    selector = Selector(html_content)
    return {
        "url": selector.css('link[rel=canonical] ::attr(href)').get(),
        "title": selector.css('#js-article-title::text').get(),
        "timestamp": selector.css('#js-article-date ::attr(datetime)').get(),
        "writer": get_writer(selector),
        "shares_count": shares_count(selector),
        "comments_count": comments_count(selector),
        "summary": "".join(
            selector.css(
                '.tec--article__body > p:nth-child(1) *::text').getall()
        ),
        "sources": get_sources(selector),
        "categories": get_categories(selector),
    }


# Requisito 3
def scrape_novidades(html_content):
    """Seu código deve vir aqui"""
    selector = Selector(html_content)
    urls = selector.css(
        '.tec--list__item .tec--card__title__link ::attr(href)'
    ).getall()
    return urls


# Requisito 4
def scrape_next_page_link(html_content):
    """Seu código deve vir aqui"""
    selector = Selector(html_content)
    next_page_url = selector.css(
        '.z--mt-48 ::attr(href)'
    ).get()
    if next_page_url is not None:
        return next_page_url
    return None


# Requisito 5
def get_tech_news(amount):
    """Seu código deve vir aqui"""
    BASE_URL = 'https://www.tecmundo.com.br/novidades'
    news_html = fetch(BASE_URL)
    news_url = scrape_novidades(news_html)
    if len(news_url) < amount:
        while(len(news_url) < amount):
            next_page = fetch(scrape_next_page_link(news_html))
            news_url += scrape_novidades(next_page)

    infos_news = [scrape_noticia(fetch(new)) for new in news_url[0:amount]]
    create_news(infos_news)
    return infos_news
