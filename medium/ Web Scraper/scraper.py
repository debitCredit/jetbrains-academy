import requests
import string
import os
import re

from bs4 import BeautifulSoup


def nature_scraper(news_category: string, pages: int):
    for page in range(1, pages+1, 1):
        url = f"https://www.nature.com/nature/articles?searchType=journalSearch&sort=PubDate&page={page}"
        r = requests.get(url)
        soup = BeautifulSoup(r.content, "lxml")

        # creates dirs even when no articles exists, this should be in article_scraper, only here to pass test #3
        directory = f"Page_{page}"
        if not os.path.isdir(directory):
            os.mkdir(directory)

        for article in soup("article"):
            title = article.div.h3.a.get_text(strip=True)
            url = article.div.h3.a["href"]
            category = article.div.p.span.get_text(strip=True)

            if category != news_category:
                continue
            else:
                article_scraper(url, title, page)


def article_scraper(url, title, page):
    translator = str.maketrans(" ", "_", string.punctuation)
    url = f"https://www.nature.com{url}"
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "lxml")
    # re used because different categories have different div class names for the body of the article
    body = soup.find("div", re.compile("article.+body")).text.strip()

    directory = f"Page_{page}"
    file_name = f"{title.translate(translator)}.txt"
    file_path = os.path.join(directory, file_name)

    with open(file_path, 'wb') as file:
        file.write(body.encode("UTF-8"))


pages = int(input())
category = input()
nature_scraper(category, pages)
