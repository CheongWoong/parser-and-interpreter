import sys

from tokenizer import tokenize

class RBMRCFAE():
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
        elif type(self) == Refun:
            pass
        elif type(self) == Setvar:
            pass
        elif type(self) == Newbox:
            pass
        elif type(self) == Setbox:
            pass
        elif type(self) == Openbox:
            pass
        elif type(self) == Seqn:
            pass

class Num(RBMRCFAE):
    def __init__(self, num):
        self.num = num

class Add(RBMRCFAE):
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs

class Sub(RBMRCFAE):
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs

class Mul(RBMRCFAE):
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs

class Id(RBMRCFAE):
    def __init__(self, name):
        self.name = name

class Fun(RBMRCFAE):
    def __init__(self, param, body):
        self.param = param
        self.body = body
        if type(parse(self.param)) != Id:
            return Exception

class App(RBMRCFAE):
    def __init__(self, ftn, arg):
        self.ftn = ftn
        self.arg = arg

class If0(RBMRCFAE):
    def __init__(self, test, then, els):
        self.test = test
        self.then = then
        self.els = els

class Rec(RBMRCFAE):
    def __init__(self, name, expr, first):
        self.name = name
        self.expr = expr
        self.first = first
        if type(parse(self.name)) != Id:
            return Exception

class Refun(RBMRCFAE):
    def __init__(self, param, body):
        self.param = param
        self.body = body
        if type(parse(self.param)) != Id:
            return Exception

class Setvar(RBMRCFAE):
    def __init__(self, name, v):
        self.name = name
        self.v = v
        if type(parse(self.name)) != Id:
            return Exception

class Newbox(RBMRCFAE):
    def __init__(self, v):
        self.v = v

class Setbox(RBMRCFAE):
    def __init__(self, bn, v):
        self.bn = bn
        self.v = v

class Openbox(RBMRCFAE):
    def __init__(self, v):
        self.v = v

class Seqn(RBMRCFAE):
    def __init__(self, ex1, ex2):
        self.ex1 = ex1
        self.ex2 = ex2

class RBMRCFAE_Value():
    def __str__(self):
        if type(self) == NumV:
            return '(numV %s)' % self.n

class NumV(RBMRCFAE_Value):
    def __init__(self, n):
        self.n = n

class ClosureV(RBMRCFAE_Value):
    def __init__(self, param, body, ds):
        self.param = param
        self.body = body
        self.ds = ds
        if type(parse(self.param)) != Id:
            return Exception

class BoxV(RBMRCFAE_Value):
    def __init__(self, address):
        self.address = int(address)

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

class Store():
    pass

class mtSto(Store):
    def __init__(self):
        pass

class aSto(Store):
    def __init__(self, address, value, rest):
        self.address = int(address)
        self.value = value
        self.rest = rest

class Value_Store():
    pass

class V_S(Value_Store):
    def __init__(self, value, store):
        self.value = value
        self.store = store

def lookup(name, ds):
    if type(ds) == mtSub:
        sys.exit('error: lookup: free identifier')
    elif type(ds) == aSub:
        return ds.value if ds.name == name else lookup(name, ds.ds)
    elif type(ds) == aRecSub:
        return ds.box if ds.name == name else lookup(name, ds.ds)

def store_lookup(address, sto):
    if type(sto) == mtSto:
        sys.exit('error: store_lookup: No value at address')
    elif type(sto) == aSto:
        return sto.value if sto.address == address else store_lookup(address, sto.rest)

def malloc(st):
    return max_address(st) + 1

def max_address(st):
    if type(st) == mtSto:
        return 0
    elif type(st) == aSto:
        return max(st.address, max_address(st))

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

def interp(rbmrcfae, ds=mtSub()):
    if type(rbmrcfae) == Num:
        return NumV(rbmrcfae.num)
    elif type(rbmrcfae) == Add:
        return NumV(interp(rbmrcfae.lhs, ds).n + interp(rbmrcfae.rhs, ds).n)
    elif type(rbmrcfae) == Sub:
        return NumV(interp(rbmrcfae.lhs, ds).n - interp(rbmrcfae.rhs, ds).n)
    elif type(rbmrcfae) == Mul:
        return NumV(interp(rbmrcfae.lhs, ds).n * interp(rbmrcfae.rhs, ds).n)
    elif type(rbmrcfae) == Id:
        return lookup(rbmrcfae.name, ds)
    elif type(rbmrcfae) == Fun:
        return ClosureV(rbmrcfae.param, rbmrcfae.body, ds)
    elif type(rbmrcfae) == App:
        f_val = interp(rbmrcfae.ftn, ds)
        a_val = interp(rbmrcfae.arg, ds)
        return interp(f_val.body, aSub(f_val.param, a_val, f_val.ds))
    elif type(rbmrcfae) == If0:
        return interp(rbmrcfae.then, ds) if interp(rbmrcfae.test, ds).n == 0 else interp(rbmrcfae.els, ds)
    elif type(rbmrcfae) == Rec:
        value_holder = NumV(0)
        new_ds = aRecSub(rbmrcfae.name, value_holder, ds)
        new_ds.box = interp(rbmrcfae.expr, new_ds)
        return interp(rbmrcfae.first, new_ds)
