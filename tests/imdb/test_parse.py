import os

import pytest
from lxml import etree

from movieGood.imdb.parse import parse_ratings_page


@pytest.mark.parametrize('item_file, exp_result',
                         [('imdb_movie_item.html',
                           (['Матрица: Революция'], ['tt0242653'], [2003], [6]))
                          ])
def test_parse_item(item_file, exp_result):
    dir_path, _ = os.path.split(__file__)
    item_file = os.path.join(dir_path, 'tests_data', item_file)
    with open(item_file, 'r', encoding='utf-8') as f:
        lines = ''.join(f.readlines())
    item = etree.fromstring(lines, etree.HTMLParser())
    result = parse_ratings_page(item)
    assert result == exp_result
