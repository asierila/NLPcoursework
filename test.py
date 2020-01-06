"""the purpose of this file is to parse given webpage from url, or any
given plaintext in the following way

example sentence:

  +------------[type here]-----------+
  |                                  |
  v                                  |
Olli is sleeping during the lecture. He is very tired

the relations that will be parsed are;
   +------------+--[type here]-----------+
   |            |                        |
   v            v                        |
proper noun, named entity ... ... ...pronoun

"""

try:
    from seapie import Seapie as seapie # DEBUG
except:
    print("do pip3 install seapie. importerror happened")

import nltk
import spacy
import webbrowser
from spacy import displacy
from pronouns import pronouns
from stat_parser import Parser
from parse_url_to_text import parse_body_text_from_url
from text_files import long_text, short_text, pronoun_text
import en_core_web_sm; nlp = en_core_web_sm.load() # second part is deemed import-like
from name2gender import names

# installation notes for libraries
#
# clone and install pystatparser locally:
# python setup.py install --user
# https://github.com/emilmont/pyStatParser
# or use the following
# pip3 install https://github.com/emilmont/pyStatParser/archive/master.zip
#
# import spacy  # use following for library: python -m spacy download en




class TextContainer:
    """container class for holding a single web page's or such documents
    whole text in its classified form for further processing
    """

    class SentenceContainer:
        """container class for holding a single sentences's text in its
        classified form for further processing
        """

        def __init__(self, sentence):
            self.txt = sentence
            self.doc = nlp(sentence) # the nlp base doc
            self.nes = [(X.text, X.label_) for X in self.doc.ents] # named entities
            self.pos = [token for token in nltk.pos_tag(nltk.word_tokenize(sentence))]

            self.ne_indexes = []
            self.noun_indexes = []
            self.pronoun_indexes = []
            self.propernoun_indexes = []


            def _str_find_fix(pos, index, sentence):
                """acts like str.find but doesn't match words that are contained in word. returns index
                returns next index if first fails due to being part of a another word"""

                abc = "abcedfghijlkmnopqrstuvwxyzåäö"

                while True:
                    index = sentence.find(pos, index)
                    if index == -1:
                        return index
                    if (index != 0) and (index != len(sentence)-1): #not first letter or last letter
                        if sentence[index-1] in abc:
                            index += 1
                            continue
                        if sentence[index+len(pos)] in abc:
                            index += 1
                            continue
                        else:
                            return index
                    else:
                        return index

            ## THIS BLOCK WILL CREATE NAMED ENTITY INDEXES
            for ne, ne_type in self.nes:
                index = sentence.find(ne) # find first index of occurence. will be -1 if nonexistent
                while index != -1:   # while occurence exists
                    index = sentence.find(ne, index) # find new index for it
                    if index != -1: # if result is that something exists
                        if not (index, index+len(ne)) in self.ne_indexes: # and is not already listed
                            self.ne_indexes.append((index, index+len(ne))) # add it to the list
                        index += 1 # and increase count by 1 to find next one
            # this will result in the following error:
            # "Europe" is matched from "European comission" if both "Europe" and "European comission" are in the sentence
            # resulting in two matches of "Europe"
            # the following clears it
            duplicates = []
            for start, end in self.ne_indexes:
                for start2, end2 in self.ne_indexes:
                    if start2 >= start and end2 <= end:
                        if not (start == start2 and end == end2):
                            duplicates.append((start2, end2))
            for i in duplicates:
                self.ne_indexes.remove(i)

            ## THIS BLOCK WILL CREATE PRONOUN INDEXES. ITS ALMOST COPYPASTE OF BELOW BLOCK
            for pos, pos_type in self.pos:
                if pos_type in ["PRP", "PRP$", "WP$", "WP"]:
                    index = sentence.find(pos) # find first index of occurence. will be -1 if nonexistent
                    while index != -1:   # while occurence exists
                        # index = sentence.find(pos, index) # find new index for it # DEBUG # TODO # THIS IS THE ORIGINAL LINE
                        index = _str_find_fix(pos, index, sentence)
                        if index != -1: # if result is that something exists
                            if not (index, index+len(pos)) in self.pronoun_indexes: # and is not already listed
                                self.pronoun_indexes.append((index, index+len(pos))) # add it to the list
                            index += 1 # and increase count by 1 to find next one
                # this will result in the following error:
                # "Europe" is matched from "European comission" if both "Europe" and "European comission" are in the sentence
                # resulting in two matches of "Europe"
                # the following clears it
                duplicates = []
                for start, end in self.pronoun_indexes:
                    for start2, end2 in self.pronoun_indexes:
                        if start2 >= start and end2 <= end:
                            if not (start == start2 and end == end2):
                                duplicates.append((start2, end2))
                for i in duplicates:
                    self.pronoun_indexes.remove(i)


            ## THIS BLOCK WILL CREATE PROPER NOUN INDEXES. ITS ALMOST COPYPASTE OF BELOW BLOCK
            for pos, pos_type in self.pos:
                if pos_type in ["NNP", "NNPS"]:
                    index = sentence.find(pos) # find first index of occurence. will be -1 if nonexistent
                    while index != -1:   # while occurence exists
                        # index = sentence.find(pos, index) # find new index for it # DEBUG # TODO # THIS IS THE ORIGINAL LINE
                        index = _str_find_fix(pos, index, sentence)
                        if index != -1: # if result is that something exists
                            if not (index, index+len(pos)) in self.propernoun_indexes: # and is not already listed
                                self.propernoun_indexes.append((index, index+len(pos))) # add it to the list
                            index += 1 # and increase count by 1 to find next one
                # this will result in the following error:
                # "Europe" is matched from "European comission" if both "Europe" and "European comission" are in the sentence
                # resulting in two matches of "Europe"
                # the following clears it
                duplicates = []
                for start, end in self.propernoun_indexes:
                    for start2, end2 in self.propernoun_indexes:
                        if start2 >= start and end2 <= end:
                            if not (start == start2 and end == end2):
                                duplicates.append((start2, end2))
                for i in duplicates:
                    self.propernoun_indexes.remove(i)

            ## THIS BLOCK WILL CREATE NOUN INDEXES. ITS ALMOST COPYPASTE OF ABOVE BLOCK
            for pos, pos_type in self.pos:
                if pos_type in ["NNS", "NN"]:
                    index = sentence.find(pos) # find first index of occurence. will be -1 if nonexistent
                    while index != -1:   # while occurence exists
                        index = sentence.find(pos, index) # find new index for it
                        if index != -1: # if result is that something exists
                            if not (index, index+len(pos)) in self.noun_indexes: # and is not already listed
                                self.noun_indexes.append((index, index+len(pos))) # add it to the list
                            index += 1 # and increase count by 1 to find next one
                # this will result in the following error:
                # "Europe" is matched from "European comission" if both "Europe" and "European comission" are in the sentence
                # resulting in two matches of "Europe"
                # the following clears it
                duplicates = []
                for start, end in self.noun_indexes:
                    for start2, end2 in self.noun_indexes:
                        if start2 >= start and end2 <= end:
                            if not (start == start2 and end == end2):
                                duplicates.append((start2, end2))
                for i in duplicates:
                    self.noun_indexes.remove(i)

        def pprint(self):
            """this will prettyprint give self with its known index information"""

            # upack information for easier looping
            ne_starts = [start for start, stop in self.ne_indexes]
            ne_stops = [stop for start, stop in self.ne_indexes]
            noun_starts = [start for start, stop in self.noun_indexes]
            noun_stops = [stop for start, stop in self.noun_indexes]
            pronoun_starts = [start for start, stop in self.pronoun_indexes]
            pronoun_stops = [stop for start, stop in self.pronoun_indexes]
            propernoun_starts = [start for start, stop in self.propernoun_indexes]
            propernoun_stops = [stop for start, stop in self.propernoun_indexes]

            # self.ne_indexes          ◄─────────┐
            # self.noun_indexes        ◄─────────┤
            # self.pronoun_indexes  ►────────────┤  from pronoun to anything else
            # self.propernoun_indexes  ◄─────────┘

            accumulator = []
            for index, letter in enumerate(self.txt):
                if (index in pronoun_starts) or (index in pronoun_stops):
                    accumulator.append("▲") # this block finds and marks pronouns with up triangle
                if index in ne_starts+ne_stops+propernoun_starts+propernoun_stops+noun_starts+noun_stops:
                    accumulator.append("▼") # this block finds and marks the rest with down triangle
                accumulator.append(letter)

            for index, chr in enumerate('"' + "".join(accumulator) + '"'):
                    print(chr, end="")
                    if index % 79 == 0 and index != 0:
                        print()
            print()


        def tmp_output(self):
            """this will prettyprint give self with its known index information"""

            # upack information for easier looping
            ne_starts = [start for start, stop in self.ne_indexes]
            ne_stops = [stop for start, stop in self.ne_indexes]
            noun_starts = [start for start, stop in self.noun_indexes]
            noun_stops = [stop for start, stop in self.noun_indexes]
            pronoun_starts = [start for start, stop in self.pronoun_indexes]
            pronoun_stops = [stop for start, stop in self.pronoun_indexes]
            propernoun_starts = [start for start, stop in self.propernoun_indexes]
            propernoun_stops = [stop for start, stop in self.propernoun_indexes]

            # self.ne_indexes          ◄─────────┐
            # self.noun_indexes        ◄─────────┤
            # self.pronoun_indexes  ►────────────┤  from pronoun to anything else
            # self.propernoun_indexes  ◄─────────┘

            accumulator = []
            str = ""
            for index, letter in enumerate(self.txt):
                if (index in pronoun_starts) or (index in pronoun_stops):
                    accumulator.append("▲") # this block finds and marks pronouns with up triangle
                if index in ne_starts+ne_stops+propernoun_starts+propernoun_stops+noun_starts+noun_stops:
                    accumulator.append("▼") # this block finds and marks the rest with down triangle
                accumulator.append(letter)

            for index, chr in enumerate('"' + "".join(accumulator) + '"'):
                    str += chr
                    if index % 79 == 0 and index != 0:
                        str += "\n"
            return str


    def __init__(self, plaintext):
        # self.plain_sentences = [token for token in nltk.tokenize.sent_tokenize(plaintext)]
        # self.sentences = {index: TextContainer.SentenceContainer(sentence) for (index, sentence) in enumerate(self.plain_sentences)}
        self.sentences = [TextContainer.SentenceContainer(sentence) for sentence in nltk.tokenize.sent_tokenize(plaintext)]

        self.connections = []
        # from TextContainer index, from SentenceContainer index
        # to TextContainer index, to SentenceContainer index
        #
        # from sentence and letter index to
        # to sentence and letter index
        # example: the word "He" should point to "Jouni" in the below sentence:
        # "Jouni has a headache. He thusly ingested 50mg theanine and 200mg caffeine"
        # this is saved as [ ... , ((1, 0), (0, 0)) , ...] which stands for
        # pointing from first word of second sentence to first word of first sentence.

    @staticmethod
    def _get_pronoun_type(word):
        """returns gender and multiplicity of a word.
        words are categorized into four categories represented with numbers 1,2,3,4

        due to the rules written in parenthesis four values are enough.
        it should be noted that 4 can match also 1,2,3.

        1: singular (always genderless) e.g "i"
        2: male (always singular) e.g. "he"
        3: female (always singular) e.g. "she"
        4: plural (always genderless) e.g. "they"

        I, you, he, she, it, they
        me, you, him, her, it
        my, mine, your, yours, his, her, hers, its
        myself, yourself, himself, herself, itself
        who, whom, whose, what, which
        another, each, everything, nobody, either, someone
        this, that
        """

        # this word map should cover all the cases as its only supposed to include pronuns
        word_map = {"i":          1, "you":        1, "he":         2,
                    "she":        3, "it":         1, "they":       4,
                    "me":         1, "him":        2, "her":        3,
                    "my":         1, "mine":       1, "your":       1,
                    "yours":      1, "his":        2, "hers":       3,
                    "its":        1, "myself":     1, "yourself":   1,
                    "himself":    2, "herself":    3, "itself":     1,
                    "who":        1, "whom":       1, "whose":      1,
                    "what":       1, "which":      1, "another":    1,
                    "each":       1, "everything": 4, "nobody":     1,
                    "either":     4, "someone":    1, "this":       1,
                    "that":       1, "we":         4, "themselves": 4,
                    "our":        4, "their":      4, "theirs":     4,
                    "them":       4}
        word = word.lower()
        try:
            wordtype = word_map[word]
        except KeyError:
            raise NotImplementedError("'" + word + "'" + " is not mapped to any value")
        else:
            return wordtype


    def parse_corefs(self):
        """argument indexes are for the word that you want to resolve the coref for
        returns goal sentence index and goal word index
        """
        
        # these indexes can be assumed to be correct and they can be
        # assumed to correctly contain multiple words separated by spaces
        # so they are used as is and then tagged as needed
        # self.ne_indexes = []
        # self.noun_indexes = []
        # self.pronoun_indexes = []
        # self.propernoun_indexes = []
        
        
        for i in reversed(range(len(self.sentences))): # reversed pointer over sentences
            sentence = self.sentences[i]
            txt = sentence.txt
            
            
            for p_start, p_end in sentence.pronoun_indexes:
                pronoun = txt[p_start:p_end]
            
                pronoun_type = TextContainer._get_pronoun_type(pronoun)
                #seapie()
                # DEBUG ERROR RAISE
                if pronoun_type in (2,3):
                
                    for idx, (ne, ne_type) in enumerate(sentence.nes):
                        if ne_type == "PERSON":
                            print("pronoun_type", pronoun_type)
                            print("names[ne.lower()]+1", names[ne.lower()]+1)
                            if pronoun_type == names[ne.lower()]+1: # magix fix. mies on databasessa 1 kun pitäis olla 2 jotta pronomini lista toimii
                                ne_start, ne_stop = sentence.ne_indexes[idx]
                                # if p_start > ne_start:
                                print("MATCH!!!!")
                                seapie()
                            
                            
                else:
                    print("pronoun types for other than male/female not implemented")
                    # raise NotImplementedError("pronoun types for other than male/female not implemented")
               
            
            #print(self.sentences[i].txt)

        



def get_goal_type(word):
    pass








if __name__ == "__main__":
    # source = pronoun_text
    # link = "https://www.bbc.com/news/world-asia-50723352"
    # link = "https://www.bbc.com/news/world-us-canada-50747374"
    # link = "https://www.bbc.com/news/world-asia-50741094"
    link = "https://www.bbc.com/news/world-europe-50740324"
    # link = "https://www.bbc.com/news/live/election-2019-50739883" # erittäin vaikea

    source = parse_body_text_from_url(link)
    
    # DEBUG
    source = "Markus is so fucking tired his eyes are going to fall of his head"
    
    wholetext = TextContainer(source)

    for index, sentence in enumerate(wholetext.sentences):
        if len(sentence.nes) != len(sentence.ne_indexes): # sanity check
            print("index mismatch in sentence", index)
            exit()
        print("─"*80)
        print("SENTENCE INDEX:", index)
        sentence.pprint()


    wholetext.parse_corefs()


    seapie()


    # for index, sentence in enumerate(sentences):

        # print("======")
        # print(named_entities)

        # seapie()

        # =========== OLD MAIN BLOCK BEGIN. DO NOT REMOVE ===========
        # =========== OLD MAIN BLOCK BEGIN. DO NOT REMOVE ===========
        # =========== OLD MAIN BLOCK BEGIN. DO NOT REMOVE ===========
        # print("=====", "parsing sentence", index+1, "of", len(sentences), "=====")

        # tagged = [tokenized for tokenized in nltk.pos_tag(nltk.word_tokenize(sentence))]
        # tree = Parser().parse(sentence)
        # doc = nlp(sentence)
        # named_entities = [(X.text, X.label_) for X in doc.ents]

        # show tree structure in tkinter window for the sentence
        # tree.draw()

        # print tagged text in flat format
        # for word, tag in tagged: print(word, "(" + tag + ") ", end="")

        # print tagged text in tree format (different tags than above!)
        # print(tree)

        # dump named entities from the sentence
        # print(named_entities)

        # visualize connections between words in the sentence in browser
        # browser = "C:/Program Files/Mozilla Firefox/firefox.exe %s"
        # print("ctrl+c to continue by closing the server")
        # webbrowser.get(browser).open("http://localhost:5000")
        # try:
        #     displacy.serve(doc, style="ent") # or style="ent" or style="dep"
        # except KeyboardInterrupt:
        #     pass # allow breaking the server quickly
        # print("=====", "server closed. finished parsing:", index+1, "of", len(sentences), "=====")
        # =========== OLD MAIN BLOCK END DO NOT REMOVE ===========
        # =========== OLD MAIN BLOCK END DO NOT REMOVE ===========
        # =========== OLD MAIN BLOCK END DO NOT REMOVE ===========




"""
penn-treebank tag explanations

CC    Coordinating conjunction
CD    Cardinal number
DT    Determiner
EX    Existential there
FW    Foreign word
IN    Preposition or subordinating conjunction
JJ    Adjective
JJR   Adjective, comparative
JJS   Adjective, superlative
LS    List item marker
MD    Modal
NN    Noun, singular or mass
NNS   Noun, plural
NNP   Proper noun, singular
NNPS  Proper noun, plural
PDT   Predeterminer
POS   Possessive ending
PRP   Personal pronoun
PRP$  Possessive pronoun
RB    Adverb
RBR   Adverb, comparative
RBS   Adverb, superlative
RP    Particle
SYM   Symbol
TO    to
UH    Interjection
VB    Verb, base form
VBD   Verb, past tense
VBG   Verb, gerund or present participle
VBN   Verb, past participle
VBP   Verb, non-3rd person singular present
VBZ   Verb, 3rd person singular present
WDT   Wh-determiner
WP    Wh-pronoun
WP$   Possessive wh-pronoun
WRB   Wh-adverb
"""


"""
tags found so far
NN
IN
CD
RBR
JJR
RB
VBZ
MD
VBN
JJ
VB
JJS
PRP
WP
UH
NNS
VBD
RBS
VBG
WDT
$
VBP
NNPS
NNP
TO
POS
DT
RP
PRP$
WRB
CC
"""