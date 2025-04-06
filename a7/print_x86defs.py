from typing import Set, Dict, Tuple, List
import cs3020_support.x86 as x86

def print_x86_defs(program) -> str:
    """
    Prints an x86 program to a string.
    :param program: An x86 program.
    :return: A string, ready for gcc.
    """

    def print_arg(a: x86.Arg) -> str:
        match a:
            case x86.Immediate(i):
                return f'${i}'
            case x86.Reg(r):
                return f'%{r}'
            case x86.ByteReg(r):
                return f'%{r}'
            case x86.Var(x):
                return f'#{x}'
            case x86.Deref(register, offset):
                return f'{offset}(%{register})'
            case x86.GlobalVal(x):
                return f'{x}(%rip)'
            case _:
                raise Exception('print_arg', a)

    def print_instr(e: x86.Instr) -> str:
        match e:
            case x86.Addq(a1, a2):
                return f'addq {print_arg(a1)}, {print_arg(a2)}'
            case x86.Subq(a1, a2):
                return f'subq {print_arg(a1)}, {print_arg(a2)}'
            case x86.Imulq(a1, a2):
                return f'imulq {print_arg(a1)}, {print_arg(a2)}'
            case x86.Movq(a1, a2):
                return f'movq {print_arg(a1)}, {print_arg(a2)}'
            case x86.Movzbq(a1, a2):
                return f'movzbq {print_arg(a1)}, {print_arg(a2)}'
            case x86.Cmpq(a1, a2):
                return f'cmpq {print_arg(a1)}, {print_arg(a2)}'
            case x86.Andq(a1, a2):
                return f'andq {print_arg(a1)}, {print_arg(a2)}'
            case x86.Orq(a1, a2):
                return f'orq {print_arg(a1)}, {print_arg(a2)}'
            case x86.Xorq(a1, a2):
                return f'xorq {print_arg(a1)}, {print_arg(a2)}'
            case x86.Leaq(a1, a2):
                return f'leaq {print_arg(a1)}, {print_arg(a2)}'
            case x86.Pushq(a1):
                return f'pushq {print_arg(a1)}'
            case x86.Popq(a1):
                return f'popq {print_arg(a1)}'
            case x86.Callq(label):
                return f'callq {label}'
            case x86.IndirectCallq(a1, _):
                return f'callq *{print_arg(a1)}'
            case x86.Retq():
                return f'retq'
            case x86.Jmp(label):
                return f'jmp {label}'
            case x86.JmpIf(cc, label):
                return f'j{cc} {label}'
            case x86.Set(cc, a1):
                return f'set{cc} {print_arg(a1)}'
            case _:
                raise Exception('print_instr', e)

    def print_block(label: str, instrs: List[x86.Instr]) -> str:
        name = f'{label}:\n'
        instr_strs = '\n'.join(['  ' + print_instr(i) for i in instrs])
        return name + instr_strs

    def print_def(d):
        block_instrs = '\n'.join([print_block(label, block) for label, block in d.blocks.items()])
        return f'def {d.label}:\n' + block_instrs + '\n'

    def_str = '\n'.join([print_def(d) for d in program.defs])
    program = "  .globl main\n" + def_str + "\n"
    return program
