import pandas as pd
import numpy as np
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize

df = pd.read_csv('/home/rebeca/preprocessedData.csv')
print(df.shape)

for index, row in df.iterrows():
    title = row['title'].lower()
    subtitle = row['subtitle'].lower()

    # X = input("Enter first string: ").lower() 
    # Y = input("Enter second string: ").lower() 
    #title = "Os setores que ainda estão contratando em meio à pandemia"
    #subtitle = "Covid-19 deve causar a maior crise no mercado de trabalho desde a Segunda Guerra, mas ainda há oportunidades em alguns setores - não apenas na saúde."

    # tokenization
    title_tokenize = word_tokenize(title)
    subtitle_tokenize = word_tokenize(subtitle)

    # stopwords
    sw = stopwords.words('portuguese')

    # remove stop words from string 
    title_set = {w for w in title_tokenize if not w in sw}  
    subtitle_set = {w for w in subtitle_tokenize if not w in sw} 
    l1 = []
    l2 = []

    # form a set containing keywords of both strings  
    rvector = title_set.union(subtitle_set)  
    for w in rvector: 
        if w in title_set: l1.append(1) # create a vector 
        else: l1.append(0) 
        if w in subtitle_set: l2.append(1) 
        else: l2.append(0)
    
    cos = []
    c = 0
    # cosine formula  
    for i in range(len(rvector)): 
            c+= l1[i]*l2[i] 
    cosine = c / float((sum(l1)*sum(l2))**0.5)
    cos.append(cosine)

    print("similarity: ", cosine)

print(np.mean(cosine))