## In case If you have an error mentioning spacy.strings.StringStore size changed, may indicate binary incompatibility
## pip uninstall neuralcoref
## pip uninstall spacy
## pip install spacy==2.1.6
## pip install --upgrade setuptools
## pip install cython==0.29.14
## pip install https://github.com/huggingface/neuralcoref/archive/master.zip
## python -m spacy download en

## Ehkä merkitystä numpy==1.17.2


import spacy
import neuralcoref

def parse_body_text_from_url(link):
    """
    Fetches the HTML version of a BBC page and parses it to text.
    """

    html = _get_html_file(link)
    text = _html_to_text(html)
    text = _parse_body_text_from_text_version(text)
    return text

link = "https://www.bbc.com/news/world-europe-50740324"

nlp = spacy.load('en_core_web_sm')
neuralcoref.add_to_pipe(nlp)
doc1 = nlp('My sister has a dog. She loves him.')
print(doc1._.coref_clusters)

doc2 = nlp('Angela lives in Boston. She is quite happy in that city.')
for ent in doc2.ents:
    print(ent._.coref_cluster)










##link = "https://www.bbc.com/news/world-europe-50740324"