import pymongo as pm
import pprint as p

client = pm.MongoClient('localhost', 27017)
#db = client['IPL']
#match = db['matches']
db = client['IPL']
deliveries = db['deliveries']

for dlvry in deliveries.find({'bowler':'A Choudhary'}):
    p.pprint(dlvry)