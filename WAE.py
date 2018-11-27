import sys

from tokenizer import tokenize

class WAE():
    def __str__(self):
        if type(self) == Num:
            return '(num %s)' % self.num
        elif type(self) == Add:
            return '(add %s %s)' % (self.lhs, self.rhs)
        elif type(self) == Sub:
            return '(sub %s %s)' % (self.lhs, self.rhs)
        elif type(self) == With:
            return '(with %s %s %s)' % (self.i, self.v, self.e)
        elif type(self) == Id:
            return '(id %s)' % self.name

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
    def __init__(self, i, v, e):
        self.i = i
        self.v = v
        self.e = e
        if type(parse(self.i)) != Id:
            return Exception

class Id(WAE):
    def __init__(self, name):
        self.name = name

def subst(wae, idtf, val):
    if type(wae) == Num:
        return wae
    elif type(wae) == Add:
        return Add(subst(wae.lhs, idtf, val), subst(wae.rhs, idtf, val))
    elif type(wae) == Sub:
        return Sub(subst(wae.lhs, idtf, val), subst(wae.rhs, idtf, val))
    elif type(wae) == With:
        return With(wae.i, subst(wae.v, idtf, val), wae.e if wae.i == idtf else subst(wae.e, idtf, val))
    elif type(wae) == Id:
        return Num(val) if wae.name == idtf else wae

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
                elif len(token_) == 3 and token_[0] == 'with' and len(tokenize(token_[1])) == 2:
                    i = tokenize(token_[1])[0]
                    v = tokenize(token_[1])[1]
                    e = token_[2]
                    return With(i, parse(v), parse(e))

            elif len(expr.split()) == 1:
                return Id(expr)

            raise Exception

        except:
            sys.exit('parse: bad syntax: %s' % expr)

def interp(wae):
    if type(wae) == Num:
        return wae.num
    elif type(wae) == Add:
        return interp(wae.lhs) + interp(wae.rhs)
    elif type(wae) == Sub:
        return interp(wae.lhs) - interp(wae.rhs)
    elif type(wae) == With:
        return interp(subst(wae.e, wae.i, interp(wae.v)))
    elif type(wae) == Id:
        sys.exit('interp: free identifier')
