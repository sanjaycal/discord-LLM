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

from googleapiclient.discovery import build

api_key = open("googleSearchAPIKey","r").read()
cse_id = open("googleSearchCSEID","r").read()

def google_search(search_term, **kwargs):
    global api_key
    global cse_id
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
    out = []
    gs = res['items']
    for i in gs:
        #out.append({"link":i["link"],"snippet":i["snippet"]})
        out.append({"link":i["link"]})
    return out
