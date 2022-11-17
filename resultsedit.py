import pandas as pd

file = r"/Users/yotamtwersky/Documents/GitHub/p-recommender/data/results.json"
error_lines_bad = False
df1 = pd.read_json(file)
print (df1.head())

file2 = r"/Users/yotamtwersky/Documents/GitHub/p-recommender/data_science/cleaned_data5scheduler.json"
df2 = pd.read_json(file2)
print (df2.head())
outputlist = []
for i in df1[0]:
    for j in range(len(df2)):
        #print(df2["identifier"][j])
        if df2["identifier"][j] == i:
            i = i + " " + df2["title"][j]
            outputlist = outputlist + [i]

import json
with open(r'/Users/yotamtwersky/Documents/GitHub/p-recommender/newresults.txt', 'w') as f:
    json.dump(outputlist, f)