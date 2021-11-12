import lxml
from lxml import etree


def get_imdb_ratings():
    return parse_imdb_ratings_page(r'.\test_data\Your Ratings - IMDb.html')


def parse_imdb_ratings_page(page):
    html_parser = etree.HTMLParser()
    tree: lxml.etree._ElementTree = etree.parse(page, html_parser)
    ratings = list(tree.xpath('//label[@class="ipl-rating-interactive__star-container"]'
                              '/div[@class="ipl-rating-star ipl-rating-interactive__star"]'
                              '/span[@class="ipl-rating-star__rating"]/text()'))
    titles = list(tree.xpath('//h3[@class="lister-item-header"]/a/text()'))
    years = list(tree.xpath('//h3[@class="lister-item-header"]'
                            '/span[contains(@class, "lister-item-year")]/text()'))
    years = [y[1:-1] for y in years]  # removing () brackets
    movies = list(zip(titles, years, ratings))
    return movies


def get_kinopoisk_ratings():
    pass

if __name__ == '__main__':
    # https://www.imdb.com/user/ur58128213/ratings
    get_imdb_ratings()
