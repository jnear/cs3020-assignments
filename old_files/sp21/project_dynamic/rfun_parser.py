from dataclasses import dataclass
from collections import OrderedDict
from typing import List, Set, Dict, Tuple
from cs3020_support.base_ast import AST, print_ast
from lark import Lark
from typed_rfun import *

##################################################
# Abstract Syntax Trees: Rvec
##################################################

@dataclass
class RfunExp(AST):
    pass

@dataclass
class Int(RfunExp):
    val: int

@dataclass
class Bool(RfunExp):
    val: bool

@dataclass
class Var(RfunExp):
    var: str

@dataclass
class Let(RfunExp):
    x: str
    e1: RfunExp
    body: RfunExp

@dataclass
class Prim(RfunExp):
    op: str
    args: List[RfunExp]

@dataclass
class If(RfunExp):
    e1: RfunExp
    e2: RfunExp
    e3: RfunExp

@dataclass
class Funcall(RfunExp):
    fun: RfunExp
    args: List[RfunExp]

@dataclass
class Lambda(RfunExp):
    args: List[str]
    body: RfunExp

@dataclass
class RfunDef(AST):
    name: str
    args: List[str]
    body: RfunExp

@dataclass
class RfunProgram(AST):
    defs: List[RfunDef]
    body: RfunExp


##################################################
# Concrete Syntax Parser
##################################################

_rfun_parser = Lark(r"""
    ?exp: NUMBER -> int_e
        | "True" -> true_e
        | "False" -> false_e
        | CNAME -> var_e
        | "let" CNAME "=" exp "in" exp -> let_e
        | "if" exp "then" exp "else" exp -> if_e
        | "-" exp -> neg_e
        | "not" exp -> not_e
        | exp "+" exp -> plus_e
        | exp _cmp exp -> cmp_e
        | "vectorRef" "(" exp "," exp ")" -> vector_ref_e
        | "vectorSet" "(" exp "," exp "," exp ")" -> vector_set_e
        | "vector" "(" exp ("," exp)* ")" -> vector_e
        | "lambda" "(" def_args ")" "->" exp -> lambda_e
        | funcall_e
        | "(" exp ")"

    !_cmp: "<"|">"|"=="|">="|"<="|"&&"|"||"

    funcall_e.-500: exp "(" (exp ("," exp)*)? ")"

    def_e: "def" CNAME "(" def_args ")" "=" "{" exp "}"
    def_args: (CNAME ("," CNAME)*)?

    prog: def_e* exp

    %import common.NUMBER
    %import common.CNAME

    %import common.WS
    %ignore WS
    """, start='prog', parser='lalr')


##################################################
# Pass #0: Parsing Concrete to Abstract Syntax
##################################################

def _parse(s: str) -> RfunProgram:
    def bprog(p) -> RfunProgram:
        assert p.data == 'prog'

        defs = [bdef(d) for d in p.children[:-1]]
        expr = bast(p.children[-1])

        return RfunProgram(defs, expr)

    def bdef(d):
        assert d.data == 'def_e'

        name, args, body = d.children
        assert args.data == 'def_args'
        
        return RfunDef(str(name),
                       [str(a) for a in args.children],
                       bast(body))

    def bast(e) -> RfunExp:
        if e.data == 'int_e':
            return Int(int(e.children[0]))
        if e.data == 'var_e':
            return Var(str(e.children[0]))
        elif e.data == 'plus_e':
            e1, e2 = e.children
            return Prim('+', [bast(e1), bast(e2)])
        elif e.data == 'neg_e':
            e1 = e.children[0]
            return Prim('neg', [bast(e1)])
        elif e.data == 'let_e':
            x, e1, body = e.children
            return Let(str(x), bast(e1), bast(body))
        elif e.data == 'if_e':
            e1, e2, e3 = e.children
            return If(bast(e1), bast(e2), bast(e3))
        elif e.data == 'cmp_e':
            e1, op, e2 = e.children
            return Prim(str(op), [bast(e1), bast(e2)])
        elif e.data == 'not_e':
            e1 = e.children[0]
            return Prim('not', [bast(e1)])
        elif e.data == 'true_e':
            return Bool(True)
        elif e.data == 'false_e':
            return Bool(False)
        elif e.data == 'vector_ref_e':
            e1, e2 = e.children
            return Prim('vectorRef', [bast(e1), bast(e2)])
        elif e.data == 'vector_set_e':
            e1, e2, e3 = e.children
            return Prim('vectorSet', [bast(e1), bast(e2), bast(e3)])
        elif e.data == 'vector_e':
            new_children = [bast(c) for c in e.children]
            return Prim('vector', new_children)
        elif e.data == 'funcall_e':
            new_children = [bast(c) for c in e.children]
            return Funcall(new_children[0], new_children[1:])
        elif e.data == 'lambda_e':
            args, body = e.children
            arg_names = [str(a) for a in args.children]

            return Lambda(arg_names, bast(body))
        else:
            raise Exception('parse', e)

    parsed = _rfun_parser.parse(s)
    program = bprog(parsed)
    return program

def parse_rfun(s: str) -> RfunProgram:
    return _parse(s)

