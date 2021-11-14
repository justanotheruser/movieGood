from movieGood.kinopoisk.fetch_pages import get_kinopoisk_pages, get_page_tree
from movieGood.kinopoisk.parse import parse_page_tree
from transliterate import translit


async def get_movies(client, url):
    movies = []
    pages = await get_kinopoisk_pages(client, url)
    for page in pages:
        movies.extend(parse_page_tree(get_page_tree(page)))
    for i in range(len(movies)):
        if not movies[i].orig_title:
            movies[i].orig_title = transliterate(movies[i].rus_title)
    return movies


def transliterate(rus_title):
    orig_title: str = translit(rus_title, 'ru', reversed=True)
    orig_title = orig_title.replace('ja', 'ya')
    orig_title = orig_title.replace('ju', 'yu')
    orig_title = orig_title.replace('«', "'").replace('»', "'")
    return orig_title
