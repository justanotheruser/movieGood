import asyncio
import re
import tempfile
import lxml
from lxml import etree
import os
import math
from typing import List

from movieGood.fetch import fetch
from movieGood.exceptions import InvalidLinkException, ParsingFailedException

FLASK_G_URL = ''
# Limitation of kinopoisk
MAX_RATINGS_PER_PAGE = 200


class MovieInfo:
    def __init__(self, rus_title, orig_title, year, rating):
        self.rus_title = rus_title
        self.orig_title = orig_title
        self.year = year
        self.rating = rating

    def __eq__(self, other):
        return self.rus_title == other.rus_title and \
               self.orig_title == other.orig_title and \
               self.year == other.year and \
               self.rating == other.rating

    def __repr__(self):
        return f'"{self.rus_title}", "{self.orig_title}", {self.year}, {self.rating}'


async def get_kinopoisk_ratings(client, url):
    ratings = []
    pages = await get_kinopoisk_pages(client, url)
    for page in pages:
        ratings.extend(parse_page_tree(get_page_tree(page)))
    return ratings


async def get_kinopoisk_pages(client, url) -> List[str]:
    root_url = get_root_votes_page(url)
    first_page = await fetch(client, root_url)
    FLASK_G_URL = root_url
    first_page_tree = get_page_tree(first_page)
    total_ratings = get_total_ratings_amount(first_page_tree)
    if not total_ratings:
        return [first_page]
    total_pages = math.ceil(total_ratings / MAX_RATINGS_PER_PAGE)
    pages_urls = [root_url + f'list/ord/date/perpage/{MAX_RATINGS_PER_PAGE}/page/{i}/'
                  for i in range(2, total_pages + 1)]
    pages_fut = await fetch_pages(client, pages_urls)
    # todo: try-except
    pages = pages_fut.result()
    return [first_page] + pages


def get_root_votes_page(url: str):
    match = re.search(r'(https://www.kinopoisk.ru/user/\d{1,}/).*', url)
    if not match:
        raise InvalidLinkException(url, 'Ссылка не является ссылкой на профиль пользователя Кинопоиска')
    return match.group(1) + 'votes/'


def get_page_tree(page: str) ->  lxml.etree._ElementTree:
    with tempfile.TemporaryDirectory() as tmpdirname:
        tmpfilename = os.path.join(tmpdirname, 'page.html')
        with open(tmpfilename, 'w', encoding='utf-8') as f:
            f.write(page)
        return etree.parse(tmpfilename, etree.HTMLParser())


def get_total_ratings_amount(tree: lxml.etree._ElementTree):
    """ Returns total amount of ratings or None if there's only one page """
    pagesFromTo = list(tree.xpath('//div[@class="pagesFromTo"]/text()'))
    if not pagesFromTo:
        return None
    pagesFromTo = pagesFromTo[0]
    pagesFromToRegex = r'1—\d{1,}.*?(\d{1,})'
    match = re.search(pagesFromToRegex, pagesFromTo)
    if not match:
        raise ParsingFailedException(FLASK_G_URL, tree,
                                     f"Expected 'pagesFromTo' to contain '{pagesFromToRegex}',"
                                     f"instead found '{pagesFromTo}'")
    return int(match.group(1))


async def fetch_pages(client, pages_urls):
    tasks = []
    for url in pages_urls:
        task = asyncio.create_task(fetch(client, url))
        tasks.append(task)
    responses = asyncio.gather(*tasks)
    await responses
    return responses


def parse_page_tree(tree: lxml.etree._ElementTree):
    movies = []
    items = tree.xpath('//div[@class="profileFilmsList"]/div[contains(@class, "item")]')
    for item in items:
        movies.append(parse_item(item))
    return movies


def parse_item(item):
    rus_title = list(item.xpath('.//div[@class="nameRus"]/a/text()'))
    if rus_title:
        rus_title = rus_title[0]
    else:
        raise ParsingFailedException(FLASK_G_URL, item, 'Expected to find "nameRus"')

    title_regexs = [
        r'(.*?) \((\d{4})\)',
        r'(.*?) \(сериал, (\d{4})',
        r'(.*?) \(мини-сериал, (\d{4})'
    ]
    match = None
    for regex in title_regexs:
        match = re.search(regex, rus_title)
        if match:
            break
    if match:
        rus_title = match.group(1)
        year = int(match.group(2))
    else:
        raise ParsingFailedException(FLASK_G_URL, item, f'Unexpted format of rus title {rus_title}')

    orig_title = list(item.xpath('.//div[@class="nameEng"]/text()'))
    if orig_title:
        orig_title = orig_title[0]
    else:
        raise ParsingFailedException(FLASK_G_URL, item, 'Expected to find "nameEng"')
    if orig_title == ' ':
        orig_title = None

    rating = list(item.xpath('.//div[@class="vote"]/text()'))
    if rating:
        rating = int(rating[0])
    else:
        raise ParsingFailedException(FLASK_G_URL, item, 'Expected to find "vote"')

    return MovieInfo(rus_title, orig_title, year, rating)
