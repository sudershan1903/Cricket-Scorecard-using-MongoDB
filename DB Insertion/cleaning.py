def headings(string):
    diction = eval(string)
    keys = list(diction.keys())
    string = ""
    for i in keys:
        string = string + str(i).capitalize() + '\t\t\t'
    return string

def process(string):
    diction = eval(string)
    #keys = list(diction.keys())
    values = list(diction.values())
    string = ""
    for i in values:
        string = string + str(i) + '\t'
    return string

string = "{'date': '2008-05-13', 'team1': 'Kolkata Knight Riders', 'team2': 'Delhi Daredevils', 'winner': 'Kolkata Knight Riders', 'venue': 'Eden Gardens'}"
print(headings(string))
print(process(string))