import pandas as pd
import pymongo as pm
import numpy as np

client = pm.MongoClient('localhost', 27017)
db = client['IPL']
deliveries = db['deliveries']


dlvrs = pd.read_csv("deliveries.csv")
#print(dlvrs.head())

columns = list(dlvrs.columns)
nrows = len(dlvrs)
ncols = len(columns)
objids=[]
temp=[]
for i in range(nrows):
    ball = dict()
    for j in range(ncols):
        if type(dlvrs.iloc[i,j])!=str:
            if dlvrs.iloc[i,j]!=0 and np.isnan(dlvrs.iloc[i,j])==False:
                ball.update({columns[j]:int(dlvrs.iloc[i,j])})
        else:
            ball.update({columns[j]:dlvrs.iloc[i,j]})
    temp.append(ball)
    if len(temp) == 100:
        res = deliveries.insert_many(temp)
        objids.append(res)
        temp=[]

res = deliveries.insert_many(temp)
objids.append(res)

print(len(objids))
            
