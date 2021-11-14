from movieGood import kinopoisk
import pytest
import os
from lxml import etree

@pytest.mark.parametrize('input_url, result_url',
                         [('https://www.kinopoisk.ru/user/3669404/votes/',
                           'https://www.kinopoisk.ru/user/3669404/votes/'),
                          ('https://www.kinopoisk.ru/user/3669404/',
                           'https://www.kinopoisk.ru/user/3669404/votes/'),
                          ('https://www.kinopoisk.ru/user/3669404/votes/list/ord/date/page/',
                           'https://www.kinopoisk.ru/user/3669404/votes/')
                          ])
def test_get_root_votes_page(input_url, result_url):
    assert result_url == kinopoisk.get_root_votes_page(input_url)


@pytest.mark.parametrize('item_file, exp_result',
                         [('kinopoisk_series_item.html',
                          kinopoisk.MovieInfo('Во все тяжкие', 'Breaking Bad', 2008, 10))])
def test_parse_item(item_file, exp_result):
    dir_path, _ = os.path.split(__file__)
    item_file = os.path.join(dir_path, 'tests_data', item_file)
    with open(item_file, 'r', encoding='utf-8') as f:
        lines = ''.join(f.readlines())
    item = etree.fromstring(lines, etree.HTMLParser())
    result = kinopoisk.parse_item(item)
    assert result == exp_result
