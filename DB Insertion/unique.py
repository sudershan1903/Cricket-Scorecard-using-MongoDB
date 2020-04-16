import pymongo as pm

client = pm.MongoClient('localhost', 27017)
db = client['IPL']
match = db['matches']

#p.pprint(match.find_one())

teams=sorted(match.distinct('team1'))

venues=sorted(match.distinct('venue'))

seasons = sorted(match.distinct('season'))
    
