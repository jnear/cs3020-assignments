# reg ::= rsp | rbp | rax | rbx | rcx | rdx | rsi | rdi |
# r8 | r9 | r10 | r11 | r12 | r13 | r14 | r15
# arg ::= $int | %reg | int(%reg)
# instr ::= addq arg,arg | subq arg,arg | negq arg | movq arg,arg |
# callq label | pushq arg | popq arg | retq | jmp label

from dataclasses import dataclass
from typing import List, Set, Dict, Tuple, Any
from .python import AST

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

@dataclass(frozen=True, eq=True)
class ByteReg(Arg):
    val: str

@dataclass(frozen=True, eq=True)
class Var(Arg):
    var: str

@dataclass(frozen=True, eq=True)
class VecVar(Var):
    var: str

@dataclass(frozen=True, eq=True)
class GlobalVal(Arg):
    val: str

@dataclass(frozen=True, eq=True)
class FunRef(Arg):
    label: str

@dataclass(frozen=True, eq=True)
class Deref(Arg):
    reg: str
    offset: int

# ==================================================
# Instructions
# ==================================================
@dataclass(frozen=True, eq=True)
class Instr(AST):
    pass

@dataclass(frozen=True, eq=True)
class Addq(Instr):
    a1: Arg
    a2: Arg

@dataclass(frozen=True, eq=True)
class Subq(Instr):
    a1: Arg
    a2: Arg

@dataclass(frozen=True, eq=True)
class Imulq(Instr):
    a1: Arg
    a2: Arg

@dataclass(frozen=True, eq=True)
class Movq(Instr):
    a1: Arg
    a2: Arg

@dataclass(frozen=True, eq=True)
class Movzbq(Instr):
    a1: Arg
    a2: Arg

@dataclass(frozen=True, eq=True)
class Cmpq(Instr):
    a1: Arg
    a2: Arg

@dataclass(frozen=True, eq=True)
class Andq(Instr):
    a1: Arg
    a2: Arg

@dataclass(frozen=True, eq=True)
class Orq(Instr):
    a1: Arg
    a2: Arg

@dataclass(frozen=True, eq=True)
class Xorq(Instr):
    a1: Arg
    a2: Arg

@dataclass(frozen=True, eq=True)
class Leaq(Instr):
    a1: Arg
    a2: Arg

@dataclass(frozen=True, eq=True)
class Pushq(Instr):
    a1: Arg

@dataclass(frozen=True, eq=True)
class Popq(Instr):
    a1: Arg

@dataclass(frozen=True, eq=True)
class Callq(Instr):
    label: str

@dataclass(frozen=True, eq=True)
class IndirectCallq(Instr):
    e1: Arg
    num_args: int

@dataclass(frozen=True, eq=True)
class TailJmp(Instr):
    e1: Arg
    num_args: int

@dataclass(frozen=True, eq=True)
class Jmp(Instr):
    label: str

@dataclass(frozen=True, eq=True)
class JmpIf(Instr):
    cc: str
    label: str

@dataclass(frozen=True, eq=True)
class Set(Instr):
    cc: str
    e1: Arg

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
            case ByteReg(r):
                return f'%{r}'
            case Var(x):
                return f'#{x}'
            case Deref(register, offset):
                return f'{offset}(%{register})'
            case GlobalVal(x):
                return f'{x}(%rip)'
            case _:
                raise Exception('print_arg', a)

    def print_instr(e: Instr) -> str:
        match e:
            case Addq(a1, a2):
                return f'addq {print_arg(a1)}, {print_arg(a2)}'
            case Subq(a1, a2):
                return f'subq {print_arg(a1)}, {print_arg(a2)}'
            case Imulq(a1, a2):
                return f'imulq {print_arg(a1)}, {print_arg(a2)}'
            case Movq(a1, a2):
                return f'movq {print_arg(a1)}, {print_arg(a2)}'
            case Movzbq(a1, a2):
                return f'movzbq {print_arg(a1)}, {print_arg(a2)}'
            case Cmpq(a1, a2):
                return f'cmpq {print_arg(a1)}, {print_arg(a2)}'
            case Andq(a1, a2):
                return f'andq {print_arg(a1)}, {print_arg(a2)}'
            case Orq(a1, a2):
                return f'orq {print_arg(a1)}, {print_arg(a2)}'
            case Xorq(a1, a2):
                return f'xorq {print_arg(a1)}, {print_arg(a2)}'
            case Leaq(a1, a2):
                return f'leaq {print_arg(a1)}, {print_arg(a2)}'
            case Pushq(a1):
                return f'pushq {print_arg(a1)}'
            case Popq(a1):
                return f'popq {print_arg(a1)}'
            case Callq(label):
                return f'callq {label}'
            case IndirectCallq(a1, _):
                return f'callq *{print_arg(a1)}'
            case Retq():
                return f'retq'
            case Jmp(label):
                return f'jmp {label}'
            case JmpIf(cc, label):
                return f'j{cc} {label}'
            case Set(cc, a1):
                return f'set{cc} {print_arg(a1)}'
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
