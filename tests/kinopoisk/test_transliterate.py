import pytest
from movieGood.kinopoisk.kinopoisk import transliterate

@pytest.mark.parametrize('rus_title, exp_orig_title',
                         [("Операция «Ы» и другие приключения Шурика",
                           "Operatsiya 'Y' i drugie priklyucheniya Shurika"),
                          ("Бриллиантовая рука",
                           "Brilliantovaya ruka")])
def test_transliterate(rus_title, exp_orig_title):
    orig_title = transliterate(rus_title)
    assert exp_orig_title == orig_title
