from tech_news.database import search_news
import datetime


def query_and_create_tupla(find_where, find_what):
    news = search_news({find_where: {'$regex': find_what, '$options': 'i'}})
    list_news = []
    for new in news:
        list_news.append((new["title"], new["url"]))

    return list_news


# Requisito 6
def search_by_title(title):
    return query_and_create_tupla('title', title)


# https://www.kite.com/python/answers/how-to-validate-a-date-string-format-in-python
# Requisito 7
def search_by_date(date):
    format = "%Y-%m-%d"
    try:
        datetime.datetime.strptime(date, format)
        return query_and_create_tupla('timestamp', date)
    except ValueError:
        raise ValueError('Data inválida')


# Requisito 8
def search_by_source(source):
    return query_and_create_tupla('sources', source)


# Requisito 9
def search_by_category(category):
    return query_and_create_tupla('categories', category)
