import requests
import json
import string

from bs4 import BeautifulSoup


def request_quote():
    r = requests.get(input("Input the URL:\n"))
    try:
        soup = BeautifulSoup(r.content, "lxml")
        title = soup.find("h1").get_text(strip=True).partition("(")[0]
        para = soup.find("div", "summary_text").get_text(strip=True)
        print(json.dumps({"title": title, "description": para}))
    except (KeyError, AttributeError):
        print("Invalid movie page!")


def save_page_source():
    url = input("Input the URL:\n")
    r = requests.get(url)
    try:
        if not r:
            print(f"The URL returned {r.status_code}!")
            exit(0)
        with open('source.html', 'wb') as file:
            file.write(r.content)
    except:
        pass
    else:
        print("Content saved.")


def nature_scraper():
    url = "https://www.nature.com/nature/articles"
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "lxml")

    for article in soup("article"):
        title = article.div.h3.a.get_text(strip=True)
        url = article.div.h3.a["href"]
        category = article.div.p.span.get_text(strip=True)

        if category != "News":
            continue
        else:
            article_scraper(url, title)


def article_scraper(url, title):
    translator = str.maketrans(" ", "_", string.punctuation)
    # hardcoded url for this project
    url = f"https://www.nature.com{url}"
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "lxml")
    body = soup.find("div", "article__body").text.strip()

    with open(f"{title.translate(translator)}.txt", 'wb') as file:
        file.write(body.encode("UTF-8"))


nature_scraper()
