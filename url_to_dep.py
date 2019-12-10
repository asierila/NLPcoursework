### URLISTA artikkelin n:nnen lauseen dep ja ent esitys


from bs4 import BeautifulSoup
import requests
import re
import spacy

import nltk
from stat_parser import Parser

from spacy import displacy
from collections import Counter
import en_core_web_sm
nlp = spacy.load("en_core_web_sm")


def url_to_string(url):
    res = requests.get(url)
    html = res.text
    soup = BeautifulSoup(html, 'html.parser')
    for script in soup(["script", "style", 'aside']):
        script.extract()
    return " ".join(re.split(r'[\n\t]+', soup.get_text()))
    
    
ny_bb = url_to_string('https://www.nytimes.com/2018/08/13/us/politics/peter-strzok-fired-fbi.html?hp&action=click&pgtype=Homepage&clickSource=story-heading&module=first-column-region&region=top-news&WT.nav=top-news')
article = nlp(ny_bb)
len(article.ents)

##labels = [x.label_ for x in article.ents]
##Counter(labels)

##items = [x.text for x in article.ents]
##Counter(items).most_common(3)

sentences = [x for x in article.sents]
print(sentences[20])




##displacy.serve(nlp(str(sentences[20])), style='dep', options = {'distance': 120})
displacy.serve(nlp(str(sentences[20])), style='ent', options = {'distance': 120})