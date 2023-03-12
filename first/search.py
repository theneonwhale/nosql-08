import connect

from models import Authors, Quotes


def search_quote_by_tag(query):
    result = []
    quotes = Quotes.objects()
    for quote in quotes:
        if query in quote.tags:
            result.append(quote.quote)
    print('result', result)
    return result


def search_quotes_by_author(query):
    result = []
    quotes = Quotes.objects()
    authors = Authors.objects()
    author_id = [author.id for author in authors if author.fullname == query][0]
    for quote in quotes:
        if author_id == quote.author.id:
            result.append(quote.quote)
    print('result', result)
    return result


def search_quote_by_tags(query):
    result = []
    tags = query.split(',')
    quotes = Quotes.objects()
    for tag in tags:
        for quote in quotes:
            if tag in quote.tags and quote.quote not in result:
                result.append(quote.quote)
    print('result', result)
    return result


def main():
    run = True
    while run:
        command = input('Enter command: ')
        command_length = len(command.split(':'))
        if command_length == 2:
            func = command.split(':')[0]
            query = command.split(':')[1]
            match func:
                case 'tag':
                    search_quote_by_tag(query)
                case 'author':
                    search_quotes_by_author(query)
                case 'tags':
                    search_quote_by_tags(query)
                case _:
                    print('Unknown command. Try again.')
        elif command_length == 1:
            func = command.split(':')[0]
            if func == 'exit':
                run = False
                print('Bye!')
            else:
                print('Unknown command. Try again.')
        else:
            print('Unknown command. Try again.')


if __name__ == '__main__':
    main()
