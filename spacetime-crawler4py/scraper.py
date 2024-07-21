import re
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from tool import save_url_content_local
from tool import tokenize
from tool import delete_stopwords
from tool import frequency_and_print
from tool import determine_longest_page

visited_url = dict()



def scraper(url, resp):
    global visited_url
    links = extract_next_links(url, resp)
    res = [link for link in links if is_valid(link)]

    for i in set(res):
        parsed = urlparse(i)
        if (parsed.path == '' or parsed.path == '//'):
            if (parsed._replace(scheme="http").geturl() + '/' in visited_url):
                continue
        if (parsed._replace(scheme="http").geturl() in visited_url):
            continue

        with open("crawled_urls.txt2", "a", encoding="utf-8") as file:
            file.write(parsed._replace(scheme="http").geturl() + "\n")

        # delete like 'http://www.ics.uci.edu//'
        if (parsed.path == '' or parsed.path == '//'):
            visited_url[parsed._replace(scheme="http", path='/').geturl()] = False
        else:
            visited_url[parsed._replace(scheme="http").geturl()] = False

    return res


def extract_next_links(url, resp):
    # Implementation required.
    # url: the URL that was used to get the page
    # resp.url: the actual url of the page
    # resp.status: the status code returned by the server. 200 is OK, you got the page. Other numbers mean that there was some kind of problem.
    # resp.error: when status is not 200, you can check the error here, if needed.
    # resp.raw_response: this is where the page actually is. More specifically, the raw_response has two parts:
    #         resp.raw_response.url: the url, again
    #         resp.raw_response.content: the content of the page!
    # Return a list with the hyperlinks (as strings) scrapped from resp.raw_response.content
    if resp.status != 200:
        print(resp.status, resp.error)
        return []

    try:
        parsed = urlparse(url)
        links_output = []
        if (re.search("(.)*java|txt|pdf|ppsx", parsed.path.lower()) == None):
            # store current page's contents in a local text file, here we name it as 'url_contents_store.txt'
            save_url_content_local(url, 'url_contents_store.txt')

            # open the local txt file and only save valid English words in a list, omit the words like 's' and 're'
            words_list = tokenize('url_contents_store.txt')

            # We determine the longest page by recording the number of the valid English words they have
            # Then, we print the words numbers and also the url of this longest page
            determine_longest_page(url, words_list)

            # In order to get the 50 common words, we need to remove stopwords firstly
            tokens_without_stopwords = delete_stopwords(words_list)

            # Finally, we record the frequency of each valid English word and also print them in terminal
            frequency_and_print(tokens_without_stopwords)

        soup = BeautifulSoup(resp.raw_response.content, 'html.parser')
        # Find all links on this current page
        href_list = [a['href'] for a in soup.find_all('a', href=True)]
        for href in href_list:
            links_output.append(href)
    except:
        return list()

    return list(set(links_output))


def is_valid(url):
    # Decide whether to crawl this url or not. 
    # If you decide to crawl it, return True; otherwise return False.
    # There are already some conditions that return False.
    try:
        parsed = urlparse(url)
        if parsed.scheme not in set(["http", "https"]):
            return False

        if len(parsed.fragment) != 0:
            return False

        if (re.match(r".*\.(ics|cs|informatics|stat)\.uci\.edu", parsed.netloc.lower()) == None and
                re.match(r"(http|https)://today\.uci\.edu/department/information_computer_sciences/.*", url) == None):
            return False

        if parsed.query != '':
            return False

        if re.search("calendar|event", parsed.path.lower()):
            if (re.search("year|month|day|week|category", parsed.path.lower())):
                return False
            if (re.search('\d{4}-\d{2}-\d{2}|\d{4}-\d{2}', parsed.path.lower())):
                return False

        if (re.search("download", parsed.path.lower())):
            return False

        if (re.search("(.)*java|txt|pdf|ppsx", parsed.path.lower())):
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
