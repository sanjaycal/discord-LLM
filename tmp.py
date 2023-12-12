from googleapiclient.discovery import build

my_api_key = "AIzaSyBQrGvmPr_ggQz5DhD_cxJc7Xjn5i074g0"
my_cse_id = "86bee08725af54459"

def google_search(search_term, api_key, cse_id, **kwargs):
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=search_term, cx=cse_id, **kwargs).execute()
    return res['items']

results = google_search(
    'stackoverflow site:en.wikipedia.org', my_api_key, my_cse_id, num=10)
for result in results:
    print(result)