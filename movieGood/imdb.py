import tempfile
import lxml
from lxml import etree
import os

from fetch import fetch


async def imdb_ratings_pages(client, start_page_url):
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


async def get_imdb_ratings(client, url):
    ratings = []
    async for page_tree in imdb_ratings_pages(client, url):
        ratings.extend(parse_imdb_ratings_page(page_tree))
    return ratings


def parse_imdb_ratings_page(tree: lxml.etree._ElementTree):
    ratings = list(tree.xpath('//div[@class="ipl-rating-star ipl-rating-star--other-user small"]'
                              '/span[@class="ipl-rating-star__rating"]/text()'))
    titles = list(tree.xpath('//h3[@class="lister-item-header"]/a/text()'))
    years = list(tree.xpath('//h3[@class="lister-item-header"]'
                            '/span[contains(@class, "lister-item-year")]/text()'))
    years = [y[1:-1] for y in years]  # removing () brackets
    movies = list(zip(titles, years, ratings))
    return movies
