import pytest

from movieGood.kinopoisk import get_first_page_and_user_id


@pytest.mark.parametrize('input_url, first_page_url, user_id',
                         [('https://www.kinopoisk.ru/user/3669404/votes/',
                           'https://www.kinopoisk.ru/user/3669404/votes/', '3669404'),
                          ('https://www.kinopoisk.ru/user/3669404/',
                           'https://www.kinopoisk.ru/user/3669404/votes/', '3669404'),
                          ('https://www.kinopoisk.ru/user/3669404/votes/list/ord/date/page/',
                           'https://www.kinopoisk.ru/user/3669404/votes/', '3669404')
                          ])
def test_get_root_votes_page(input_url, first_page_url, user_id):
    result_url, result_user_id = get_first_page_and_user_id(input_url)
    assert result_url == first_page_url
    assert result_user_id == user_id