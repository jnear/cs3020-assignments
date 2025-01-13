from ast import *
from typing import List, Set, Dict
from dataclasses import dataclass
import functools

binops = {
    '+': lambda a, b: a + b,
    'Eq': lambda a, b: a == b,
    'And': lambda a, b: a and b,
    'Or': lambda a, b: a or b,
    'Gt': lambda a, b: a > b,
    'Lt': lambda a, b: a < b,
    'GtE': lambda a, b: a >= b,
    'LtE': lambda a, b: a <= b,
    }

unops = {
    'Not': lambda a: not a
    }

@dataclass
class ClassDefVal:
    name: str
    fields: List[str]

@dataclass
class ObjectVal:
    name: str
    fields: Dict[str, any]

def eval_Lif(prog: Module) -> List[int]:
    def eval_stmts(stmts: List[stmt], env: Dict[str, any]) -> List[any]:
        outputs = []
        for stmt in stmts:
            match stmt:
                case ClassDef(name, _, _, [Pass()]):
                    env[name] = ClassDefVal(name, [])
                case ClassDef(name, _, _, body):
                    fields = [a.target.id for a in body]
                    env[name] = ClassDefVal(name, fields)
                case Assign([Name(x)], e):
                    env[x] = eval_e(e, env)
                case Expr(Call(Name('print'), [e])):
                    outputs.append(eval_e(e, env))
                case If(condition, then_stmts, else_stmts):
                    if eval_e(condition, env):
                        outputs += eval_stmts(then_stmts, env)
                    else:
                        outputs += eval_stmts(else_stmts, env)
                case While(test, body):
                    while eval_e(test, env):
                        outputs += eval_stmts(body, env)
                case _:
                    raise Exception('eval_stmts', dump(stmt))
        return outputs
        
    def eval_e(e: expr, env: Dict[str, any]) -> any:
        match e:
            case Attribute(e1, field):
                match eval_e(e1, env):
                    case ObjectVal(name, fields):
                        return fields[field]
                    case _:
                        raise Exception('eval_e', e)
            case Call(Name(fun_name), args):
                match env[fun_name]:
                    case ClassDefVal(name, fields):
                        return ObjectVal(name, {f: eval_e(a, env) for f, a in zip(fields, args)})
                    case _:
                        raise Exception('eval_e', e)
            case Constant(i):
                return i
            case Name(x):
                return env[x]
            case UnaryOp(op, e1):
                return unops[type(op).__name__](eval_e(e1, env))
            case BinOp(e1, Add(), e2):
                return eval_e(e1, env) + eval_e(e2, env)
            case BinOp(e1, Sub(), e2):
                return eval_e(e1, env) - eval_e(e2, env)
            case BinOp(e1, Mult(), e2):
                return eval_e(e1, env) * eval_e(e2, env)
            case Compare(e1, [op], [e2]):
                return binops[type(op).__name__](eval_e(e1, env), eval_e(e2, env))
            case BoolOp(op, args):
                vals = [eval_e(e, env) for e in args]
                return functools.reduce(binops[type(op).__name__], vals)
            case IfExp(test, then_e, else_e):
                if eval_e(test, env):
                    return eval_e(then_e, env)
                else:
                    return eval_e(else_e, env)
            case Tuple(args):
                return tuple([eval_e(a, env) for a in args])
            case Subscript(e1, e2):
                return eval_e(e1, env)[eval_e(e2, env)]
            case _:
                raise Exception('eval_e', dump(e))

    env = {}
    match prog:
        case Module(stmts):
            return eval_stmts(stmts, env)
        case _:
            raise Exception('eval_Lif', prog)
