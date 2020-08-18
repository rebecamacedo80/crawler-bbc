import nltk
import re
import pandas as pd
from nltk.corpus import stopwords 
import spacy
import csv
import matplotlib.pyplot as plt
from numpy import mean
from numpy import std
from statistics import pvariance

class Preprocess:
        
    def is_number(self, s):
        try:
            float(s)
            return True
        except ValueError:
            return False

    def preprocess(self, caminho):
        df = pd.read_csv(caminho)
        good = pd.DataFrame(columns=['title', 'subtitle'])
        
        for index, row in df.iterrows():
            print('solving problems ', index)

            title = row['title'].lower()
            subtitle =  row['subtitle'].lower()
            
            title = re.sub('^[\t\n\r\f\v]+', '', title)
            title = re.sub('$[\t\n\r\f\v]+', '', title)
            
            subtitle = re.sub('^[\t\n\r\f\v]+', '', subtitle)
            subtitle = re.sub('$[\t\n\r\f\v]+', '', subtitle)
            subtitle = re.sub('[\t\n\r\f\v]+', ' ', subtitle)
            
            good = good.append({'title': title, 'subtitle': subtitle}, ignore_index=True)
            
        good.to_csv( "Boas_preprossesed.csv", index=False, encoding='utf-8-sig')

    def get_vocabulary(self, caminho):
        df = pd.read_csv(caminho)

        for index, row in df.iterrows():
            title = nlp(row['title'].lower())
            subtitle =  nlp(row['subtitle'].lower())

        stop_words = stopwords.words('portuguese')
        nlp = spacy.load('pt_core_news_sm')

        dictionary = {}

        for index, row in df.iterrows():
            title = nlp(row['title'].lower())
            subtitle =  nlp(row['subtitle'].lower())
            
            #print('TITLE TOKENINZER:  ', title)
            print('índice ', index, '...')
            for token in title:

                if token.text in stop_words or token.is_punct or self.is_number(token.text):
                    continue

                else:
                    if token.text not in dictionary:
                        dictionary[token.text] = 1
                    else:
                        dictionary[token.text] = dictionary[token.text] + 1

            #print('SUBTITLE TOKENINZER:  ', subtitle)
            for token in subtitle:

                if token.text in stop_words or token.is_punct or self.is_number(token.text):
                    continue

                else:
                    if token.text not in dictionary:
                        dictionary[token.text] = 1
                    else:
                        dictionary[token.text] = dictionary[token.text] + 1

        vocab = pd.DataFrame(sorted(dictionary.items(), key=lambda x: x[1], reverse=True))
        vocab.to_csv( "vocabulario3.csv", index=False, encoding='utf-8-sig')

    def get_length(self, caminho):
        df = pd.read_csv(caminho)
        nlp = spacy.load('pt_core_news_sm')

        sum_acc_title = 0
        sum_acc_subtitle = 0
        unit_len_title = []
        unit_len_subtitle = []

        for index, row in df.iterrows():
            title = nlp(row['title'].lower())
            subtitle =  nlp(row['subtitle'].lower())

            print('calculando... ', index)

            #print('Titulo: ', title, 'TAMANHO: ', len(title))
            unit_len_title.append([len(title)])
            sum_acc_title = sum_acc_title + len(title)

            #print('Subtitulo: ', subtitle, 'TAMANHO: ', len(subtitle))
            unit_len_subtitle.append([len(subtitle)])
            sum_acc_subtitle = sum_acc_subtitle + len(subtitle)
        
        print('soma acumulada titulo: ', sum_acc_title)
        print('soma acumulada subtitulo: ', sum_acc_subtitle)

        print('média titulo: ', sum_acc_title/74509)
        print('média subtítulo: ', sum_acc_subtitle/74509)

        file = open('LenTitles.csv', 'w+', newline ='')
        with file:     
            write = csv.writer(file) 
            write.writerows(unit_len_title)
        
        file = open('LenSubitles.csv', 'w+', newline ='')
        with file:     
            write = csv.writer(file) 
            write.writerows(unit_len_subtitle)

    def get_graph(self, caminho):
        df = pd.read_csv(caminho)
        rol = sorted(df['length'])
        print(rol)

        print('média: ', mean(rol))
        print('desvio padrão: ', std(rol))
        print('variância: ', pvariance(rol, mean(rol)))

        plt.figure(figsize=(8, 6))
        plt.hist(rol, bins=[1,100,200,300,400,500,600,700,800])
        # plt.show()
        
        fig2, ax2 = plt.subplots()
        ax2.set_title('Notched boxes')
        ax2.boxplot(rol[:len(rol)-6], showfliers=True, whis=0.75, notch=True)
        #plt.show()
        

        """ at = max(rol) - min(rol) # amplitude total
        print('Amplitude total dos dados:', at)

        k = 5 # numero de classes

        h = round(at/k) # amplitude de classe
        print('A amplitude de classe é:', h)

        # agrupamento
        cla = []
        middle_point = []
        l_inf = []
        l_sup = []

        # Menor valor da série
        menor = min(rol)

        # Menor valor somado a amplitude
        menor_amp = menor+h

        valor = menor
        while valor < max(rol):    
            cla.append('{} - {}'.format(round(valor,1),round(valor+h,1)))
            l_inf.append(valor)
            l_sup.append(valor+h)
            middle_point.append(int((valor + (valor+h))/2))
            
            valor += h

        print('Classes:', cla)
        print('Pontos médios:', middle_point)
        print('L superior:', l_sup)
        print('L inferior', l_inf)

        table_freq = pd.DataFrame( { 'Classes': cla, 'l. inferior': l_inf, 'l. superior': l_sup, 'ponto médio': middle_point } )
        print(table_freq)

        freq_list = [0, 0, 0, 0, 0, 0]
        freq_acc = []

        for number in rol:
            if number >= 1 and number < 535:
                freq_list[0] += 1
            
            elif number >= 535 and number <= 1069:
                freq_list[1] += 1
            
            elif number >= 1069 and number <= 1603:
                freq_list[2] += 1
            
            elif number >= 1603 and number <= 2137:
                freq_list[3] += 1
            
            elif number >= 2137 and number <= 2671:
                freq_list[4] += 1
            
            elif number >= 263205 and number <= 3205:
                freq_list[5] += 1
            
        print('Frequencias:', freq_list)

        acc = 0
        for f in freq_list:
            acc += f
            freq_acc.append(acc)
            
        print('Frequencias acumuladas:', freq_acc)
            
        table_freq['frequencia'] = pd.Series(freq_list, index=table_freq.index)
        table_freq['frequencia acumulada'] = pd.Series(freq_acc, index=table_freq.index)

        print(table_freq)
        
        plt.figure(figsize=(8, 6))
        plt.hist(table_freq['ponto médio'], bins=[1, 535, 1069, 1603, 2137, 2671, 3205], weights=table_freq['frequencia'])
        plt.show() """
  

    """ for x, y in sorted(dictionary.items(), key=lambda x: x[1], reverse=True):
            print(x, y) """

    # ---------------------------------------------------------------------------------------------- #
    """ f = open('/home/rebeca/fairseq_dataset/aval_sentence.se', 'r')
    arq_compression = open("ppDataComp.co", "a")
    arq_setence = open("ppDataSent.se", "a") """

    """ for line in f:
        
        line = line.replace("’", "'")
        line = line.replace("‘", "'")
        #print(line)
        print( re.sub(r"([\w/+$\s-]+|[^\w/+$\s-]+)\s*", r"\1 ", line))
        line = re.sub(r"([\w/+$\s-]+|[^\w/+$\s-]+)\s*", r"\1 ", line) + '\n' 

        arq_setence.write(line) """