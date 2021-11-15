import asyncio
import math
import os
import re
import tempfile
from typing import List

import lxml
from lxml import etree

from movieGood.exceptions import InvalidLinkException, ParsingFailedException
from movieGood.fetch import fetch

# Limitation of kinopoisk
MAX_RATINGS_PER_PAGE = 200


async def get_kinopoisk_pages(client, url) -> List[str]:
    first_page_url, _ = get_first_page_and_user_id(url)
    first_page = await fetch(client, first_page_url)
    FLASK_G_URL = first_page
    first_page_tree = get_page_tree(first_page)
    total_ratings = get_total_ratings_amount(first_page_tree)
    if not total_ratings:
        return [first_page]
    total_pages = math.ceil(total_ratings / MAX_RATINGS_PER_PAGE)
    pages_urls = [first_page_url + f'list/ord/date/perpage/{MAX_RATINGS_PER_PAGE}/page/{i}/'
                  for i in range(2, total_pages + 1)]
    pages_fut = await fetch_pages(client, pages_urls)
    # todo: try-except
    pages = pages_fut.result()
    return [first_page] + pages


def get_first_page_and_user_id(url: str):
    match = re.search(r'(https://www.kinopoisk.ru/user/(\d+)/).*', url)
    if not match:
        return None, None
    return match.group(1) + 'votes/', match.group(2)


def get_page_tree(page: str) -> lxml.etree._ElementTree:
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
        raise ParsingFailedException("FLASK_G_URL", tree,
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
