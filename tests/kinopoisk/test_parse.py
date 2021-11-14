from movieGood.kinopoisk.movie_info import MovieInfo
from movieGood.kinopoisk.parse import parse_item
import pytest
import os
from lxml import etree


@pytest.mark.parametrize('item_file, exp_result',
                         [('kinopoisk_series_item.html',
                           MovieInfo('Во все тяжкие', 'Breaking Bad', 2008, 10)),
                          ('kinopoisk_miniseries_item.html',
                           MovieInfo('Чернобыль', 'Chernobyl', 2019, None)),
                          ('kinopoisk_movie_item.html',
                           MovieInfo('Белфегор – призрак Лувра',
                                     'Belphégor - Le fantôme du Louvre', 2001, 5)),
                          ('kinopoisk_rus_movie_item.html',
                           MovieInfo('Бриллиантовая рука', None, 1968, 9)),
                          ('kinopoisk_watched_item.html',
                           MovieInfo('Остров собак', 'Isle of Dogs', 2018, None))])
def test_parse_item(item_file, exp_result):
    dir_path, _ = os.path.split(__file__)
    item_file = os.path.join(dir_path, 'tests_data', item_file)
    with open(item_file, 'r', encoding='utf-8') as f:
        lines = ''.join(f.readlines())
    item = etree.fromstring(lines, etree.HTMLParser())
    result = parse_item(item)
    assert result == exp_result
