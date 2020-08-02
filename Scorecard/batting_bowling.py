import pymongo as pm

client = pm.MongoClient('localhost', 27017)
db = client['IPL']
dlvry = db['deliveries']

match = db['matches']

def batting(id,inn):
    batsmen1 = dlvry.find({'match_id':id,'inning':inn}).distinct('batsman')
    noofballs1 =[]
    scores1=[]
    fours1=[]
    sixes1=[]
    strikerate1=[]
    for bat in batsmen1:
#        noofballs1.append(dlvry.count_documents({'match_id':id,'inning':inn,'batsman':bat,'wide_runs':{'$nin': [1,2,3,4,5]},'noball_runs':{'$exists':False}}))          
        noofballs1.append(dlvry.count_documents({'match_id':id,'inning':inn,'batsman':bat,'wide_runs':{'$exists':False},'noball_runs':{'$exists':False}}))
        pipeline1 = [{ '$match': {'$and': [ { 'match_id': id }, { 'inning': inn },{'batsman':bat}] }},{'$group':{'_id':1,'all':{'$sum':'$batsman_runs'}}}]
        scores1.append(list(dlvry.aggregate(pipeline1))[0]['all'])
        fours1.append(dlvry.count_documents({'match_id':id,'inning':inn,'batsman':bat,'batsman_runs':4}))
        sixes1.append(dlvry.count_documents({'match_id':id,'inning':inn,'batsman':bat,'batsman_runs':6}))
    total1 = sum(scores1)
    nob1=dlvry.count_documents({'match_id':id,'inning':inn,'wide_runs':{'$exists':False},'noball_runs':{'$exists':False}})
    a = int(nob1/6)
    b = nob1-6*a
    overs1=a+0.1*b
    now1 = dlvry.count_documents({'match_id':id,'inning':inn,'player_dismissed':{'$exists':True}})
    nb1=dlvry.count_documents({'match_id':id,'inning':inn,'noball_runs':1})
    pipe1 = [{ '$match': {'$and': [ { 'match_id': id }, { 'inning': inn },{'wide_runs':{'$in':[1,2,3,4,5]}}]}},{'$group':{'_id':1,'all':{'$sum':'$total_runs'}}}]
    t=list(dlvry.aggregate(pipe1))
    if len(t)!=0:
        wide1 = t[0]['all']
    else:
        wide1=0
    pipe1 = [{ '$match': {'$and': [ { 'match_id': id }, { 'inning': inn },{'bye_runs':{'$in':[1,2,3,4,5]}}]}},{'$group':{'_id':1,'all':{'$sum':'$total_runs'}}}]    
    t=list(dlvry.aggregate(pipe1))
    if len(t)!=0:
        bye1 = t[0]['all']
    else:
        bye1=0
    pipe1 = [{ '$match': {'$and': [ { 'match_id': id }, { 'inning': inn },{'legbye_runs':{'$in':[1,2,3,4,5]}}]}},{'$group':{'_id':1,'all':{'$sum':'$total_runs'}}}]    
    t=list(dlvry.aggregate(pipe1))
    if len(t)!=0:
        legbye1 = t[0]['all']
    else:
        legbye1=0
    pipe1 = [{ '$match': {'$and': [ { 'match_id': id }, { 'inning': inn },{'penalty_runs':{'$in':[1,2,3,4,5]}}]}},{'$group':{'_id':1,'all':{'$sum':'$total_runs'}}}]    
    t=list(dlvry.aggregate(pipe1))
    if len(t)!=0:
        penalty1 = t[0]['all']
    else:
        penalty1=0
        
    extra1 = nb1+wide1+bye1+legbye1+penalty1
    for i in range(len(scores1)):
        strikerate1.append(round(scores1[i]/noofballs1[i]*100,2))
#    print(noofballs1)
#    print(scores1)
#    print(fours1)
#    print(sixes1)
#    print(strikerate1)
#    print(total1+extra1)
#    print(now1)

    string = "Batting\t\tR\tB\t4s\t6s\tS/R\n"
    for i in range(len(batsmen1)):
        st = batsmen1[i]+" \t"+ str(scores1[i])+"\t"+str(noofballs1[i])+"\t"+str(fours1[i])+"\t"+str(sixes1[i])+"\t"+str(strikerate1[i])+"\n"
        string = string +st
    
    string = string + "Extras\t\t\t" + str(extra1)+" ( NB "+str(nb1)+", W "+str(wide1)+", B "+str(bye1)+", LB "+str(legbye1)+")\n"
    string = string + "Total Runs\t\t\t"+str(total1+extra1)+" ("+str(now1)+" wkts, "+str(overs1)+" ov)\n" 
    return string


def bowling(id,inn):
    bowler1 = dlvry.find({'match_id':id,'inning':inn}).distinct('bowler')
#    print(bowler1)
    balls1=[]
    overs1=[]
    runs1=[]
    wickets1=[]
    economy1=[]
    
    for bowl in bowler1:
        balls1.append(dlvry.count_documents({'match_id':id,'inning':inn,'bowler':bowl,'wide_runs':{'$exists':False},'noball_runs':{'$exists':False}}))
        pipeline1 = [{ '$match': {'$and': [ { 'match_id': id }, { 'inning': inn },{'bowler':bowl},{'legbye_runs':{'$exists':False}}] }},{'$group':{'_id':1,'all':{'$sum':'$total_runs'}}}]
        runs1.append(list(dlvry.aggregate(pipeline1))[0]['all'])
        wickets1.append(dlvry.count_documents({'match_id':id,'inning':inn,'bowler':bowl,'dismissal_kind':{'$exists':True,'$ne':'run out'}}))
        
    for i in range(len(balls1)):
        a = int(balls1[i]/6)
        b = balls1[i]-6*a
        overs1.append(a+0.1*b)
        economy1.append(round(runs1[i]/balls1[i]*6,2))
#    print(overs1)
#    print(runs1)
#    print(wickets1)
#    print(economy1)
    
    string = "Bowling\t\t O\tR\tW\tEcon\n"
    for i in range(len(bowler1)):
        st = bowler1[i]+"\t"+ str(overs1[i])+"\t"+str(runs1[i])+"\t"+str(wickets1[i])+"\t"+str(economy1[i])+"\n"
        string = string +st
    return string
    
team1 = teams[4]
team2 = teams[6]
year = seasons[9]
venue = venues[7]
mlist=[]
for mat in match.find({'team1':team1,'team2':team2,'venue':venue,'season':year},{'_id':0,'player_of_match':0,'umpire1':0,'umpire2':0,'umpire3':0}):
    mlist.append(mat)
for mat in match.find({'team1':team2,'team2':team1,'venue':venue,'season':year},{'_id':0,'player_of_match':0,'umpire1':0,'umpire2':0,'umpire3':0}):
    mlist.append(mat)
#print(mlist)

option = 1 
id = mlist[option-1]['id']
#team1 = mlist[option-1]['team1']
#team2 = mlist[option-1]['team2']
#year = mlist[option-1]['season']

print(batting(id,1))
print(batting(id,2))
print(bowling(id,1))
print(bowling(id,2))
