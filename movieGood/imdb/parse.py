import re

import lxml

from movieGood.exceptions import ParsingFailedException


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
    try:
        imdb_title_ids = [re.search(r'/title/(tt\d+)/.*', href).group(1)
                          for href in imdb_title_hrefs]
    except AttributeError:
        raise ParsingFailedException("FLASK_G_URL", tree,
                                     'Failed to parse IMDB title ids')
    return imdb_title_ids


def parse_years(tree):
    years = list(tree.xpath('//h3[@class="lister-item-header"]'
                            '/span[contains(@class, "lister-item-year")]/text()'))
    try:
        cur_year = None
        for i in range(len(years)):
            cur_year = years[i]
            # Roman numerals are used to distinguish movies that share title and release year.
            # If this is TV show use show's starting year.
            years[i] = int(re.match(r'(?:\(I+\) )?\((\d{4}).*', years[i]).group(1))
    except:
        raise ParsingFailedException("FLASK_G_URL", tree,
                                     f'Failed to parse year: "{cur_year}"')
    return years


def parse_ratings(tree):
    ratings = list(tree.xpath('//div[@class="ipl-rating-star ipl-rating-star--other-user small"]'
                              '/span[@class="ipl-rating-star__rating"]/text()'))
    try:
        ratings = [int(r) for r in ratings]
    except ValueError:
        raise ParsingFailedException("FLASK_G_URL", tree,
                                     'Failed to parse ratings')
    return ratings
