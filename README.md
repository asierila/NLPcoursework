# NLPcoursework
A repo for the course project on course 521158S Natural Language Processing and Text Mining at University of Oulu.

-----------------
    

## Project assignment
Project 10: Automatic Text Summarization 1


This project aims to implement new approaches for automatic text summarization
and evaluate their performances on small sample dataset. The Rouge-N metric is 
the standard in evaluating the

1.	First, study the open text summarization available in 
https://github.com/jaijuneja/PyTLDR It uses an extraction based summarization 
where the sentences are scored and the highly scored sentences are included in 
the summarizer. Three scoring techniques have been implemented on this package.
One is based on TextRank algorithm (it uses PageRank) and the second is based 
on Latent Semantic Analysis. (You can also check for another PageRank 
summarizer at https://github.com/davidadamojr/TextRank), while the third one 
uses relevance sentence scoring using cosine similarity, see details on the link. 
Check that the programs correctly when using either html documents or text 
documents as input. Demonstrate this finding through an example of your own 
original document and comment on the summarizer outputted by TextRank, Latent 
Semantic and Relevance sentence scoring algorithms.

2.	Design a simple GUI where the user can input a link or source file of the 
document to be summarized and output the summarizer using each of the three above 
methods.

3.	We would like to evaluate the performance of the three summarizers using a 
standard evaluation metric. ROUGE-2, ROUGE-3 are commonly employed to evaluate 
the extent of overlapping between an automatically generated abstract and a set 
of manually generated summaries. Consider the CNN/Dailymail dataset that you can 
download from https://github.com/morningmoni/FAR. You need a simple python script 
that allows you to quantify ROUGE-2 and ROUGE-3, you can inspire from numerous 
implementations available online of automatic summarizers. Your task is to assess
the performance of each of three summarizers on CNN/Dailymail dataset using 
ROUGE-2 and ROUGE-3 metrics. Comment on the performance and limitations of the 
tested algorithms.

4.	We want to extend the above summarization by incorporating coherence of text 
with respect to named-entity. For this purpose, first use SpaCy named-entity tagger 
and identify person or organization named-entity. Suggest a simple heuristic that 
enables whenever a sentence outputted by a given algorithm contains a person or an 
organization named-entity, then other sentences in the original document that contain 
the same named-entity, , if not outputted by the underlined algorithm, will also be 
included in the summarizer up to a certain threshold (that you can discuss and tune up). 
Run the newly designed algorithm on the same CNN/Dailymail dataset, and report the ROUGE-2 
and ROUGE-3 performances.

5.	Suggest a GUI where the user can input his own text to be summarized 
(or a link / pointer to the location of the original document) and output the summary 
according to each of the aforementioned methodologies.

-----------------
## Käännös parhaan ymmärryksemme mukaan

Projekti 10: Tekstin tiivistys 1

Projektin tarkoitus on kehittää uusia keinoja automaattiseen tekstin
tiivistämiseen ja testata niiden toimivuutta pienellä datasetillä.
ROUGE-N metriikka on standardi tekstin tiivistämisen arvioinnissa.

1.  Ensimmäisenä tutki open sauce tekstin tiivistäjää 
https://github.com/jaijuneja/PyTLDR. Se pisteyttää lauseet ja ottaa
mukaan tiivistelmään isoimmat pisteet saaneet. PyTLDR sisältää kolme
tiivistäjää jotka ovat: textRank algoritmi (käyttää pagerankkia), latent
semantic analysis, ja relevance sentence scoring joka käyttää cosine
similarity:ä. Tarkista että nämä kolme toimii plaintekstillä ja HTML
filuilla. Demoa tämän jälkeen omilla teksteillä.

2.  Suunnittele simppeli GUI johon voi laittaa linkin source filun
dokumentista, joka tiivistetään. Outputtina tiivistelmä kolmella eri
keinolla.

3.  Arvioi näitä kolmea tiivistäjää. Rouge2 ja Rouge3 on tyypillisesti
käytössä kun verrataan automaattista ja manuaalista tiivistystä. Käytä
CNN/Dailymail datasettia täältä https://github.com/morningmoni/FAR.
Käytä Rouge2 ja Rouge3 metriikoita näiden kolmen tiivistäjän
arviointiin kyseisellä datasetillä. Kommentoi näiden algoritmien
suorituskykyä ja rajoitetteita.

4.  Haluamme laajentaa ylläolevaa tiivistelmää ottamalla mukaan
tekstin koherenssin named-entityjen mukaan. Tähän tarkoitukseen
käytä spaCy named-entity taggeria ja identifioi henkilöt ja organisaatiot.
Ehdota yksinkertaista heuristiikka, joka tutkii valmista tiivistelmää käyden
läpi sen jokaisen lauseen. Jos jossain tiivistelmän lauseissa on nimetty enti-
teetti, niin muuta algortimia jollain thresholdilla ottamaan mukaan
herkemmin lauseita alkuperäisestä tekstistä, joissa on on sama named-entity.
Aja parannetut algoritmit samalle datasetille, ja raportoi toimintaa kuten aiemmin.

5.  Toteuta sama GUI uusille algoritmeille.
