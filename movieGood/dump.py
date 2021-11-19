import asyncio
import os
from typing import Optional

import click

import imdb
import kinopoisk
from movieGood.exceptions import ParsingFailedException


@click.command()
@click.option('--url', help='URL of ratings page of Kinopoisk or IMDB')
@click.option('--output', default=None, help='Name of .csv file with scarped ratings;'
                                             ' defaults to name based on site and profile id')
@click.option('--lang', default='en', help='Title language for IMDB')
def dump(url: str, output: Optional[str], lang: str):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(async_dump(url, output, lang))


async def async_dump(url: str, output: Optional[str], language: str):
    site, user_id = get_site_and_user_id(url)
    try:
        if site == 'kinopoisk':
            movies_df = await kinopoisk.get_movies(url)
        elif site == 'imdb':
            movies_df = await imdb.get_movies(url, language)
        else:
            print('Not supported URL format')
            return
    except ParsingFailedException as e:
        dump_id = get_dump_id(site, user_id, language)
        failed_item_file = os.path.join(dump_dir_name(),
                                        f'{dump_id}_parsing_failed.html')
        e.tree.write(failed_item_file, pretty_print=True, encoding='utf-8')
        print(e.message)
        print(f'Problematic tree was dumped into {failed_item_file}')
        return

    if not output:
        dump_id = get_dump_id(site, user_id, language)
        output = os.path.join(dump_dir_name(), f'{dump_id}.csv')
    movies_df.to_csv(output, index=False)


def get_dump_id(site, user_id, language):
    if site == 'imdb':
        return f'{site}_{user_id}_{language}'
    else:
        return f'{site}_{user_id}'

def dump_dir_name():
    dir_name, _ = os.path.split(__file__)
    return os.path.join(dir_name, 'dump')


def get_site_and_user_id(url: str):
    _, user_id = kinopoisk.get_first_page_and_user_id(url)
    if user_id:
        return 'kinopoisk', user_id
    _, user_id = imdb.get_first_page_and_user_id(url)
    if user_id:
        return 'imdb', user_id
    return None, None


if __name__ == '__main__':
    dump()
