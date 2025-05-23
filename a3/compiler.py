from typing import List, Set, Dict, Tuple
import sys
import itertools
import traceback

from cs3020_support.python import *
import x86

import constants
from interference_graph import InterferenceGraph

# Input Language: LVar
# op ::= "add"
# Expr ::= Var(x) | Constant(n) | Prim(op, [Expr])
# Stmt ::= Assign(x, Expr) | Print(Expr)
# LVar ::= Program([Stmt])

gensym_num = 0
global_logging = False

def log(label, value):
    if global_logging:
        print()
        print(f'--------------------------------------------------')
        print(f'Logging: {label}')
        print(value)
        print(f'--------------------------------------------------')

def log_ast(label, value):
    log(label, print_ast(value))

def gensym(x):
    """
    Constructs a new variable name guaranteed to be unique.
    :param x: A "base" variable name (e.g. "x")
    :return: A unique variable name (e.g. "x_1")
    """

    global gensym_num
    gensym_num = gensym_num + 1
    return f'{x}_{gensym_num}'


##################################################
# remove-complex-opera*
##################################################
# Input Language: LVar
# op ::= "add"
# Expr ::= Var(x) | Constant(n) | Prim(op, [Expr])
# Stmt ::= Assign(x, Expr) | Print(Expr)
# LVar ::= Program([Stmt])

def rco(prog: Program) -> Program:
    """
    Removes complex operands. After this pass, the arguments to operators (unary and binary
    operators, and function calls like "print") will be atomic.
    :param prog: An Lvar program
    :return: An Lvar program with atomic operator arguments.
    """

    pass


##################################################
# select-instructions
##################################################
# Input Language: LVar (all expressions are atomic)
# op ::= "add"
# Expr ::= Var(x) | Constant(n) | Prim(op, [Expr])
# Stmt ::= Assign(x, Expr) | Print(Expr)
# LVar ::= Program([Stmt])

# Output language: pseudo-x86
# Arg ::= Immediate(n) | Var(x) | Reg(str) | Deref(r, offset)
# Instr ::= Movq(Arg, Arg) | Addq(Arg, Arg) | Callq(str) | Retq()
# X86 ::= X86Program(Dict[str, [Instr]])

def select_instructions(prog: Program) -> x86.X86Program:
    """
    Transforms a Lvar program into a pseudo-x86 assembly program.
    :param prog: a Lvar program
    :return: a pseudo-x86 program
    """

    pass


##################################################
# allocate-registers
##################################################
# Input language: pseudo-x86
# Arg ::= Immediate(n) | Var(x) | Reg(str) | Deref(r, offset)
# Instr ::= Movq(Arg, Arg) | Addq(Arg, Arg) | Callq(str) | Retq()
# X86 ::= X86Program(Dict[str, [Instr]])

# Output language: pseudo-x86 (without variables)
# Arg ::= Immediate(n) | Reg(str) | Deref(r, offset)
# Instr ::= Movq(Arg, Arg) | Addq(Arg, Arg) | Callq(str) | Retq()
# X86 ::= X86Program(Dict[str, [Instr]])

Color = int
Coloring = Dict[str, Color]
Saturation = Set[Color]

def allocate_registers(program: x86.X86Program) -> x86.X86Program:
    """
    Assigns homes to variables in the input program. Allocates registers and
    stack locations as needed, based on a graph-coloring register allocation
    algorithm.
    :param program: A pseudo-x86 program.
    :return: An x86 program, annotated with the number of bytes needed in stack
    locations.
    """

    blocks = program.blocks
    live_after_sets = {}
    homes: Dict[str, x86.Arg] = {}

    pass


##################################################
# patch-instructions
##################################################
# Input/output language: pseudo-x86 (without variables)
# Arg ::= Immediate(n) | Reg(str) | Deref(r, offset)
# Instr ::= Movq(Arg, Arg) | Addq(Arg, Arg) | Callq(str) | Retq()
# X86 ::= X86Program(Dict[str, [Instr]])

def patch_instructions(program: x86.X86Program) -> x86.X86Program:
    """
    Patches instructions with two memory location inputs, using %rax as a temporary location.
    :param program: An x86 program.
    :return: A patched x86 program.
    """

    pass


##################################################
# prelude-and-conclusion
##################################################
# Input/output language: pseudo-x86 (without variables)
# Arg ::= Immediate(n) | Reg(str) | Deref(r, offset)
# Instr ::= Movq(Arg, Arg) | Addq(Arg, Arg) | Callq(str) | Retq()
# X86 ::= X86Program(Dict[str, [Instr]])

def prelude_and_conclusion(program: x86.X86Program) -> x86.X86Program:
    """
    Adds the prelude and conclusion for the program.
    :param program: An x86 program.
    :return: An x86 program, with prelude and conclusion.
    """

    pass


##################################################
# Compiler definition
##################################################

compiler_passes = {
    'remove complex opera*': rco,
    'select instructions': select_instructions,
    'allocate registers': allocate_registers,
    'patch instructions': patch_instructions,
    'prelude & conclusion': prelude_and_conclusion,
    'print x86': x86.print_x86
}


def run_compiler(s, logging=False):
    global global_logging
    global_logging = logging

    def print_prog(current_program):
        print('Concrete syntax:')
        if isinstance(current_program, x86.X86Program):
            print(x86.print_x86(current_program))
        elif isinstance(current_program, Program):
            print(print_program(current_program))

        print()
        print('Abstract syntax:')
        print(print_ast(current_program))

    current_program = parse(s)

    if logging == True:
        print()
        print('==================================================')
        print(' Input program')
        print('==================================================')
        print()
        print_prog(current_program)

    for pass_name, pass_fn in compiler_passes.items():
        current_program = pass_fn(current_program)

        if logging == True:
            print()
            print('==================================================')
            print(f' Output of pass: {pass_name}')
            print('==================================================')
            print()
            print_prog(current_program)

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
