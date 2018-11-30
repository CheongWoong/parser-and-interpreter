import sys

from tokenizer import tokenize

class RCFAE():
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
        elif type(self) == If0:
            return '(if0 %s %s %s)' % (self.test, self.then, self.els)
        elif type(self) == Rec:
            return '(rec (%s %s %s))' % (self.name, self.expr, self.first)

class Num(RCFAE):
    def __init__(self, num):
        self.num = num

class Add(RCFAE):
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs

class Sub(RCFAE):
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs

class Mul(RCFAE):
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs

class Id(RCFAE):
    def __init__(self, name):
        self.name = name

class Fun(RCFAE):
    def __init__(self, param, body):
        self.param = param
        self.body = body
        if type(parse(self.param)) != Id:
            return Exception

class App(RCFAE):
    def __init__(self, ftn, arg):
        self.ftn = ftn
        self.arg = arg

class If0(RCFAE):
    def __init__(self, test, then, els):
        self.test = test
        self.then = then
        self.els = els

class Rec(RCFAE):
    def __init__(self, name, expr, first):
        self.name = name
        self.expr = expr
        self.first = first
        if type(parse(self.name)) != Id:
            return Exception

class RCFAE_Value():
    def __str__(self):
        if type(self) == NumV:
            return '(numV %s)' % self.n

class NumV(RCFAE_Value):
    def __init__(self, n):
        self.n = n

class ClosureV(RCFAE_Value):
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

class aRecSub(DefrdSub):
    def __init__(self, name, box, ds):
        self.name = name
        self.box = box
        self.ds = ds

def lookup(name, ds):
    if type(ds) == mtSub:
        sys.exit('error: lookup: free identifier')
    elif type(ds) == aSub:
        return ds.value if ds.name == name else lookup(name, ds.ds)
    elif type(ds) == aRecSub:
        return ds.box if ds.name == name else lookup(name, ds.ds)

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
                elif len(token_) == 1 and token_[0] == 'mtSub':
                    return mtSub()
                elif len(token_) == 4 and token_[0] == 'if0':
                    return If0(parse(token_[1]), parse(token_[2]), parse(token_[3]))
                elif len(token_) == 3 and token_[0] == 'rec' and len(tokenize(token_[1])) == 2:
                    return Rec(tokenize(token_[1])[0], parse(tokenize(token_[1])[1]), parse(token_[2]))

            elif len(expr.split()) == 1 and expr[0].isalpha():
                return Id(expr)

            raise Exception

        except:
            sys.exit('parse: bad syntax: %s' % expr)

def interp(rcfae, ds=mtSub()):
    if type(rcfae) == Num:
        return NumV(rcfae.num)
    elif type(rcfae) == Add:
        return NumV(interp(rcfae.lhs, ds).n + interp(rcfae.rhs, ds).n)
    elif type(rcfae) == Sub:
        return NumV(interp(rcfae.lhs, ds).n - interp(rcfae.rhs, ds).n)
    elif type(rcfae) == Mul:
        return NumV(interp(rcfae.lhs, ds).n * interp(rcfae.rhs, ds).n)
    elif type(rcfae) == Id:
        return lookup(rcfae.name, ds)
    elif type(rcfae) == Fun:
        return ClosureV(rcfae.param, rcfae.body, ds)
    elif type(rcfae) == App:
        f_val = interp(rcfae.ftn, ds)
        a_val = interp(rcfae.arg, ds)
        return interp(f_val.body, aSub(f_val.param, a_val, f_val.ds))
    elif type(rcfae) == If0:
        return interp(rcfae.then, ds) if interp(rcfae.test, ds).n == 0 else interp(rcfae.els, ds)
    elif type(rcfae) == Rec:
        value_holder = NumV(0)
        new_ds = aRecSub(rcfae.name, value_holder, ds)
        new_ds.box = interp(rcfae.expr, new_ds)
        return interp(rcfae.first, new_ds)
