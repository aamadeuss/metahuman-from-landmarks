from inspect import getframeinfo, stack
class debugger():
    def __init__(self, print_msg=True):
        self.count = 0
        self.print_msg = print_msg
    
    def p(self, message='test'):
        caller = getframeinfo(stack()[1][0])
        if self.print_msg:
            print("-----DEBUGGER:%s:%d:%s:%d----" % (caller.filename, caller.lineno, message, self.count))
        self.count += 1