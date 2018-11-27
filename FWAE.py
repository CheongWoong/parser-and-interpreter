import sys

from tokenizer import tokenize

class FWAE():
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
        elif type(self) == Fun:
            return '(fun %s %s)' % (self.param, self.body)
        elif type(self) == App:
            return '(app %s %s)' % (self.ftn, self.arg)

class Num(FWAE):
    def __init__(self, num):
        self.num = num

class Add(FWAE):
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs

class Sub(FWAE):
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs

class With(FWAE):
    def __init__(self, i, v, e):
        self.i = i
        self.v = v
        self.e = e
        if type(parse(self.i)) != Id:
            return Exception

class Id(FWAE):
    def __init__(self, name):
        self.name = name

class Fun(FWAE):
    def __init__(self, param, body):
        self.param = param
        self.body = body
        if type(parse(self.param)) != Id:
            return Exception

class App(FWAE):
    def __init__(self, ftn, arg):
        self.ftn = ftn
        self.arg = arg

def subst(fwae, idtf, val):
    if type(fwae) == Num:
        return fwae
    elif type(fwae) == Add:
        return Add(subst(fwae.lhs, idtf, val), subst(fwae.rhs, idtf, val))
    elif type(fwae) == Sub:
        return Sub(subst(fwae.lhs, idtf, val), subst(fwae.rhs, idtf, val))
    elif type(fwae) == With:
        return With(fwae.i, subst(fwae.v, idtf, val), fwae.e if fwae.i == idtf else subst(fwae.e, idtf, val))
    elif type(fwae) == Id:
        return Num(val) if fwae.name == idtf else fwae
    elif type(fwae) == App:
        return App(subst(fwae.ftn, idtf, val), subst(fwae.arg, idtf, val))
    elif type(fwae) == Fun:
        return fwae if fwae.param == idtf else Fun(fwae.param, subst(fwae.body, idtf, val))

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
                elif len(token_) == 2:
                    return App(parse(token_[0]), parse(token_[1]))
                elif len(token_) == 3 and token_[0] == 'fun' and len(tokenize(token_[1])) == 1:
                    return Fun(tokenize(token_[1])[0], parse(token_[2]))

            elif len(expr.split()) == 1:
                return Id(expr)

            raise Exception

        except:
            sys.exit('parse: bad syntax: %s' % expr)

def interp(fwae):
    if type(fwae) == Num:
        return fwae.num
    elif type(fwae) == Add:
        return interp(fwae.lhs) + interp(fwae.rhs)
    elif type(fwae) == Sub:
        return interp(fwae.lhs) - interp(fwae.rhs)
    elif type(fwae) == With:
        return interp(subst(fwae.e, fwae.i, interp(fwae.v)))
    elif type(fwae) == Id:
        sys.exit('interp: free identifier')
    elif type(fwae) == Fun:
        return fwae
    elif type(fwae) == App:
        ftn = interp(fwae.ftn)
        return interp(subst(ftn.body, ftn.param, interp(fwae.arg)))
