import pandas as pd

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