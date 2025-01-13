import ast
from ast import *

from dataclasses import dataclass
from collections import OrderedDict, defaultdict
from typing import List, Set, Dict, Tuple as TupleType, DefaultDict, Callable
import itertools
import sys
import traceback

from cs3020_support.base_ast import AST, print_ast

import cs3020_support.x86exp as x86
import cfun
import constants

gensym_num = 0

# Generates a new unique symbol
def gensym(x):
    global gensym_num
    gensym_num = gensym_num + 1
    return f'{x}_{gensym_num}'

# Returns the "simple" name of an object's type
def name_of(op):
    return type(op).__name__

# A "begin expression" for Python
# Runs the list of statements, then evaluates to the value of the expression
class Begin(expr):
    _fields = ['stmts', 'exp']
    __match_args__ = tuple(_fields)

    def __init__(self, stmts, exp):
        self.stmts = stmts
        self.exp = exp

# An "allocate expression" for Python
# allocates memory for Tuples
class Allocate(expr):
    _fields = ['num_bytes', 'tuple_type']
    __match_args__ = tuple(_fields)

    def __init__(self, num_bytes, tuple_type):
        self.num_bytes = num_bytes
        self.tuple_type = tuple_type

# A "global value expression" for Python
# references global values used by the compiler
class GlobalValue(expr):
    _fields = ['name']
    __match_args__ = tuple(_fields)

    def __init__(self, name):
        self.name = name

# A "collect statement" for Python
# runs the garbage collector
class Collect(expr):
    _fields = ['num_bytes']
    __match_args__ = tuple(_fields)

    def __init__(self, num_bytes):
        self.num_bytes = num_bytes

@dataclass
class FunctionType:
    args: List[type]
    output_type: type

# Assigns e the type t and returns e
def with_type(t, e):
    e.has_type = t
    return e

##################################################
# typecheck
##################################################

TEnv = Dict[str, type]

def typecheck(program: Module) -> Module:
    """
    Typechecks the input program; throws an error if the program is not well-typed.
    :param e: The Ltup program to typecheck
    :return: The program, if it is well-typed
    """

    prim_arg_types = {
        '+':   [int, int],
        'Not': [bool],
        'Or':  [bool, bool],
        'And':  [bool, bool],
        'Gt':   [int, int],
        'Gte':  [int, int],
        'Lt':   [int, int],
        'LtE':  [int, int],
    }

    prim_output_types = {
        '+':   int,
        'Not': bool,
        'Or':  bool,
        'And':  bool,
        'Gt':   bool,
        'Gte':  bool,
        'Lt':   bool,
        'LtE':  bool,
    }


    pass


##################################################
# remove-complex-opera*
##################################################

def rco(prog: Module) -> Module:
    """
    Removes complex operands. After this pass, the arguments to operators (unary and binary
    operators, and function calls like "print") will be atomic.
    :param prog: An Lvar program
    :return: An Lvar program with atomic operator arguments.
    """

    pass


##################################################
# expose-allocation
##################################################

def expose_alloc(prog: Module) -> Module:
    """
    Exposes allocations in an Ltup program. Replaces Tuple(...) with explicit
    allocation.
    :param prog: An Ltup program
    :return: An Ltup program, without Tuple constructors
    """

    pass


##################################################
# explicate-control
##################################################

def explicate_control(prog: Module) -> cfun.CProgram:
    """
    Transforms an Ltup Expression into a Cfun program.
    :param e: An Ltup Expression
    :return: A Cfun Program
    """

    pass


##################################################
# select-instructions
##################################################

def select_instructions(p: cfun.CProgram) -> x86.Program:
    """
    Transforms a Cfun program into a pseudo-x86 assembly program.
    :param p: a Cfun program
    :return: a pseudo-x86 program
    """

    pass


##################################################
# uncover-live
##################################################

def uncover_live(defs: Dict[str, x86.Program]) -> \
  Dict[str, TupleType[x86.Program, Dict[str, List[Set[x86.Var]]]]]:
    return {fun_name: uncover_live_(prog) for fun_name, prog in defs.items()}
        

def uncover_live_(program: x86.Program) -> TupleType[x86.Program, Dict[str, List[Set[x86.Var]]]]:
    """
    Performs liveness analysis. Returns the input program, plus live-after sets
    for its blocks.
    :param program: a pseudo-x86 assembly program
    :return: A tuple. The first element is the same as the input program. The
    second element is a dict of live-after sets. This dict maps each label in
    the program to a list of live-after sets for that label. The live-after
    sets are in the same order as the label's instructions.
    """

    pass


##################################################
# build-interference
##################################################

class InterferenceGraph:
    """
    A class to represent an interference graph: an undirected graph where nodes
    are x86.Arg objects and an edge between two nodes indicates that the two
    nodes cannot share the same locations.
    """
    graph: DefaultDict[x86.Arg, Set[x86.Arg]]

    def __init__(self):
        self.graph = defaultdict(lambda: set())

    def add_edge(self, a: x86.Arg, b: x86.Arg):
        if a != b:
            self.graph[a].add(b)
            self.graph[b].add(a)

    def neighbors(self, a: x86.Arg) -> Set[x86.Arg]:
        if a in self.graph:
            return self.graph[a]
        else:
            return set()

    def __str__(self):
        pairs = set()
        for k in self.graph.keys():
            new_pairs = set((k, v) for v in self.graph[k])
            pairs = pairs.union(new_pairs)

        for a, b in list(pairs):
            if (b, a) in pairs:
                pairs.remove((a, b))

        strings = [print_ast(a) + ' -- ' + print_ast(b) for a, b in pairs]
        return 'InterferenceGraph{\n ' + ',\n '.join(strings) + '\n}'


def build_interference(defs: Dict[str, TupleType[x86.Program, Dict[str, List[Set[x86.Var]]]]]) -> \
        Dict[str, TupleType[x86.Program, InterferenceGraph]]:
    return {fun_name: build_interference_(prog) for fun_name, prog in defs.items()}

def build_interference_(inputs: TupleType[x86.Program, Dict[str, List[Set[x86.Var]]]]) -> \
        TupleType[x86.Program, InterferenceGraph]:
    """
    Build the interference graph.
    :param inputs: A Tuple. The first element is a pseudo-x86 program. The
    second element is the dict of live-after sets produced by the uncover-live
    pass.
    :return: A Tuple. The first element is the same as the input program. The
    second is a completed interference graph.
    """

    pass


##################################################
# allocate-registers
##################################################

Color = int
Coloring = Dict[x86.Var, Color]
Saturation = Set[Color]

def allocate_registers(defs: Dict[str, TupleType[x86.Program, InterferenceGraph]]) -> \
        Dict[str, TupleType[x86.Program, int, int]]:
    return {fun_name: allocate_registers_(prog) for fun_name, prog in defs.items()}

def allocate_registers_(inputs: TupleType[x86.Program, InterferenceGraph]) -> \
        TupleType[x86.Program, int]:
    """
    Assigns homes to variables in the input program. Allocates registers and
    stack locations as needed, based on a graph-coloring register allocation
    algorithm.
    :param inputs: A Tuple. The first element is the pseudo-x86 program. The
    second element is the completed interference graph.
    :return: A Tuple. The first element is an x86 program (with no variable
    references). The second element is the number of bytes needed in stack
    locations.
    """

    # Defines the set of registers to use
    register_locations = [x86.Reg(r) for r in
                          constants.caller_saved_registers + constants.callee_saved_registers]

    pass


##################################################
# patch-instructions
##################################################

def patch_instructions(defs: Dict[str, TupleType[x86.Program, int, int]]) -> \
  Dict[str, TupleType[x86.Program, int, int]]:
    return {fun_name: patch_instructions_(prog) for fun_name, prog in defs.items()}

def patch_instructions_(inputs: TupleType[x86.Program, int, int]) -> TupleType[x86.Program, int, int]:
    """
    Patches instructions with two memory location inputs, using %rax as a temporary location.
    :param inputs: A Tuple. The first element is an x86 program. The second element is the
    stack space in bytes.
    :return: A Tuple. The first element is the patched x86 program. The second element is
    the stack space in bytes.
    """

    pass


##################################################
# print-x86
##################################################

def print_x86(defs: Dict[str, TupleType[x86.Program, int, int]]) -> str:
    output = ""
    for name, stuff in defs.items():
        output += print_x86_(stuff, name)
    return output

def print_x86_(inputs: TupleType[x86.Program, int, int], def_name: str) -> str:
    """
    Prints an x86 program to a string.
    :param inputs: A Tuple. The first element is the x86 program. The second element
    is the stack space in bytes.
    :return: A string, ready for gcc.
    """

    pass


##################################################
# Compiler definition
##################################################

compiler_passes = {
    'typecheck': typecheck,
    'remove complex opera*': rco,
    'expose allocation': expose_alloc,
    'explicate control': explicate_control,
    'select instructions': select_instructions,
    'uncover live': uncover_live,
    'build interference': build_interference,
    'allocate registers': allocate_registers,
    'patch instructions': patch_instructions,
    'print x86': print_x86
}


def run_compiler(s, logging=False):
    current_program = parse(s)

    if logging == True:
        print()
        print('==================================================')
        print(' Input program')
        print('==================================================')
        print()
        print(print_ast(current_program))

    for pass_name, pass_fn in compiler_passes.items():
        current_program = pass_fn(current_program)

        if logging == True:
            print()
            print('==================================================')
            print(f' Output of pass: {pass_name}')
            print('==================================================')
            print()
            print(print_ast(current_program))

    return current_program


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Usage: python compiler.py <source filename>')
    else:
        file_name = sys.argv[1]
        with open(file_name) as f:
            print(f'Compiling program {file_name}...')

            try:
                program = f.read()
                x86_program = run_compiler(program, logging=True)

                with open(file_name + '.s', 'w') as output_file:
                    output_file.write(x86_program)

            except:
                print('Error during compilation! **************************************************')
                traceback.print_exception(*sys.exc_info())

