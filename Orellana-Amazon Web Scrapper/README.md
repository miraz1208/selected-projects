# Orellana
Amazon is the most popular online shop, selling millions of products.

This program is called '*Orellana*'-
named after one of the world's foremost explorer on the Amazon Rainforest.

This program takes a product name, start search results page
and end search result page number as input,
analyzes the search results, filters out the
already recorded results and then
writes a csv file of the overall search results.

##### Video demo:
<https://youtu.be/mRpaz1-SeaM>

## Libraries

The program uses the following libraries:

- `csv`: to write CSV file.
- `sys`: to exit the program.
- `time.sleep`: to initiate delay in program execution.
- `datetime`: to name file avoiding overwriting.
- `requests`: to request content from web.
- `bs4.BeautifulSoup`: to read HTML Data.
- `lxml`: to parse the collected HTML data.
- `autocorrect.Speller`: to check input spelling.
- `goto_web.GotoWeb`: custom class, gets access to the web.
- `fake_useragent`: Bypass security robot check at website
- `product.Product`: custom class, deals with product details.

### `main()` Function

The `main()` function is the entry point of the program. It includes an infinite loop that keeps asking the user to input a product name. The input is then validated using the `validate_product_name()` function. If the input is valid, the program generates a valid URL using the `get_url()` function, compiles all search and filtered results using the `compiler()` function, and saves the results as a CSV file using the `save_as()` function.

### `validate_product_name()` Function

The `validate_product_name()` function is used to validate the input from the user. The function checks if the input is all integers, and if not, it checks the spelling of the input using the `autocorrect.Speller` library. If the spelling is incorrect, the program asks the user if they meant the suggested spelling.

### `page_start_end()` Function

The `page_start_end()` function is used to get the start page and end page of the search. The function checks if the input is a number and if the end page is greater than the start page.

### `get_url()` Function

The `get_url()` function is used to generate a URL with the product name embedded.

### `scrapper()` Function

The `scrapper()` function is used to get input URL and returns a `ResultSet` object.

### `compiler()` Function

The `compiler()` function compiles all the results. It takes a URL, start page number, and end page number as input and returns a list of all gathered results after filtering.
A sleep function is used to cause delay in the search to avoid being blocked by the website.

### `save_as()` Function

The `save_as()` function saves the search result in CSV format.
