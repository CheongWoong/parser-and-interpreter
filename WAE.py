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
            return '(with %s %s %s)' % (self.name, self.body, self.expr)
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
    def __init__(self, name, body, expr):
        self.name = name
        self.body = body
        self.expr = expr

class Id(WAE):
    def __init__(self, name):
        self.name = name

def parse(expr):
    try:
        return Num(int(expr))

    except:
        try:
            token_ = tokenize(expr)

            if len(token_) == 3 and token_[0] == '+':
                return Add(parse(token_[1]), parse(token_[2]))
            elif len(token_) == 3 and token_[0] == '-':
                return Sub(parse(token_[1]), parse(token_[2]))
            elif len(token_) == 3 and token_[0] == 'with':
                i = tokenize(token_[1])[0]
                v = tokenize(token_[1])[1]
                e = token_[2]
                return With(i, parse(v), parse(e))

            if True: #need to set the condition
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

    return expr
