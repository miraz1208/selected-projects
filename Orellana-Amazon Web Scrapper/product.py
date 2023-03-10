"""
This class deals with product information.
1. Product Name
2. Product ASIN
3. Price
4. Sponsorship status
5. Product Rating
6. Product Review
"""

import re


class Product:
    """Product information"""

    def __init__(self) -> None:
        pass

    def get_name_url(self, item) -> str:
        """Derives item url from input ResultSet object"""
        try:
            atag = item.h2.a
            description = atag.text.strip()
            url = "https://www.amazon.com" + atag.get("href")
        except AttributeError:
            description = ""
            url = ""

        to_return = (description, url)
        return to_return

    def get_asin(self, url) -> str:
        """Derives ASIN from input url"""
        asin_group = re.search(r"B[A-Z0-9]{9}", url)
        try:
            asin = asin_group.group(0)
        except AttributeError:
            asin = "Not Found"

        return asin

    def get_price(self, item) -> str:
        """Derives sponsorship status from input html text"""
        try:
            price_parent = item.find("span", "a-price")
            price = price_parent.find("span", "a-offscreen").text
        except AttributeError:
            price = "N/S"

        return price

    def get_sponsorship(self, item) -> str:
        """Derives sponsorship status from input html text"""
        try:
            sponsor = item.find("span", {"class": "a-color-base"}).text
            if sponsor == "Sponsored":
                status = "Yes"
            else:
                status = "No"
        except AttributeError:
            status = ""
        return status

    def get_rating_review(self, item) -> tuple:
        """Derives rating & review from input html text"""
        try:
            rating = item.find("span", "a-icon-alt").text.split(" ")[0]
            reviews = item.find(
                "span", {"class": "a-size-base s-underline-text"}
            ).text
            total_review = reviews.replace('-', '')

        except (AttributeError, ValueError):
            rating = "0"
            total_review = "0"
        collection = (rating, total_review)
        return collection
