import asyncio
import aiohttp
import tempfile
import lxml
from lxml import etree
import os


async def get_imdb_ratings(client, url):
    imdb_page = await fetch(client, url)
    with tempfile.TemporaryDirectory() as tmpdirname:
        tmpdirname = '.'
        tmpfilename = os.path.join(tmpdirname, 'imdb_page.html')
        with open(tmpfilename, 'w', encoding='utf-8') as f:
            f.write(imdb_page)
        imdb_page_tree: lxml.etree._ElementTree = etree.parse(tmpfilename, etree.HTMLParser())
    return parse_imdb_ratings_page(imdb_page_tree)


def parse_imdb_ratings_page(tree):
    ratings = list(tree.xpath('//label[@class="ipl-rating-interactive__star-container"]'
                              '/div[@class="ipl-rating-star ipl-rating-interactive__star"]'
                              '/span[@class="ipl-rating-star__rating"]/text()'))
    titles = list(tree.xpath('//h3[@class="lister-item-header"]/a/text()'))
    years = list(tree.xpath('//h3[@class="lister-item-header"]'
                            '/span[contains(@class, "lister-item-year")]/text()'))
    years = [y[1:-1] for y in years]  # removing () brackets
    movies = list(zip(titles, years, ratings))
    return movies


def get_kinopoisk_ratings():
    pass


async def fetch(client, url):
    async with client.get(url) as resp:
        assert resp.status == 200
        return await resp.text()


async def main():
    async with aiohttp.ClientSession() as client:
        imdb_ratings = await get_imdb_ratings(client,
                                              'https://www.imdb.com/user/ur58128213/ratings')
        print(imdb_ratings)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
