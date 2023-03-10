"""
Amazon is the most popular online shop, selling millions of products.

This program is called 'Orellana'-
named after one of the world's foremost explorer on the Amazon Rainforest.

This program takes a product name, start search results page
and end search result page number as input,
analyzes the search results, filters out the
already recorded results and then
writes a csv file of the overall search results.
"""


# pylint: disable=E1101
import csv  # To write CSV file
import sys  # To exit program
from time import sleep  # To initiate delay in program execution
from datetime import datetime  # To name file avoiding overwriting
from bs4 import BeautifulSoup  # To read HTML Data
from autocorrect import Speller  # To check input spelling
from goto_web import GotoWeb  # Custom class, gets access to web
from product import Product  # Custom class, deals with product details


def main() -> None:
    '''Main function'''
    while True:
        try:
            product: str = validate_product_name()
            formatted = product.replace(' ', '+')
            start, end = page_start_end()
            end += 1
            # Generate valid url
            url = get_url(formatted)

            # Compiles all search & filtered result
            results = compiler(url, start, end)

            # Save results as CSV file
            save_as(product, results)
            sys.exit()

        except KeyboardInterrupt:
            print('\n Exiting program...')
            sys.exit()

        except TypeError:
            print('\n TypeError occurred...Exiting...')
            sys.exit()

        except EOFError:
            print('\n EOF Occurred...')
            sys.exit()


def validate_product_name() -> str:
    '''Validates the input from user'''
    while True:
        product: str = input("Please input a Product name: ").lower()
        try:
            product = int(product)
            print('Product name cannot be all integers')
        except ValueError:
            product = product.lower()
            check = Speller(lang='en')
            word = check(product)
            if word != product:
                ans = input(f'Did you mean- {word}? (Y/N)').lower().strip()
                if ans == 'Y':
                    product = word
                else:
                    continue
            return product


def page_start_end() -> tuple:
    '''
    Get start page and end page of search
    input: int
    output: tuple
    '''
    while True:
        try:
            start = int(input('Start search from page(Number): '))
            if start == 0:
                print('Start page can not be 0')
                continue
            break
        except ValueError:
            print('Please enter a number')
            continue

    while True:
        try:
            end = int(input('End search at page(Number): '))
        except ValueError:
            print('Please enter a number')
            continue
        if end <= start:
            print('''Endpage number cannot be lower
                  or equal to than Start page number.''')
            sleep(1)
            print(f'Please enter a number higher than {start}')
            continue
        break
    print(f'Searching results from page {start} to {end}')
    return (start, end)


def get_url(name: str) -> str:
    '''Generates url with product name embedded'''

    site_address = f'https://www.amazon.com/s?k={name}&ref=nb_sb_noss'
    site_address += '&page={}'  # Placeholder to enter page number
    return site_address


def scrapper(url: str):
    '''Gets input url
    returns ResultSet object'''

    try:
        access = GotoWeb()
        content = access.web(url)
        soup = BeautifulSoup(content, 'lxml')

        search_results = soup.find_all(
            'div',
            {
                'data-component-type': 's-search-result'
            })
        return search_results
    except TypeError:
        return None


def compiler(url: str, start: int, end: int) -> list:
    '''
    Compiles all the results.
    Takes URL, start page no and end page no as input
    Returns List of all gathered results after filter
    '''

    # Empty results list, to be appended with filtered results later
    results = []
    # To keep track of recorded ASIN's, first an empty list is created
    all_asins = []

    # Iterate through all pages in search result
    for page in range(start, end):
        print('----------------------------------')
        print(f'Gathering Data from page {page}...')
        print('----------------------------------')

        sleep(10)

        items = scrapper(url.format(page))

        for count, item in enumerate(items):
            product = Product()
            print(f'Analyzing item {count + 1}')

            # Get product name and product url
            name, url_2 = product.get_name_url(item)

            asin = product.get_asin(url_2)

            # Get price
            price = product.get_price(item)

            # Check if sponsored or not
            status = product.get_sponsorship(item)

            # Get rating & total review
            rating, review = product.get_rating_review(item)

            # Filter results
            if asin not in all_asins:

                print(f'Gathering data of item {count + 1}')

                # Append selected ASIN to all_asins list to keep track
                all_asins.append(asin)

                # Send selected item info to final result list
                results.append((page,
                                name,
                                asin,
                                price,
                                status,
                                rating,
                                review))

            else:
                # Message to notify that unsaved result was skipped
                print(f'Skipping item {count + 1}')

    print(f'Compiling {len(all_asins)} search results...')

    return results


def save_as(search: str, description: list) -> None:
    '''Saves search result in CSV format'''

    print('Now writing file...')

    now = str(datetime.now()).replace(":", ".")

    with open(f'outputs/{search}_{now}.csv',
              'w',
              newline='',
              encoding='utf-8'
              ) as file:
        writer = csv.writer(file)
        writer.writerow([
            'Page',
            'Name',
            'ASIN',
            'Price',
            'Sponsored',
            'Rating',
            'Total Reviews'
            ])
        writer.writerows(description)
    print('___File saved!___')
    sys.exit()


if __name__ == '__main__':
    main()
