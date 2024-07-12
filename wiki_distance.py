from pathlib import Path
import requests
from bs4 import BeautifulSoup

# Directory to save your .json files to
# NB: create this directory if it doesn't exist
SAVED_JSON_DIR = Path(__file__).parent / 'visited_paths'


def distance(source_url: str, target_url: str) -> int | None:
    """Amount of wiki articles which should be visited to reach the target one
    starting from the source url. Assuming that the next article is choosing
    always as the very first link from the first article paragraph (tag <p>).
    If the article does not have any paragraph tags or any links in the first
    paragraph then the target is considered unreachable and None is returned.
    If the next link is pointing to the already visited article, it should be
    discarded in favor of the second link from this paragraph. And so on
    until the first not visited link will be found or no links left in paragraph.
    NB. The distance between neighbour articles (one is pointing out to the other)
    assumed to be equal to 1.
    :param source_url: the url of source article from wiki
    :param target_url: the url of target article from wiki
    :return: the distance calculated as described above
    """
    print(target_url)
    my_links = set()
    count = 0
    while source_url != target_url:
        html = requests.get(source_url).text
        for paragraph in BeautifulSoup(html).findAll('p'):
            is_paragraph = 0
            for i in paragraph.parents:
                if i.attrs.get('class') is None:
                    is_paragraph += 1

            if is_paragraph == 1:
                found = False
                for link in paragraph.findAll('a'):
                    if (link.get('href') is None) or (link.get('href')[0:5] != '/wiki') or (
                            link.get('href')[-4:] == '.ogg'):
                        continue
                    lin = 'https://ru.wikipedia.org' + link.get('href')
                    if lin in my_links:
                        continue
                    my_links.add(lin)
                    source_url = lin
                    count += 1
                    found = True
                    break
                if not found:
                    return None
                break
    return count
