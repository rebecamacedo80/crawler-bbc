import pandas as pd
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize
from nltk.tokenize.treebank import TreebankWordDetokenizer
from Levenshtein import *

df = pd.read_csv('/home/rebeca/sentencasRUINS-teste.csv')

stop_words = stopwords.words('portuguese')
twd = TreebankWordDetokenizer()

for index, row in df.iterrows():
    title = row['title'].lower()
    subtitle = row['subtitle'].lower()

    print('title: ', title, '\n')
    print('subtitle: ', subtitle, '\n')

    title_tokens = word_tokenize(title)
    subtitle_tokens = word_tokenize(subtitle)

    print('title TOKENIZADO: ', title_tokens, '\n')
    print('subtitle TOKENIZADO: ', subtitle_tokens, '\n')

    filtered_title = [w for w in title_tokens if not w in stop_words]
    filtered_subtitle = [w for w in subtitle_tokens if not w in stop_words]

    title = twd.detokenize(filtered_title)
    subtitle = twd.detokenize(filtered_subtitle)

    print('title without stopword: ', title)
    print('subtitle without stopword: ', subtitle)

    print('DISTANCIA DE LEVENSHTEIN = ', distance(title, subtitle), '\n', '######################################################################\n')

""" oi = "oi"
ola = "olá"

print(distance(oi, ola)) """