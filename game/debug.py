import json

def debug(x,y=True):
    if type(y) is bool and type(x) is str:
        if y is True:
            print(x)

def read_message(x,y):
    if x != "server" and x !="client":
        if x == True or x ==1:
            x="server"
        elif x == False or x == 0:
            x="client"
        else:
            return ""
    a = json.load(open('./game/data/Message.json'))
    return a[x]