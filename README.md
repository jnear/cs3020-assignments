# CS 3020 Assignment Code and Support

We will be implementing our compilers in Python. This repository
contains the support code and assignment scaffolding you will need.

## Installing Conda and Jupyter Notebook

We will be writing Python code for assignments in regular files, and
completing exercises in Jupyter notebooks. To set up a Python
installation that supports Jupyter notebooks. I recommend using Conda.
Please [click
here](https://github.com/jnear/cs211-data-privacy/blob/master/jupyter.md)
for information on installing Conda and setting up Jupyter notebooks.

## Creating the CS 3020 Environment

Python version 3.10 is required for CS 3020 (to support pattern
matching). I recommend creating a fresh Conda environment for CS 3020,
to ensure you have the right version of Python and the appropriate
libraries. You can create the environment as follows:

1. Open a terminal with Conda support. On Windows, launch "Anaconda
   Prompt"; on Linux or MacOS, launch a regular terminal.
2. To create the environment, type: `conda create -n cs3020 python=3.10`
3. To activate the environment, type `conda activate cs3020`. The
   prompt's prefix should change from `(base)` to `(cs3020)`.

## Installing the Support Code

You can install the support code for CS 3020 using `pip`:

1. Open a terminal with Conda support (as above)
2. Activate the Conda env: `conda activate cs3020`
3. Install the code: `pip install git+https://github.com/jnear/cs3020-assignments.git`

## Downloading the Assignment Code

This repository contains the assignment code and in-class exercises.
You need to download the files in this repository to your computer in
order to complete the assignments. 

**Option 1: clone the repository**

1. Open a terminal
2. Navigate to the directory that should hold your copy of the repo (e.g. `cd Downloads`)
3. Type `git clone https://github.com/jnear/cs3020-assignments.git`

To update your copy of the repo with new files, navigate to the repo
on your computer and type `git pull`.

**Option 2: download a zip file**

1. Click the green "code" button at the top of this page
2. Select "download zip" from the box that pops up
3. Extract the zip file somewhere on your computer

## Starting Jupyter Notebook

1. Open a terminal (MacOS or Linux) or the Anaconda Prompt (Windows)
2. Navigate to the `cs3020-assignments` directory
3. Activate the CS 3020 environment by typing `conda activate cs3020`
4. Start Jupyter notebook by typing `jupyter notebook`

If you get a "command not found" error, try installing Jupyter by
typing `pip install jupyter`, then try the steps above again.

## Installing and Using PyCharm

I recommend using the PyCharm "community edition" to edit your
assignment code code. PyCharm supports Python 3's static type hints,
and can help you avoid difficult-to-debug errors when implementing
your compiler. You can find information on downloading and installing
it [at this
link](https://www.jetbrains.com/pycharm/download/other.html). Make
sure you download the **Community Edition** (the non-paid version).

You can set up PyCharm to work with your Conda environment as follows:

1. Click the "open" button in PyCharm to open a project
2. Select the `cs3020-assignments` directory you created using the
   steps "Downloading the Assignment Code" above. If you're asked to
   create a virtual env, click "cancel."
3. Open Settings (File -> Settings, or PyCharm -> Preferences on MacOS)
4. Open the "Project: cs3020-assignments" -> "Python Interpreter"
   section of the settings
5. Click the "Python Interpreter" drop-down box, and click "Show All"
6. On the left side, click the plus icon (+) to add an interpreter.
7. On the left side, select "Conda Environment"
8. In the "Conda Executable" box, insert the path to the `conda`
   executable on your computer (if it's not already there).
9. Click the "Use Existing Environment" option
10. In the "Use Existing Environment" drop-down, pick the cs3020
   environment that you created earlier
11. Click "OK" three times
   
## Running the Compiler & Tests

To compile a program into an assembly file, navigate to the directory
containing the compiler implementation and run `compile.py`. For example:

```
cd a1/
python compiler.py tests/test1.py
```

will produce the file `tests/test1.py.s`.

To run all of the tests, navigate to the directory containing the
compiler implementation and run `run_tests.py`. For example:

```
cd a1/
python run_tests.py
```

This process allows you to quickly verify that all of the test cases
pass, but does not print out the output of each compiler pass.

You can run (or debug) the compiler in PyCharm by creating a run
configuration with `compiler.py` as the target and the filename of a
test as the command-line argument. You can run the tests by creating a
configuration with `run_tests.py` as the target.

## Online Compiler Diff Checker
This script will display the diffs of your compiler compared to the online compiler. By default it checks the prelude and conclusion pass but you can
specify a pass the check. 

You may need to pip install a few packages if any of the imports are unrecognized when running the script. Use `pip install [name of package]`.

Run `python verify.py --help` for specific usage

Verify all tests in the `a2/tests` dir with the `a2` compiler
```
python verify.py a2/tests/ a2`
```

Verify the assign homes pass of the `a2/tests/test1.py` file with the `a2` compiler
```
python verify.py a2/tests/test1.py a2 -v ah
```

Verify all tests in the `a2/tests` dir with the `a2` online compiler and your local `a1` compiler
```
python verify.py a2/tests/ a2 -l a1
```

Use the `-d` flag to show the strings that were extracted from both compilers. If the local compiler string is not an AST, there is probably an issue
with your compiler. Run your compiler on a test case like `python compiler.py tests/test1.py` to determine what the error is.

## Assignment Submission

This repository contains the skeleton of each assignment's
solution. The only file you will need to change is `compiler.py`. When
you submit your assignment solution on Blackboard, you should upload
*only* the `compiler.py` file. Please do not change any other files; I
won't have access to changes you make to other files when grading your
assignments.

## Useful Tips

To install the CS 3020 support code *inside* a Jupyter notebook, put the
following code in a cell and run it:

```
!pip install git+https://github.com/jnear/cs3020-assignments
```

If you try to run `jupyter notebook` in your Conda environment, and
get a command not found error, try:

```
pip install jupyter
```

If you try the above, and get a command not found error for `pip`,
try:

```
conda install pip
```

and then try installing Jupyter again.

## FAQs on Completing Assignments

#### What is the point of this pass? What is it trying to do?
- Look at the relevant section in the textbook; the first sentence or paragraph describes the goal of the pass and often why it's needed
- Look at the relevant section in the most recent exercise; the first note or first few questions often describes the point of the pass and its high level idea

#### How do I get started on a pass?
- Build the structure of the pass *without thinking*
  - Look at the grammar for the input to the pass
    - Create a nested function for each production rule (the left-hand side of ::=)
    - Create a match statement inside each nested function
    - Create a match case for each case of that production rule in the grammar (the right-hand side of ::=)
  - Most exercise sections describing a pass will include a final question of the form "describe the pass in the compiler" whose answer gives an overview for the implementation strategy of the pass
    - Copy and paste these instructions into your code as comments
    - Follow the comments as you implement the function

#### How do I fill in the implementation of the pass?
- Fill in the structure by thinking
  - Consult the textbook
  - Consult the exercises and your notes
  - Try an example in the online compiler
  - Try an example on paper
  - Re-do the relevant exercise questions

## Installing Python with Homebrew (Optional, Mac-only)

Homebrew is an open source package manager for MacOS. To install homebrew run their installation command on your terminal. You can find 
the command on their [website](https://brew.sh/)

Once you have homebrew to installed, you can install any version of python using their CLI. In this case I am installing version 3.10 other 
versions are also supported, you can find more information in the [python formulae](https://docs.brew.sh/Homebrew-and-Python)

```bash
brew install python@3.10
```

## Building the Runtime (Optional)

We will test our x86 assembly code using both an emulator and direct
execution on your hardware. To assemble your code into a binary,
you'll need a runtime system. The runtime is implemented in C, in the
file `runtime.c`. You can compile the runtime into an object file
(`runtime.o`) as follows:

```
gcc -c -g -std=c99 runtime.c
```

This will produce a file named `runtime.o`. The -g flag is to tell the
compiler to produce debug information that you may need to use the gdb
(or lldb) debugger.

Next, suppose your compiler has produced the x86 assembly program file
`foo.s` (the `.s` filename extension is the standard one for assembly
programs). To produce an executable program, you can then run:

```
gcc -g runtime.o foo.s
```

which will produce the executable program named `a.out` by linking
your program with the runtime.

To run a compiled program, first use GCC to assemble it into a
binary, then run the resulting binary (which will be called `a.out`):

```
gcc -g ../runtime.o tests/test1.py.s
./a.out
```

The process above runs a single program and allows you to view its
output.
