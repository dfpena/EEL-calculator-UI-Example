
#!/usr/bin/env python
from decorator import decorator

import eel
import math
import sys



def limit_decimal_precision(_float):
    """
    it seems long floats dont limit within the display window
    and total digits we can show is 11
    """
    order_of_magitude = math.log10(_float)
    #  3 will be 0, 30 will be 1 etc etc
    floor = math.floor(order_of_magitude)
    #  e.g. .456 will be -1
    if floor < 0:
        return 10
    return 10 - floor


@decorator
def on_start(func,*args, **kwargs):
    if kwargs !={}:
        try:
            if kwargs['Start']:
                if 'Verbose' in kwargs['Settings']:
                    if kwargs['Settings']['Verbose']:
                        print(func)
                        pass
                response= func(*args,**kwargs)
                return response
            else:
                kwargs['Start'] = False
                print(func,"DID NOT START")
                return(kwargs)
        except Exception as e:
            print('NODE ERROR OCCURED TRYING TO START NODE FUNCTION:')
            print('===========================================')
            print(func,e)
            print('===========================================')
            print('LAST STATE SET TO:')
            print('===========================================')
            print('ekwargs')
            print('===========================================')
            print('LAST NODE FUNCTION SET TO:')
            print('===========================================')
            print('efunc')
            print('===========================================')
            global ekwargs
            global efunc
            ekwargs = kwargs
            efunc = func
            print('HALTING')
            raise
    else:
        print('Empty kwargs')
        return ()



def start():
    return {'Start':True,'Settings':{'Verbose':True},'Status':{},"Threads":[]}

 
@on_start
def eelStart1(*args,**kwargs):

    @eel.expose
    def action1Sqrt(event):
        kwargs['Data'] = event
        return sqrt3(**kwargs)['Data'] 
        
    @eel.expose
    def action2Square(event):
        kwargs['Data'] = event
        return square4(**kwargs)['Data']
    
    
    @eel.expose
    def action3Evaluate(event):
        kwargs['Data'] = event
        return calceval2(**kwargs)['Data'] 
    
    @eel.expose
    def addString(userstring,new):
        if userstring ==  "0":
            userstring=''
        return(userstring+new)
    
    @eel.expose
    def clear():
        return('0')
        
        
    eel.init('web')
    eel.start('index.html', disable_cache=True, size=(400, 675))
    sys.exit()
    return kwargs
 
@on_start
def calceval2(*args,**kwargs):
    out = eval(kwargs['Data'])
    if isinstance(out, float):
        to_round = limit_decimal_precision(out)
        out = round(out, to_round)
    kwargs['Data'] = out
    return kwargs
 
@on_start
def sqrt3(*args,**kwargs):
    kwargs['Data'] = (round(math.sqrt(eval(kwargs['Data'])),5))
    return kwargs
 
@on_start
def square4(*args,**kwargs):
    kwargs['Data'] = eval(kwargs['Data'])**2
    return kwargs
 


class StremeNode:
    def __init__(self):
        pass

    def run(self,*args,**kwargs):
        self.kwargs=eelStart1(**kwargs)
        return (self.kwargs)

class liveprocess:
    def __init__(self):
        self.status="pending"
    def run(self,expname):
        self.response=eelStart1(**start())
        self.status="completed"
        return(self.status)

if __name__ == '__main__':
    process = liveprocess()
    process.run('Local')
    
