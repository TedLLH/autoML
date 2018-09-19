import pandas as pd
import os
import sys

df = pd.read_csv(sys.argv[1] + '.csv', names=[sys.argv[1]])

# remove Thumbs.db

print("***Thumbs.db: ", (df[sys.argv[1]] == 'gs://admangoml-vcm/images/'+sys.argv[2]+ '/' +sys.argv[1]+'/Thumbs.db').value_counts())

df = df[df[sys.argv[1]]!='gs://admangoml-vcm/images/'+sys.argv[2]+ '/' +sys.argv[1]+'/Thumbs.db']

print("***after removing Thumbs.db: ", (df[sys.argv[1]] == 'gs://admangoml-vcm/images/'+sys.argv[2]+ '/' +sys.argv[1]+'/Thumbs.db').value_counts())

# remove .csv

print("***.csv: ", (df[sys.argv[1]] == 'gs://admangoml-vcm/images/'+sys.argv[2]+ '/' +sys.argv[1]+'/'+sys.argv[1]+'.csv').value_counts())

df = df[df[sys.argv[1]]!='gs://admangoml-vcm/images/'+sys.argv[2]+ '/' +sys.argv[1]+'/'+sys.argv[1]+'.csv']

print("***after removing .csv: ", (df[sys.argv[1]] == 'gs://admangoml-vcm/images/'+sys.argv[2]+ '/' +sys.argv[1]+'/'+sys.argv[1]+'.csv').value_counts())

# add labels

df['label'] = sys.argv[3]

df.to_csv(sys.argv[1] + '.csv', index=False, header=False)