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
    expr = expr.replace('{', '(').replace('}', ')')
    expr = expr.replace('[', '(').replace(']', ')')
    expr = expr.replace('(', '( ').replace('  ', ' ')
    expr = expr.replace('(', ' (').replace('  ', ' ')
    expr = expr.replace(')', ') ').replace('  ', ' ')
    expr = expr.replace(')', ' )').replace('  ', ' ')
    expr = expr.lstrip().rstrip()

    try:
        return Num(int(expr))

    except:
        try:
            if expr[0] == '(' and expr[-1] == ')':
                token_ = []
                temp = ''
                concat = 0
                for s in expr[2:-1]:
                    if s == ' ' and concat <= 0:
                        token_.append(temp)
                        temp = ''
                    elif s == '(':
                        concat += 1
                        temp += '('
                    elif s == ')':
                        concat -= 1
                        temp += ')'
                    else:
                        temp = temp + s

                if len(token_) == 3 and token_[0] == '+':
                    return Add(parse(token_[1]), parse(token_[2]))
                elif len(token_) == 3 and token_[0] == '-':
                    return Sub(parse(token_[1]), parse(token_[2]))
                elif len(token_) == 3 and token_[0] == 'with' and len(parse(token_[1])) == 2:
                    return With(parse(token_[1])[0], parse(token_[1])[1], parse(token_[2]))
                elif len(token_) == 2:
                    return [token_[0], parse(token_[1])]

            if True: #need to set the condition
                return Id(expr)

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
