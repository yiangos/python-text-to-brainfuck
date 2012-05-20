class BFGenerator(object):
    """Takes a string and generates a brainfuck code that, when run,
       prints the original string to the brainfuck interpreter standard
       output"""
      
    def text2BF(self, data):
        """Converts a string into a BF program. Returns the BF code"""
        glyphs = len(set([c for c in data]))
        number_of_bins = max(max([ord(c) for c in data]) // glyphs,1)
        # Create an array that emulates the BF memory array as if the
        # code we are generating was being executed. Initialize the
        # array by creating as many elements as different glyphs in
        # the original string. Then each "bin" gets an initial value
        # which is determined by the actual message.
        # FIXME: I can see how this can become a problem for languages
        # that don't use a phonetic alphabet, such as Chinese.
        bins = [(i + 1) * number_of_bins for i in range(glyphs)]
        code="+" * number_of_bins + "["
        code+="".join([">"+("+"*(i+1)) for i in range(1,glyphs)])
        code+="<"*(glyphs-1) + "-]"
        code+="+" * number_of_bins
        # For each character in the original message, find the position
        # that holds the value closest to the character's ordinal, then
        # generate the BF code to move the memory pointer to that memory
        # position, get the value of that memory position to be equal
        # to the ordinal of the character and print it (i.e. print the
        # character).
        current_bin=0
        for char in data:
            new_bin=[abs(ord(char)-b)
                     for b in bins].index(min([abs(ord(char)-b)
                                               for b in bins]))
            appending_character=""
            if new_bin-current_bin>0:
                appending_character=">"
            else:
                appending_character="<"
            code+=appending_character * abs(new_bin-current_bin)
            if ord(char)-bins[new_bin]>0:
                appending_character="+"
            else:
                appending_character="-"
            code+=(appending_character * abs( ord(char)-bins[new_bin])) +"."
            current_bin=new_bin
            bins[new_bin]=ord(char)
        return code
    

if __name__=="__main__":
    bfg=BFGenerator()
    print(bfg.text2BF(input("Set text>")))
