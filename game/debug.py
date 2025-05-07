def debug(x,y=True):
    if type(y) is bool and type(x) is str:
        if y is True:
            print(x)