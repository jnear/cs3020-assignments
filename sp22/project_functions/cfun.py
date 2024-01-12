from dataclasses import dataclass
from typing import List, Set, Dict, Tuple
from cs3020_support.base_ast import AST

##################################################
@dataclass(eq=True)
class Atm(AST):
    pass

@dataclass(eq=True)
class ConstantInt(Atm):
    val: int

@dataclass(eq=True)
class ConstantBool(Atm):
    val: bool

@dataclass(eq=True)
class Name(Atm):
    var: str

@dataclass(eq=True)
class GlobalValue(Atm):
    var: str

@dataclass(eq=True)
class Subscript(Atm):
    var: str
    offset: int

##################################################
@dataclass(eq=True)
class Exp(AST):
    pass

@dataclass(eq=True)
class AtmExp(Exp):
    atm: Atm

@dataclass(eq=True)
class BinOp(Exp):
    e1: Exp
    op: any
    e2: Exp

@dataclass(eq=True)
class UnaryOp(Exp):
    op: any
    e1: Exp

@dataclass(eq=True)
class Compare(Exp):
    e1: Exp
    op: any
    e2: Exp

@dataclass(eq=True)
class Allocate(Exp):
    num_bytes: int
    tuple_type: any

@dataclass(eq=True)
class Call(Exp):
    fun_name: str
    args: List[Exp]

##################################################
@dataclass(eq=True)
class Stmt(AST):
    pass

@dataclass(eq=True)
class Print(Stmt):
    exp: Exp

@dataclass(eq=True)
class Collect(Stmt):
    num_bytes: int

@dataclass(eq=True)
class Assign(Stmt):
    var: str
    exp: Exp

@dataclass(eq=True)
class Return(Stmt):
    exp: Exp

@dataclass(eq=True)
class Goto(Stmt):
    label: str

@dataclass(eq=True)
class If(Stmt):
    test: Compare
    then_branch: Goto
    else_branch: Goto

##################################################
@dataclass(eq=True)
class CFunDef(AST):
    name: str
    args: List[str]
    blocks: Dict[str, List[Stmt]]

@dataclass(eq=True)
class CProgram(AST):
    defs: List[CFunDef]
