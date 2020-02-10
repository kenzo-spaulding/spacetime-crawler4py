import lxml.html as html
import re
from urllib.parse import urlparse, urldefrag
import urllib


def scraper(url: str, resp) -> list:
    temp_links = extract_next_links(url, resp)
    links = []
    for link in temp_links:
        a = urldefrag(link[2])[0]
        links.append(a)
    print(links)
    return [link for link in links if is_valid(link)]


def extract_next_links(url: str, resp) -> list:
    return [link for link in html.iterlinks(resp.raw_response.content)]


def is_valid(url):
    try:
        def check_url(url2):
            url2 = url2
            valids = {".ics.uci.edu", ".cs.uci.edu", ".informatics.uci.edu", ".stat.uci.edu",
                      "today.uci.edu/department/information_computer_sciences"}
            for entry in valids:
                if entry in url2:
                    return True
            return False

        parsed = urlparse(url)
        if parsed.scheme not in set(["http", "https"]) or not check_url(url):
            return False
        return not re.match(
            r".*\.(css|js|bmp|gif|jpe?g|ico"
            + r"|png|tiff?|mid|mp2|mp3|mp4"
            + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
            + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
            + r"|epub|dll|cnf|tgz|sha1"
            + r"|thmx|mso|arff|rtf|jar|csv"
            + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower())

    except TypeError:
        print("TypeError for ", parsed)
        raise
