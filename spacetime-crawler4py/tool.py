import urllib.request
from urllib.parse import urlparse

from bs4 import BeautifulSoup
from bs4 import Comment


LONGEST_PAGE_LENGTH = 0
LONGEST_PAGE_URL = ""
Words_Frequency = dict()


def save_url_content_local(url, filename):
    # Accept a String(url) and and store HTML contents into 'html'
    html = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(html, 'html.parser')
    text_list = []
    for text in soup.findAll(text=True):
        # First, we need to move the comments in the html file
        if isinstance(text, Comment):
            continue

        # We need to remove HTML markup
        text_without_markup = text.get_text(strip=True)
        text_list.append(text_without_markup)

    data = ' '.join(text_list)

    with open(filename, mode='w', encoding='utf-8') as f:
        f.write(data)


def tokenize(filepath_local):
    try:
        file = open(filepath_local, 'r', encoding='UTF-8')
        line = file.read()
        text = ''
        for content in line:
            if (content.isascii()) and (content.isalpha()):
                text += content.lower()
            else:
                text += " "
        tokens_temp = text.split()
        tokens = list()
        for token in tokens_temp:
            if len(token) != 1:
                tokens.append(token)

        return tokens

    except FileNotFoundError:
        raise FileNotFoundError('I can\'t find the file')


def determine_longest_page(current_url, words_list):
    global LONGEST_PAGE_URL
    global LONGEST_PAGE_LENGTH
    current_page_length = len(words_list)
    if current_page_length > LONGEST_PAGE_LENGTH:
        LONGEST_PAGE_LENGTH = current_page_length
        LONGEST_PAGE_URL = current_url
    print('So far, the longest page length is:', LONGEST_PAGE_LENGTH, '. And the url is:', LONGEST_PAGE_URL)


def delete_stopwords(tokens):
    with open("stop_words.txt", "r", encoding="UTF-8") as stopwords_file:
        stopwords = stopwords_file.read().split()

    tokens_without_stopwords = [token for token in tokens if token not in stopwords]
    return tokens_without_stopwords


def frequency_and_print(tokens_without_stopwords):
    global Words_Frequency
    for j in tokens_without_stopwords:
        if j not in Words_Frequency:
            Words_Frequency[j] = 1
        else:
            Words_Frequency[j] += 1

    frequency_sorted = dict(sorted(Words_Frequency.items(), key=lambda x: (-x[1], x[0])))
    print(list(frequency_sorted.items())[:50])


def subdomains_tracker(source_url):
    url = urlparse(source_url)
    result = ''
    count = 0
    for char in url.netloc:
        if result == "www.":
            result = ''

        if url.netloc[count:] == 'ics.uci.edu':
            if result != '':
                result += 'ics.uci.edu'
            break
        elif url.netloc[count:] == 'cs.uci.edu':
            if result != '':
                result += 'cs.uci.edu'
            break
        elif url.netloc[count:] == 'informatics.uci.edu':
            if result != '':
                result += 'informatics.uci.edu'
            break
        elif url.netloc[count:] == 'stat.uci.edu':
            if result != '':
                result += 'stat.uci.edu'
            break

        result += char
        count += 1
    return result
