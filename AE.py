import sys

from tokenizer import tokenize

class AE():
    def __str__(self):
        if type(self) == Num:
            return '(num %s)' % self.num
        elif type(self) == Add:
            return '(add %s %s)' % (self.lhs, self.rhs)
        elif type(self) == Sub:
            return '(sub %s %s)' % (self.lhs, self.rhs)

class Num(AE):
    def __init__(self, num):
        self.num = num

class Add(AE):
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs

class Sub(AE):
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs

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
