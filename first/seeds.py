import json

import connect

from models import Authors, Quotes


def seed_authors():
    with open('data/authors.json') as file:
        for author_data in json.load(file):
            author = Authors(
                fullname=author_data.get('fullname'),
                born_date=author_data.get('born_date'),
                born_location=author_data.get('born_location'),
                description=author_data.get('description')
            )
            author.save()


def seed_quotes():
    with open('data/quotes.json') as file:
        for quote_data in json.load(file):
            quote = Quotes(
                tags=quote_data.get("tags"),
                author=Authors.objects(fullname=quote_data.get("author"))[0].id,
                quote=quote_data.get("quote")
            )
            quote.save()


if __name__ == '__main__':
    seed_authors()
    seed_quotes()
