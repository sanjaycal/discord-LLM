import requests
from bs4 import BeautifulSoup


def get_text(url):
    try:
        r = requests.get(url)
    except:
        return "Invalid URL"
    if r.status_code!=200:
        return f"status code:{r.status_code}"

    soup = BeautifulSoup(r.text, features="html.parser")

    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()    # rip it out

    # get text
    text = soup.get_text()

    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)

    return text