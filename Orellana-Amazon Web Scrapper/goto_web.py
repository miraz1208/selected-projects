"""Separate class to access the web"""

import requests
from fake_useragent import UserAgent


class GotoWeb:
    """Gets access to web"""

    def __init__(self) -> None:
        pass

    def web(self, url):
        """Access web"""
        user_agent = UserAgent()
        ua_random = user_agent.random

        head = {
            "User-Agent": ua_random,
            "Accept-Language": "en-US, en;q=0.5",
        }

        try:
            session = requests.Session()
            session.trust_env = False
            page = session.get(
                url,
                headers=head,
                timeout=60,
                allow_redirects=False)

            page.raise_for_status()

            page_content = page.content

            return page_content
        except requests.exceptions.RequestException as error:
            print(f'Error: {error}')
            return None
