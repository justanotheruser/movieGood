import tempfile
import lxml
from lxml import etree
import os
import aiohttp
import pandas as pd

from movieGood.fetch import fetch
from movieGood.imdb.parse import parse_ratings_page


async def get_movies(url, title_language='en'):
    titles, imdb_title_ids, years, ratings = [], [], [], []
    headers = {'Accept-Language': title_language}
    async with aiohttp.ClientSession(headers=headers) as client:
        async for page_tree in ratings_pages(client, url):
            page_titles, page_imdb_title_ids, page_years, page_ratings = parse_ratings_page(page_tree)
            titles.extend(page_titles)
            imdb_title_ids.extend(page_imdb_title_ids)
            years.extend(page_years)
            ratings.extend(page_ratings)
    return pd.DataFrame({'imdb_title_id': imdb_title_ids,
                         f'title_{title_language}': titles,
                         'year': years, 'rating': ratings})



async def ratings_pages(client, start_page_url):
    next_page_link = start_page_url
    while next_page_link:
        page = await fetch(client, next_page_link)
        with tempfile.TemporaryDirectory() as tmpdirname:
            tmpfilename = os.path.join(tmpdirname, 'page.html')
            with open(tmpfilename, 'w', encoding='utf-8') as f:
                f.write(page)
            tree: lxml.etree._ElementTree = etree.parse(tmpfilename, etree.HTMLParser())
            yield tree
            next_page_link = list(tree.xpath('//div[@class="list-pagination"]'
                                             '/a[(contains(@class, "next-page")'
                                             '    and not(contains(@class, "disabled")))]/@href'))
            if next_page_link:
                next_page_link = 'https://www.imdb.com' + next_page_link[0]


