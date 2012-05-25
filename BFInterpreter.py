from io import StringIO as StringIO
from SparseMatrix import SparseMatrix as SparseMatrix

class BFInterpreter(object):
    """Takes a brainfuck code, parses it, executes it and returns
       the brainfuck standard output results as a string."""
    
    tokens="[]<>,.+-"
    grammar={}
    MAX_MEMORY_SLOTS=30000

    def __init__(self):
        self.loopcount=0
        self.code_tree=[]
        self.program_pointer=0
        self.memory=SparseMatrix()
        self.memory_pointer=0
        self.output=StringIO()
        self.grammar={
            ">":self.move_forward,
            "<":self.move_back,
            ",":self.take_input,
            ".":self.print_output,
            "+":self.increase_value,
            "-":self.decrease_value,
            "[":self.start_loop,
            "]":self.end_loop
        }
        
    def normalize(self, source):
        """Takes out all non-brainfuck characters and returns the
           stripped down source code"""
        return "".join([c for c in source if c in self.tokens])

    def reset(self):
        """Resets the interpreter internal state"""
        self.loopcount=0
        self.code_tree=[]
        self.program_pointer=0
        self.memory=SparseMatrix()
        self.memory_pointer=0
         
        
    def tokenize(self, source, position, container_tree):
        """Recursively converts the source code into a parsable tree of
           instructions, where each branch represents a while loop.
           Returns the tree (does not store it in internal state)."""
        source=self.normalize(source)
        self.program_pointer=position
        while self.program_pointer<len(source):
            char=source[self.program_pointer]
            self.program_pointer+=1
            if char in self.tokens[2:]:
                container_tree.append((char, None))
            elif char=="[":
                self.loopcount+=1
                container_tree.append((char,
                                      self.tokenize(source,
                                                    self.program_pointer,
                                                    [])))
            elif char=="]":
                if self.loopcount==0:
                    raise Exception("Loop mismatch. More closing than opening")
                self.loopcount-=1
                container_tree.append((char, None))
                return container_tree
        if self.loopcount!=0:
            raise Exception("Loop mismatch. More opening than closing")
        return container_tree

    def execute(self, source):
        """Executes a BF program"""
        self.reset()
        self.tokenize(source,0,self.code_tree)
        self.execute_statements(self.code_tree)
        output=self.output.getvalue()
        self.output.close()
        return output

    def execute_statements(self, tree):
        """Recursively executes all statements saved in the
           interpreter internal state"""
        for statement in tree:
            if statement[1]==None:
                self.grammar[statement[0]]()
            else:
                while self.memory[self.memory_pointer]!=0:
                    self.execute_statements(statement[1])

    def move_forward(self):
        """Instructions for the ">" BF token"""
        if self.memory_pointer>=self.MAX_MEMORY_SLOTS:
            raise RuntimeError("memory pointer overflow")
        self.memory_pointer+=1

    def move_back(self):
        """Instructions for the "<" BF token"""
        if self.memory_pointer==0:
            raise RuntimeError("Cannot move to negative memory index")
        self.memory_pointer-=1

    def increase_value(self):
        """Instructions for the "+" BF token"""
        self.memory[self.memory_pointer]+=1

    def decrease_value(self):
        """Instructions for the "-" BF token"""
        self.memory[self.memory_pointer]-=1

    def take_input(self):
        """Instructions for the "," BF token"""
        self.memory[self.memory_pointer]=ord(input())

    def print_output(self):
        """Instructions for the "." BF token"""
        self.output.write(chr(self.memory[self.memory_pointer]))

    def start_loop(self):
        """Instructions for the "[" BF token"""
        pass

    def end_loop(self):
        """Instructions for the "]" BF token"""
        pass

if __name__=="__main__":
    sample_source="""
        driver BF program that prints "hello World!"
        Taken from wikipedia
        +++++ +++++             initialize counter (cell #0) to 10
        [                       use loop to set the next
                                four cells to 70/100/30/10
            > +++++ ++          add  7 to cell #1
            > +++++ +++++       add 10 to cell #2 
            > +++               add  3 to cell #3
            > +                 add  1 to cell #4
            <<<< -              decrement counter (cell #0)
        ]                   
        > ++ .                  print 'H'
        > + .                   print 'e'
        +++++ ++ .              print 'l'
        .                       print 'l'
        +++ .                   print 'o'
        > ++ .                  print ' '
        << +++++ +++++ +++++ .  print 'W'
        > .                     print 'o'
        +++ .                   print 'r'
        ----- - .               print 'l'
        ----- --- .             print 'd'
        > + .                   print '!'
        > .                     print '\n'
    """
    parser=BFInterpreter()
    print(parser.execute(sample_source))
