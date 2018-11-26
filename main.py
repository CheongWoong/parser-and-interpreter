import argparse

import AE
import WAE
import FWAE
import FAE
import RCFAE
import RBMRCFAE

parser = {'AE':AE.parse, 'WAE':WAE.parse, 'FWAE':FWAE.parse, 'FAE':FAE.parse,
              'RCFAE':RCFAE.parse, 'RBMRCFAE':RBMRCFAE.parse}
interpreter = {'AE':AE.interp, 'WAE':WAE.interp, 'FWAE':FWAE.interp, 'FAE':FAE.interp,
                   'RCFAE':RCFAE.interp, 'RBMRCFAE':RBMRCFAE.interp}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('expr', nargs='+', help='s-expression')
    parser.add_argument('-p', action='store_true', help='enable a parser only')
    parser.add_argument('-lang', type=str, default='AE', help='which language?')
    args = parser.parse_args()

    args.expr = ' '.join(args.expr)
    
    if args.p:
        print(parse(args.expr, args.lang.upper()))
    else:
        print(run(args.expr, args.lang.upper()))

def run(expr, lang):
    expr = parse(expr, lang)
    expr = interp(expr, lang)
    return expr

def parse(expr, lang):
    return parser[lang](expr)

def interp(expr, lang):
    return interpreter[lang](expr)
    
if __name__ == '__main__':
    main()

