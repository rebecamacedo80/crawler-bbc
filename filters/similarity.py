import pandas as pd
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize
from nltk.stem import RSLPStemmer
import spacy
from spacy.lemmatizer import Lemmatizer

df = pd.read_csv('/home/rebeca/preprocessedData.csv')
df_good = pd.DataFrame(columns=['Title', 'Subtitle'])
df_bad = pd.DataFrame(columns=['Title', 'Subtitle'])

stop_words = stopwords.words('portuguese')
stemmer = RSLPStemmer()
nlp = spacy.load('pt_core_news_sm')

words_tit = []
words_sub = []

bad_sentence = 0
good_sentence = 0

for index, row in df.iterrows():
    title = nlp(row['title'].lower())
    subtitle =  nlp(row['subtitle'].lower())

    for token in title:
        if token.text in stop_words or token.is_punct:
            continue
        else:
            if token.pos_ in ['VERB', 'AUX']:
                words_tit.append(stemmer.stem(token.lemma_))
            else:
                words_tit.append(stemmer.stem(token.text))

    for token in subtitle:
        if token.text in stop_words or token.is_punct:
            continue
        else:
            if token.pos_ in ['VERB', 'AUX']:
                words_sub.append(stemmer.stem(token.lemma_))
            else:
                words_sub.append(stemmer.stem(token.text))
                
    """ print(title)
    print('Palavras título: ', words_tit, '\n')
    print(subtitle)
    print('Palavras subtítulo: ', words_sub, '\n') """

    count = 0
    for word in words_tit:
        if word in words_sub:
            count = count + 1
    
    if len(words_tit) != 0:
        if count/len(words_tit) > 0.40:
            good_sentence = good_sentence + 1

            print('\n----------------------------------------------------------------\n')
            print('BOA DUPLA:\nTitle: "', title, '"\nSubtitle: ', subtitle)

            df_good = df_good.append({'Title': title, 'Subtitle': subtitle}, ignore_index=True)

        else:
            bad_sentence = bad_sentence + 1

            print('\n----------------------------------------------------------------\n')
            print('MÁ DUPLAS:\nTitle: "', title, '"\nSubtitle: ', subtitle)

            df_bad = df_bad.append({'Title': title, 'Subtitle': subtitle}, ignore_index=True)
    else:
        print('TITLE erro: ', title, '\nSUBTITLE erro: ', subtitle)

    words_tit.clear()
    words_sub.clear()

df_good.to_csv( "dupasBoas.csv", index=False, encoding='utf-8-sig')
df_bad.to_csv( "duplasRuins.csv", index=False, encoding='utf-8-sig')

print('\n----------------------------------------------------------------\n')    
print('Sentenças boas = ', good_sentence, '\n')
print('Sentenças ruins = ', bad_sentence, '\n')


""" def convertSingular(self, word):
        if word[-3:] == 'éis':
            word = word.replace(word[-3:], 'el')
            return word

        elif word[-3:] == 'ais':
            word = word.replace(word[-3:], 'al')
            return word
        
        elif word[-3:] == 'uis':
            word = word.replace(word[-3:], 'ul')
            return word
        
        elif word[-3:] == 'óis':
            word = word.replace(word[-3:], 'ol')
            return word

        elif word[-3:] == 'eis':
            word = word.replace(word[-3:], 'il')
            return word

        elif word[-3:] in ['ãos', 'ães', 'ões']:
            word = word.replace(word[-3:], 'ão')
            return word

        elif word[-3:] in ['res', 'zes', 'ses']:
            word = word.replace(word[-2:], '')
            return word

        elif word[-2:] == 'ns':
            word = word.replace(word[-2:], 'm')
            return word
        
        elif word[-2:] == 'is':
            word = word.replace(word[-2:], 'il')
            return word

        elif word[-1:] == 's':
            word = word[:-1]
            return word

        else:
            return word """  

#doc = nlp(u'Você encontrou o livro que eu te falei, Carla?')

""" stop_words = stopwords.words('portuguese')
stemmer = RSLPStemmer()

words_tit = []
words_sub = []

for index, row in df.iterrows():
    title = row['title'].lower()
    subtitle = row['subtitle'].lower()

    title_tokens = word_tokenize(title)
    subtitle_tokens = word_tokenize(subtitle)

    for token in title_tokens:
        if token not in stop_words:
            words_tit.append(stemmer.stem(token))

    print('"', title, '"\n')
    print('titulo tokenizado:\n', words_tit, '\n\n')

    for token in subtitle_tokens:
        if token not in stop_words:
            words_sub.append(stemmer.stem(token))
    
    print('"', subtitle, '"\n')
    print('subtitulo tokenizado:\n', words_sub, '\n\n')

    print('#################################################################\n')

    words_tit.clear()
    words_sub.clear() """