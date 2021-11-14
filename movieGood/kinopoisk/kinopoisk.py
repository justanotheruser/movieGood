from movieGood.kinopoisk.fetch_pages import get_kinopoisk_pages, get_page_tree
from movieGood.kinopoisk.parse import parse_page_tree


async def get_ratings(client, url):
    ratings = []
    pages = await get_kinopoisk_pages(client, url)
    for page in pages:
        ratings.extend(parse_page_tree(get_page_tree(page)))
    return ratings


