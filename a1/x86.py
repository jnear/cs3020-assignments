# reg ::= rsp | rbp | rax | rbx | rcx | rdx | rsi | rdi |
# r8 | r9 | r10 | r11 | r12 | r13 | r14 | r15
# arg ::= $int | %reg | int(%reg)
# instr ::= addq arg,arg | subq arg,arg | negq arg | movq arg,arg |
# callq label | pushq arg | popq arg | retq | jmp label

from dataclasses import dataclass
from typing import List, Set, Dict, Tuple, Any
from cs3020_support.python import AST

# ==================================================
# Arguments
# ==================================================
@dataclass(frozen=True, eq=True)
class Arg(AST):
    pass

@dataclass(frozen=True, eq=True)
class Immediate(Arg):
    val: int

@dataclass(frozen=True, eq=True)
class Reg(Arg):
    val: str

# ==================================================
# Instructions
# ==================================================
@dataclass(frozen=True, eq=True)
class Instr(AST):
    pass

@dataclass(frozen=True, eq=True)
class Movq(Instr):
    a1: Arg
    a2: Arg

@dataclass(frozen=True, eq=True)
class Callq(Instr):
    label: str

@dataclass(frozen=True, eq=True)
class Retq(Instr):
    pass

# ==================================================
# Program
# ==================================================

@dataclass(frozen=True, eq=True)
class X86Program(AST):
    blocks: Dict[str, List[Instr]]
    stack_space: int = None

# ==================================================
# Utility Functions
# ==================================================

def print_x86(program: X86Program) -> str:
    """
    Prints an x86 program to a string.
    :param program: An x86 program.
    :return: A string, ready for gcc.
    """

    def print_arg(a: Arg) -> str:
        match a:
            case Immediate(i):
                return f'${i}'
            case Reg(r):
                return f'%{r}'
            case _:
                raise Exception('print_arg', a)

    def print_instr(e: Instr) -> str:
        match e:
            case Movq(a1, a2):
                return f'movq {print_arg(a1)}, {print_arg(a2)}'
            case Callq(label):
                return f'callq {label}'
            case Retq():
                return f'retq'
            case _:
                raise Exception('print_instr', e)

    def print_block(label: str, instrs: List[Instr]) -> str:
        name = f'{label}:\n'
        instr_strs = '\n'.join(['  ' + print_instr(i) for i in instrs])
        return name + instr_strs

    blocks = program.blocks
    block_instrs = '\n'.join([print_block(label, block) for label, block in blocks.items()])

    program = "  .globl main\n" + block_instrs + "\n"
    return program
