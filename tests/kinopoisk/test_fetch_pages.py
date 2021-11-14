import pytest

from movieGood.kinopoisk.fetch_pages import get_root_votes_page


@pytest.mark.parametrize('input_url, result_url',
                         [('https://www.kinopoisk.ru/user/3669404/votes/',
                           'https://www.kinopoisk.ru/user/3669404/votes/'),
                          ('https://www.kinopoisk.ru/user/3669404/',
                           'https://www.kinopoisk.ru/user/3669404/votes/'),
                          ('https://www.kinopoisk.ru/user/3669404/votes/list/ord/date/page/',
                           'https://www.kinopoisk.ru/user/3669404/votes/')
                          ])
def test_get_root_votes_page(input_url, result_url):
    assert result_url == get_root_votes_page(input_url)