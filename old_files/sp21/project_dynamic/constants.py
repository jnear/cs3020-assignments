# Constants used in the compiler
# Caution: these may change during grading!

caller_saved_registers = ["rdx", "rcx", "rsi", "rdi", "r8", "r9", "r10"]
callee_saved_registers = ["rbx", "r12", "r13", "r14"]
parameter_passing_registers = ["rdi", "rsi", "rdx", "rcx", "r8", "r9"]

root_stack_size = 2**14
heap_size = 2**4
