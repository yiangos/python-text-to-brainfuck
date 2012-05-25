from BFInterpreter import BFInterpreter as interpreter
from BFGenerator import BFGenerator as generator

bfg=generator()
bfi=interpreter()
original_string=input("Set text>")
bf_source=bfg.text_to_brainfuck(original_string)
print("Brainfuck source:",
      bf_source,
      "number of commands:",
      len(bf_source),
      sep='\n')
bf_output=bfi.execute(bf_source)
print("Brainfuck output:",
      bf_output,
      sep='\n')
if bf_output==original_string:
    print("SUCCESS!")
else:
    print("FAILURE!")
