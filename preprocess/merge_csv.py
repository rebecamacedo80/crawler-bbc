import pandas as pd
import os
import csv

""" path = '/home/rebeca/crawler-bbc/datasets'

files = []
# r=root, d=directories, f = files
for r, d, f in os.walk(path):
    for file in f:
        if '.csv' in file:
            files.append(os.path.join(r, file))

#combine files in the list
combined_csv = pd.concat([pd.read_csv(f) for f in files])

#export to csv
combined_csv.to_csv( "dataset.csv", index=False, encoding='utf-8-sig')

with open('dataset.csv','w') as dataset:
    datasetWriter = csv.writer(dataset)
    datasetWriter.writerow(['title', 'subtitle']) """

bad_lines = []

df = pd.read_csv('dataset.csv')
print(df.isna().sum())
df = df.dropna(axis=0)

for index, row in df.iterrows():
    #print(row['title'], '\t', row ['subtitle'])

    if len(row['title']) > len(row ['subtitle']):
        bad_lines.append(index)
        
        
    else:
        continue        

print('bad lines = ', len(bad_lines))

df = df.drop(bad_lines)
print(df)

df.to_csv( "preprocessedData.csv", index=False, encoding='utf-8-sig')
