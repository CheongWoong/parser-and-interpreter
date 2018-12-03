import sys

from tokenizer import tokenize

class FAE():
    def __str__(self):
        if type(self) == Num:
            return '(num %s)' % self.num
        elif type(self) == Add:
            return '(add %s %s)' % (self.lhs, self.rhs)
        elif type(self) == Sub:
            return '(sub %s %s)' % (self.lhs, self.rhs)
        elif type(self) == Mul:
            return '(mul %s %s)' % (self.lhs, self.rhs)
        elif type(self) == Id:
            return '(id %s)' % self.name
        elif type(self) == Fun:
            return '(fun %s %s)' % (self.param, self.body)
        elif type(self) == App:
            return '(app %s %s)' % (self.ftn, self.arg)

class Num(FAE):
    def __init__(self, num):
        self.num = num

class Add(FAE):
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs

class Sub(FAE):
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs

class Mul(FAE):
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs

class Id(FAE):
    def __init__(self, name):
        self.name = name

class Fun(FAE):
    def __init__(self, param, body):
        self.param = param
        self.body = body
        if type(parse(self.param)) != Id:
            return Exception

class App(FAE):
    def __init__(self, ftn, arg):
        self.ftn = ftn
        self.arg = arg

class FAE_Value():
    def __str__(self):
        if type(self) == NumV:
            return '(numV %s)' % self.n

class NumV(FAE_Value):
    def __init__(self, n):
        self.n = n

class ClosureV(FAE_Value):
    def __init__(self, param, body, ds):
        self.param = param
        self.body = body
        self.ds = ds
        if type(parse(self.param)) != Id:
            return Exception

class DefrdSub():
    pass

class mtSub(DefrdSub):
    def __init__(self):
        pass

class aSub(DefrdSub):
    def __init__(self, name, value, ds):
        self.name = name
        self.value = value
        self.ds = ds
        if type(parse(self.name)) != Id:
            return Exception

def lookup(name, ds):
    if type(ds) == mtSub:
        sys.exit('error: lookup: free identifier')
    elif type(ds) == aSub:
        return ds.value if ds.name == name else lookup(name, ds.ds)

def parse(expr):
    try:
        return Num(int(expr))

    except:
        try:
            token_ = tokenize(expr)

            if token_:
                if len(token_) == 3 and token_[0] == '+':
                    return Add(parse(token_[1]), parse(token_[2]))
                elif len(token_) == 3 and token_[0] == '-':
                    return Sub(parse(token_[1]), parse(token_[2]))
                elif len(token_) == 3 and token_[0] == '*':
                    return Mul(parse(token_[1]), parse(token_[2]))
                elif len(token_) == 3 and token_[0] == 'with' and len(tokenize(token_[1])) == 2:
                    i = tokenize(token_[1])[0]
                    v = tokenize(token_[1])[1]
                    e = token_[2]
                    return App(Fun(i, parse(e)), parse(v))
                elif len(token_) == 2:
                    return App(parse(token_[0]), parse(token_[1]))
                elif len(token_) == 3 and token_[0] == 'fun' and len(tokenize(token_[1])) == 1:
                    return Fun(tokenize(token_[1])[0], parse(token_[2]))

            elif len(expr.split()) == 1 and expr[0].isalpha():
                return Id(expr)

            raise Exception

        except:
            sys.exit('parse: bad syntax: %s' % expr)

def interp(fae, ds=mtSub()):
    if type(fae) == Num:
        return NumV(fae.num)
    elif type(fae) == Add:
        return NumV(interp(fae.lhs, ds).n + interp(fae.rhs, ds).n)
    elif type(fae) == Sub:
        return NumV(interp(fae.lhs, ds).n - interp(fae.rhs, ds).n)
    elif type(fae) == Mul:
        return NumV(interp(fae.lhs, ds).n * interp(fae.rhs, ds).n)
    elif type(fae) == Id:
        return lookup(fae.name, ds)
    elif type(fae) == Fun:
        return ClosureV(fae.param, fae.body, ds)
    elif type(fae) == App:
        f_val = interp(fae.ftn, ds)
        a_val = interp(fae.arg, ds)
        return interp(f_val.body, aSub(f_val.param, a_val, f_val.ds))
