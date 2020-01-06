from bs4 import BeautifulSoup
import requests
import re
import spacy
import html2text
nlp = spacy.load("en_core_web_sm")


def _get_html_file(url):
    """
    Gets a HTML version of the web page given in the 'url' argument.
    Returns HTML version as a string.
    """
    if not url.startswith("http"):
        url = "https://" + url
    res = requests.get(url)
    html_page = res.text
    # print(html_page)
    # print(html_page)
    return html_page


def _html_to_text(html):
    """
    Parses HTML page to text. Returns a string.
    """

    # soup = BeautifulSoup(html, features="html.parser")
    # # text = soup.find_all(text=True)
    # blacklist = [
    #     # "script",
    #     # "style",
    #     # "aside",
    #     # "head",


    #     '[document]',
    #     'noscript',
    #     'header',
    #     # 'html',
    #     'meta',
    #     'head',
    #     'input',
    #     'script',
    # ]
    # for script in soup(blacklist):
    #     script.extract()
    # # print(soup)
    # text = soup.get_text()

    # text = ' '.join(text.split())
    # text = text.replace("\t", " ")
    # text = " ".join(re.split(r'[\n\t]+', text))
    # article = nlp(text)

    # ##labels = [x.label_ for x in article.ents]
    # ##Counter(labels)

    # ##items = [x.text for x in article.ents]
    # ##Counter(items).most_common(3)

    # sentences = [x.text for x in article.sents]
    # output = "".join(str(sentences))
    # return output

    # TODO: parse
    # <span class="off-screen">Media caption</span> out of tree
    h = html2text.HTML2Text()
    h.ignore_links = True
    h.ignore_images = True
    h.ignore_videos = True
    return h.handle(html)


def _parse_body_text_from_text_version(text):
    """
    Takes the full text and removes clutter. Returns parsed text
    """

    text_as_list = text.split("\n")
    for idx, row in enumerate(text_as_list):
        if "## related topics" in row.lower():
            text_as_list = text_as_list[:idx]
            break
        if "article share tools" in row.lower():
            text_as_list = text_as_list[:idx]
            break
        # blacklist = [
        #     "    * ",
        #     "    * ",
        # ]

    # Add dots in bullet point case for previous sentences
    for idx,char in enumerate(text):
        if char == "*":
            if text[idx-3] == "\n":
                # if text[idx-4] not in "?!.:;":
                text = text[:idx-3] + "." + text[idx-4:] 

    for idx, row in enumerate(text_as_list):
        if row.startswith(("    * ",
                           "Share this with",
                           "  * Share this with")
        ):
            text_as_list.pop(idx)
 
    for idx, row in enumerate(text_as_list):
        if row == text_as_list[idx-2] and row != " " and row != "":
            # print(row)
            text_as_list = text_as_list[idx:]
            break

    for idx, row in enumerate(text_as_list):
        if "Close share panel" in row:
            text_as_list = text_as_list[idx+3:]
            break


    text = "\n".join(text_as_list)
    
    # remove extra hashtags
    while "##" in text:
        text = text.replace("##", "#")
    
    # convert symbol to text. possible double space fixed later
    text = text.replace("%", " percent ")
    
    # remove multiple newlines to normal dot
    while "\n\n" in text:
        text = text.replace("\n\n", ". ")

    # remove multiple dots resulting from previous operation
    while ".." in text:
        text = text.replace("..", ".")
    
    # replace newlines with spaces
    while "\n" in text:
        text = text.replace("\n", " ")

    # remove multiple space
    while "  " in text:
        text = text.replace("  ", " ")


    # replace prefix with more machine-readable form
    text = text.replace("pro-", "pro ")
    text = text.replace("anti-", "anti ")
    
    text = text.replace("one-", "one ")
    text = text.replace("two-", "two ")
    text = text.replace("three-", "three ")
    text = text.replace("four-", "four ")
    text = text.replace("five-", "five ")
    text = text.replace("six-", "six ")
    text = text.replace("seven-", "seven ")
    text = text.replace("eight-", "eight ")
    text = text.replace("nine-", "nine ")
    text = text.replace("ten-", "ten ")

    numbers = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    for number in numbers:
        if number+"km" in text:
            text = text.replace(number+"km", number+" km")

    text = text.replace("#", "")
    text = text.replace("*", "")

    #get rid of "Media playback is unsupported on your device."
    while "Media playback is unsupported on your device." in text:
        text = text.replace(
            " Media playback is unsupported on your device.", ""
        )
    
    # get rid of "Media Caption" glued to other words
    word = "Media caption"
    idx = text.find(word)
    end_index = idx + len(word)
    if text[end_index] != " ":
        text = text[:idx] + text[end_index:]


    # remove multiple space
    while "  " in text:
        text = text.replace("  ", " ")
    
    while ". ." in text:
        text = text.replace(". .", ".")

    return text
    # print(text_as_list)


def parse_body_text_from_url(link):
    """
    Fetches the HTML version of a BBC page and parses it to text.
    """

    html = _get_html_file(link)
    text = _html_to_text(html)
    text = _parse_body_text_from_text_version(text)
    return text


def _debugfunc():
    """
    Contains links for BBC articles and printing. Not to use in
    production.
    """

    # link = "https://www.bbc.com/news/world-asia-50723352"
    # link = "https://www.bbc.com/news/live/election-2019-50739883"
    # link = "https://www.bbc.com/news/world-us-canada-50747374"
    # link = "https://www.bbc.com/news/world-asia-50741094"
    link = "https://www.bbc.com/news/world-europe-50740324"
    # link = "https://www.iltalehti.fi/viihdeuutiset/a/045cb810-1ffd-4641-84d7-4995953a9a4d"
    # text = parse_body_text_from_url(link)
    # teksti = _html_to_text(link)
    html = _get_html_file(link)
    text = _html_to_text(html)
    text = _parse_body_text_from_text_version(text)
    print(text)
    #print(text)



_debugfunc()


