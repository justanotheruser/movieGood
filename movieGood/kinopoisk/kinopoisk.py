import aiohttp
import pandas as pd
from transliterate import translit

from movieGood.kinopoisk.fetch_pages import get_kinopoisk_pages, get_page_tree
from movieGood.kinopoisk.parse import parse_page_tree


async def get_movies(url) -> pd.DataFrame:
    rus_title, orig_title, year, rating = [], [], [], []
    async with aiohttp.ClientSession() as client:
        pages = await get_kinopoisk_pages(client, url)
    for page in pages:
        page_rus_title, page_orig_title, page_year, page_rating = parse_page_tree(get_page_tree(page))
        rus_title.extend(page_rus_title)
        orig_title.extend(page_orig_title)
        year.extend(page_year)
        rating.extend(page_rating)

    is_rus = [False] * len(orig_title)
    for i in range(len(orig_title)):
        if not orig_title[i]:
            is_rus[i] = True
            orig_title[i] = transliterate(rus_title[i])

    return pd.DataFrame({'title_ru': rus_title, 'is_rus': is_rus,
                         'orig_title': orig_title,
                         'year': year, 'rating': rating})


def transliterate(rus_title):
    orig_title: str = translit(rus_title, 'ru', reversed=True)
    orig_title = orig_title.replace('ja', 'ya')
    orig_title = orig_title.replace('ju', 'yu')
    orig_title = orig_title.replace('«', "'").replace('»', "'")
    return orig_title
