import pandas as pd
import pymongo as pm
import numpy as np

client = pm.MongoClient('localhost', 27017)
db = client['IPL']
match = db['matches']


matches = pd.read_csv("matches.csv")

columns = list(matches.columns)
nrows = len(matches)
ncols = len(columns)
objids=[]
temp=[]

for i in range(nrows):
    mat = dict()
    for j in range(ncols):
        if type(matches.iloc[i,j])!=str:
            if matches.iloc[i,j]!=0 and np.isnan(matches.iloc[i,j])==False:
                mat.update({columns[j]:int(matches.iloc[i,j])})
        else:
            mat.update({columns[j]:matches.iloc[i,j]})
    temp.append(mat)
    if len(temp) == 50:
        res = match.insert_many(temp)
        objids.append(res)
        temp=[]

res = match.insert_many(temp)
objids.append(res)

print(len(objids))
