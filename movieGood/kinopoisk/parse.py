import re

import lxml

from movieGood.exceptions import ParsingFailedException
from movieGood.kinopoisk.movie_info import MovieInfo


def parse_page_tree(tree: lxml.etree._ElementTree):
    movies = []
    items = tree.xpath('//div[@class="profileFilmsList"]/div[contains(@class, "item")]')
    for item in items:
        movies.append(parse_item(item))
    return movies


def parse_item(item):
    rus_title, year = parse_rus_title_and_year(item)
    orig_title = parse_orig_title(item)
    rating = parse_rating(item)
    return MovieInfo(rus_title, orig_title, year, rating)


def parse_rating(item):
    vote = list(item.xpath('.//div[@class="vote"]'))
    if not vote:
        raise ParsingFailedException("FLASK_G_URL", item, 'Expected to find "vote"')
    rating = vote[0].xpath('./text()')
    if rating:
        rating = int(str(rating[0]))
    else:
        # Watched but not rated
        rating = None
    return rating


def parse_orig_title(item):
    orig_title = list(item.xpath('.//div[@class="nameEng"]/text()'))
    if orig_title:
        orig_title = orig_title[0]
    else:
        raise ParsingFailedException("FLASK_G_URL", item, 'Expected to find "nameEng"')
    if re.match(r'^\s*$', orig_title):
        orig_title = None
    return orig_title


def parse_rus_title_and_year(item):
    rus_title = list(item.xpath('.//div[@class="nameRus"]/a/text()'))
    if rus_title:
        rus_title = rus_title[0]
    else:
        raise ParsingFailedException("FLASK_G_URL", item, 'Expected to find "nameRus"')
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
        raise ParsingFailedException("FLASK_G_URL", item, f'Unexpected format of rus title {rus_title}')
    return rus_title, year
