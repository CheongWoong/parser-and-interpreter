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
    parser.add_argument('sexp', nargs='+', help='s-expression')
    parser.add_argument('-p', action='store_true', help='enable a parser only')
    parser.add_argument('-lang', type=str, default='AE', help='which language?')
    args = parser.parse_args()

    args.sexp = ' '.join(args.sexp)
    
    if args.p:
        print(parse(args.sexp, args.lang.upper()))
    else:
        print(run(args.sexp, args.lang.upper()))

def run(sexp, lang):
    sexp = parse(sexp, lang)
    sexp = interp(sexp, lang)
    return sexp

def parse(sexp, lang):
    return parser[lang](sexp)

def interp(sexp, lang):
    return interpreter[lang](sexp)
    
if __name__ == '__main__':
    main()

