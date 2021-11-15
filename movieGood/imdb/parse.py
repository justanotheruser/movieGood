import lxml
import re


def parse_ratings_page(tree: lxml.etree._ElementTree):
    titles = parse_titles(tree)
    imdb_title_ids = parse_imdb_title_ids(tree)
    years = parse_years(tree)
    ratings = parse_ratings(tree)
    return titles, imdb_title_ids, years, ratings


def parse_titles(tree):
    titles = list(tree.xpath('//h3[@class="lister-item-header"]/a/text()'))
    return titles


def parse_imdb_title_ids(tree):
    imdb_title_hrefs = list(tree.xpath('//h3[@class="lister-item-header"]/a/@href'))
    imdb_title_ids = [re.search(r'https://www.imdb.com/title/(tt\d+)/.*', href).group(1)
                      for href in imdb_title_hrefs]
    return imdb_title_ids


def parse_years(tree):
    years = list(tree.xpath('//h3[@class="lister-item-header"]'
                            '/span[contains(@class, "lister-item-year")]/text()'))
    years = [int(y[1:5]) for y in years]  # removing () brackets
    return years


def parse_ratings(tree):
    ratings = list(tree.xpath('//div[@class="ipl-rating-star ipl-rating-star--other-user small"]'
                              '/span[@class="ipl-rating-star__rating"]/text()'))
    ratings = [int(r) for r in ratings]
    return ratings
