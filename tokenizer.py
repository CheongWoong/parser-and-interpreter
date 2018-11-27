def tokenize(expr):
    expr = expr.replace('{', '(').replace('}', ')')
    expr = expr.replace('[', '(').replace(']', ')')
    expr = expr.replace('(', '( ').replace('  ', ' ')
    expr = expr.replace('(', ' (').replace('  ', ' ')
    expr = expr.replace(')', ') ').replace('  ', ' ')
    expr = expr.replace(')', ' )').replace('  ', ' ')
    expr = expr.lstrip().rstrip()

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
        return token_

    else:
        return None
