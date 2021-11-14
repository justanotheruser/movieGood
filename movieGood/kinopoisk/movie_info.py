class MovieInfo:
    def __init__(self, rus_title, orig_title, year, rating):
        self.rus_title = rus_title
        self.orig_title = orig_title
        self.year = year
        self.rating = rating

    def __eq__(self, other):
        return self.rus_title == other.rus_title and \
               self.orig_title == other.orig_title and \
               self.year == other.year and \
               self.rating == other.rating

    def __repr__(self):
        return f'"{self.rus_title}", "{self.orig_title}", {self.year}, {self.rating}'