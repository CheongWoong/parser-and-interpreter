import sys

from tokenizer import tokenize
import RCFAE

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
            return '(refun %s %s)' % (self.param, self.body)
        elif type(self) == Setvar:
            return '(setvar %s %s)' % (self.name, self.v)
        elif type(self) == Newbox:
            return '(newbox %s)' % self.v
        elif type(self) == Setbox:
            return '(setbox %s %s)' % (self.bn, self.v)
        elif type(self) == Openbox:
            return '(openbox %s)' % self.v
        elif type(self) == Seqn:
            return '(seqn %s %s)' % (self.ex1, self.ex2)

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
        if type(self) == RefclosV:
            return '(refclosV %s %s %s)' % (self.param, self.body, self.ds)

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

class RefclosV(RBMRCFAE_Value):
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
    def __str__(self):
        return '(mtSub)'

class aSub(DefrdSub):
    def __init__(self, name, address, ds):
        self.name = name
        self.address = int(address)
        self.ds = ds
        if type(parse(self.name)) != Id:
            return Exception

class aRecSub(DefrdSub):
    def __init__(self, name, box, ds):
        self.name = name
        self.box = box
        self.ds = ds

class Store():
    def __str__(self):
        if type(self) == mtSto:
            return '(mtSto)'
        elif type(self) == aSto:
            return '(aSto %s %s %s)' % (str(self.address), str(self.value), str(self.rest))

class mtSto(Store):
    pass

class aSto(Store):
    def __init__(self, address, value, rest):
        self.address = int(address)
        self.value = value
        self.rest = rest

class Value_Store():
    def __str__(self):
        return '(v*s %s %s)' % (str(self.value), str(self.store))

class V_S(Value_Store):
    def __init__(self, value, store):
        self.value = value
        self.store = store

def lookup(name, ds):
    if type(ds) == mtSub:
        sys.exit('error: lookup: free identifier')
    elif type(ds) == aSub:
        return ds.address if ds.name == name else lookup(name, ds.ds)
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
        return max(st.address, max_address(st.rest))

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
                elif len(token_) == 4 and token_[0] == 'if0':
                    return If0(parse(token_[1]), parse(token_[2]), parse(token_[3]))
                elif len(token_) == 3 and token_[0] == 'rec' and len(tokenize(token_[1])) == 2:
                    return Rec(tokenize(token_[1])[0], parse(tokenize(token_[1])[1]), parse(token_[2]))
                elif len(token_) == 2 and token_[0] == 'newbox':
                    return Newbox(parse(token_[1]))
                elif len(token_) == 3 and token_[0] == 'setbox':
                    return Setbox(parse(token_[1]), parse(token_[2]))
                elif len(token_) == 2 and token_[0] == 'openbox':
                    return Openbox(parse(token_[1]))
                elif len(token_) == 3 and token_[0] == 'seqn':
                    return Seqn(parse(token_[1]), parse(token_[2]))
                elif len(token_) == 3 and token_[0] == 'fun' and len(tokenize(token_[1])) == 1:
                    return Fun(tokenize(token_[1])[0], parse(token_[2]))
                elif len(token_) == 3 and token_[0] == 'refun' and len(tokenize(token_[1])) == 1:
                    return Refun(tokenize(token_[1])[0], parse(token_[2]))
                elif len(token_) == 2:
                    return App(parse(token_[0]), parse(token_[1]))
                elif len(token_) == 3 and token_[0] == 'setvar':
                    return Setvar(token_[1], parse(token_[2]))

            elif len(expr.split()) == 1 and expr[0].isalpha():
                return Id(expr)

            raise Exception

        except:
            sys.exit('parse: bad syntax: %s' % expr)

def interp(rbmrcfae, ds=mtSub(), st=mtSto()):
    if type(rbmrcfae) == Num:
        return V_S(NumV(rbmrcfae.num), st)
    elif type(rbmrcfae) == Add:
        return interp_two(rbmrcfae.lhs, rbmrcfae.rhs, ds, st, lambda a, b, c: V_S(a.n + b.n, c))
    elif type(rbmrcfae) == Sub:
        return interp_two(rbmrcfae.lhs, rbmrcfae.rhs, ds, st, lambda a, b, c: V_S(a.n - b.n, c))
    elif type(rbmrcfae) == Mul:
        return interp_two(rbmrcfae.lhs, rbmrcfae.rhs, ds, st, lambda a, b, c: V_S(a.n * b.n, c))
    elif type(rbmrcfae) == Id:
        return V_S(store_lookup(lookup(rbmrcfae.name, ds), st), st)
    elif type(rbmrcfae) == Fun:
        return V_S(ClosureV(rbmrcfae.param, rbmrcfae.body, ds), st)
    elif type(rbmrcfae) == Refun:
        return V_S(RefclosV(rbmrcfae.param, rbmrcfae.body, ds), st)
    elif type(rbmrcfae) == App:
        temp = interp(rbmrcfae.ftn, ds, st)
        if type(temp) == V_S:
            f_value = temp.value
            f_store = temp.store
            if type(f_value) == ClosureV:
                temp2 = interp(rbmrcfae.arg, ds, f_store)
                if type(temp2) == V_S:
                    a_value = temp2.value
                    a_store = temp2.store
                    new_address = malloc(a_store)
                    return interp(f_value.body, aSub(f_value.param, new_address, f_value.ds), aSto(new_address, a_value, a_store))
            elif type(f_value) == RefclosV:
                address = lookup(rbmrcfae.arg.name, ds)
                return interp(f_value.body, aSub(f_value.param, address, f_value.ds), f_store)
            else:
                sys.exit('error: interp: trying to apply a number')
    elif type(rbmrcfae) == Newbox:
        temp = interp(rbmrcfae.v, ds, st)
        if type(temp) == V_S:
            a = malloc(temp.st)
            return V_S(BoxV(a), aSto(a, temp.v, temp.st))
    elif type(rbmrcfae) == Setbox:
        return interp_two(rbmrcfae.bn, rbmrcfae.v, ds, st, lambda a, b, c: V_S(b, aSto(a.address, b, c)))
    elif type(rbmrcfae) == Openbox:
        temp = interp(rbmrcfae.v, ds, st)
        if type(temp) == V_S:
            return V_S(store_lookup(temp.v.address, temp.st), temp.st)
    elif type(rbmrcfae) == Seqn:
        return interp_two(rbmrcfae.ex1, rbmrcfae.ex2, ds, st, lambda a, b, c: V_S(b, c))
    elif type(rbmrcfae) == Setvar:
        a = lookup(rbmrcfae.name, ds)
        temp = interp(rbmrcfae.v, ds, st)
        if type(temp) == V_S:
            return V_S(temp.value, aSto(a, temp.value, temp.store))
    elif type(rbmrcfae) == If0:
        return interp(rbmrcfae.then, ds, st) if interp(rbmrcfae.test, ds, st).n == 0 else interp(rbmrcfae.els, ds, st)
    elif type(rbmrcfae) == Rec:
        value_holder = NumV(0)
        new_ds = aRecSub(rbmrcfae.name, value_holder, ds)
        new_ds.box = RCFAE.interp(rbmrcfae.expr, new_ds)
        value = RCFAE.interp(rbmrcfae.first, new_ds)
        value = NumV(value.n)
        return V_S(value, st)

def interp_two(expr1, expr2, ds, st, handle):
    temp = interp(expr1, ds, st)
    if type(temp) == V_S:
        temp2 = interp(expr2, ds, temp.store)
        if type(temp2) == V_S:
            return handle(temp.value, temp2.value, temp2.store)
