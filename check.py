import re

from bs4 import BeautifulSoup
import requests


def check():
    with open("links", "r") as f:
        links = [l.strip() for l in f.readlines() if l.strip()]

    for link in links:
        status_code, content = fetch(link)

        with open(f"data/{link.split('/')[-1]}", "w+") as f:
            f.write(
                content
                if status_code is None
                else f"{status_code}:{normalise(content)}"
            )


def fetch(link):
    try:
        r = requests.get(
            link,
            timeout=5,
            headers={
                "User-Agent": "GitHub Action @ github.com/bayotop/za-mamou-data (https://zamamou.sk)"
            },
        )

        return r.status_code, r.content.decode("utf-8", errors="ignore")
    except Exception as e:
        return None, e


def normalise(content):
    html = BeautifulSoup(content, features="html.parser").prettify()
    html = re.sub(r'Liferay\.authToken="[^"]+";', "", html)
    html = re.sub(r"t=[0-9]{13}", "", html)

    return html


if __name__ == "__main__":
    check()
