import sys

class WAE():
    def __str__(self):
        if type(self) == Num:
            return '(num %s)' % self.num
        elif type(self) == Add:
            return '(add %s %s)' % (self.lhs, self.rhs)
        elif type(self) == Sub:
            return '(sub %s %s)' % (self.lhs, self.rhs)
        elif type(self) == With:
            return '(with (%s %s) %s)' % (self.name, self.body, self.expr)
        elif type(self) == Id:
            return 

class Num(WAE):
    def __init__(self, num):
        self.num = num

class Add(WAE):
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs

class Sub(WAE):
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs

class With(WAE):
    def __init__(self, name, body, expr):
        self.name = name
        self.body = body
        self.expr = expr

class Id(WAE):
    def __init__(self, name):
        self.name = name

def parse(expr):
    expr = expr.lstrip().rstrip()
    expr = expr.replace('{', '(')
    expr = expr.replace('[', '(')
    expr = expr.replace('}', ')')
    expr = expr.replace(']', ')')
    
    try:
        return Num(int(expr))
    
    except:
        try:
            if expr[:3] == '( +' or expr[:2] == '(+' or expr[:3] == '( -' or expr[:2] == '(-':
                n = 2 if expr[1] == ' ' else 1
                op = expr[n]
                
                cnt = 0
                hs = [None, '', '']
                concat = 0
                for s in expr[n+1:-1]:
                    if s == ' ' and concat <= 0:
                        cnt += 1
                    elif s == '(':
                        concat += 1
                        hs[cnt] += '(' 
                    elif s == ')':
                        concat -= 1
                        hs[cnt] += ')' 
                    else:
                        hs[cnt] = hs[cnt] + s
                    
                if op == '+':
                    return Add(parse(hs[1]), parse(hs[2]))
                else:
                    return Sub(parse(hs[1]), parse(hs[2]))
                
            else:
                raise Exception
            
        except:
            sys.exit('parse: bad syntax: %s' % expr)

def interp(ae):
    if type(ae) == Num:
        return ae.num
    elif type(ae) == Add:
        return interp(ae.lhs) + interp(ae.rhs)
    elif type(ae) == Sub:
        return interp(ae.lhs) - interp(ae.rhs)
        
    return expr

