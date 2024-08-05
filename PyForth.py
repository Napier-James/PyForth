import inspect
import time
class PyForth:
    def __init__(self):
        self.s , self.r , self.l = [] , [] , []
        self.words = {
            '.'      : lambda: print(f"{self.s.pop() if self.s else 'S is empty'} "),
            '+'      : lambda: self.s.append(self.s.pop() + self.s.pop()),
            '..'     : lambda: (print(f"l={self.l}\nr={self.r}\ns={self.s}")),
            '--'     : lambda: self.interpret('-1 +'),
            '++'     : lambda: self.interpret('1 +'),
            '>l'     : lambda: self.l.append(self.s.pop()),
            'l>'     : lambda: self.s.append(self.l.pop()),
            '>r'     : lambda: self.r.append(self.s.pop()),
            'r>'     : lambda: self.s.append(self.r.pop()),
            'abs'    : lambda: self.s.append(abs(self.s.pop())),
            'clear'  : lambda: (self.s.clear() , self.l.clear() , self.r.clear() , print("stacks emptied") ),
            'drop'   : lambda: self.s.pop(),
            'dup'    : lambda: self.interpret('-1 s'),
            'emit'   : lambda: print(f"{self.s.pop() if self.s else 'Stack is empty'}",end=""),
            'eval'   : lambda: self.s.append(eval(f"{self.s.pop()}")),
            'int'    : lambda: self.s.append(int(self.s.pop())),
            'False'  : lambda: self.interpret('0'),
            'float'  : lambda: self.s.append(float(self.s.pop())),
            'len'    : lambda: self.s.append(len(self.s.pop())),
            'logic'  : lambda: self.s.append(eval(f"int({self.s.pop()} {self.r.pop()} {self.s.pop()})")),
            'math'   : lambda: self.s.append(eval(f"{self.s.pop()} {self.r.pop()} {self.s.pop()}")),
            'max'    : lambda: self.s.append(max(self.s.pop(),self.s.pop())),
            'min'    : lambda: self.s.append(min(self.s.pop(),self.s.pop())),
            'negate' : lambda: self.interpret('-1 *'),
            'nip'    : lambda: self.interpret('>r drop r>'),
            'not'    : lambda: self.interpret('1 - abs'),
            'over'   : lambda: self.interpret('-2 s'),
            'roll'   : lambda: (self.interpret('>r'),self.s.append(self.s.pop(self.s.index(int(self.r[-1])))),self.r.pop()),
            'rot'    : lambda: self.interpret('swap >r swap r> swap'),
            's'      : lambda: self.s.append(self.s[int(self.s.pop())]), # aka pick
            'swap'   : lambda: self.interpret('-2 s >r >r drop r> r>'),
            'True'   : lambda: self.interpret('1'),
            'tuck'   : lambda: self.interpret('dup >r swap r>'),
        }
    def split_head_tail( self , tail , splitter ) :
        head = tail.replace("\n"," ").split(splitter,1)[0].strip()
        tail = tail[len(head)+1:].strip()
        return head,tail
    def interpret( self , tail ) :
        while tail:
            head,tail = self.split_head_tail(tail," ")
            if head in self.words:      # execute precompiled word
                self.words[head]()
            elif head in {"-","*","/","%","//","**"} :  # all but + to allow char + char in words
                self.r.append(head)
                self.words["math"]()    # math operator between two items
            elif head in {">","<","=",">=","<=","!=","&","|"} :
                self.r.append(head)
                self.words["logic"]()   # logic operator between two items
            elif head == ":" :          # add word - compile mode?
                key ,tail = self.split_head_tail(tail," ")
                mthd,tail = self.split_head_tail(tail,";")
                self.words[key] = lambda : self.interpret(mthd)
                tail = tail[2:]
            elif head == 'forget' :     # remove compiled word
                key,tail = self.split_head_tail(tail," ")
                self.words.pop(key)
            elif head == 'if' :         # conditional
                if self.s.pop() == 0  :    # 'if op' executes op when TOS is true
                    head,tail = self.split_head_tail(tail," ")
            elif head == 'iif' :        # immediate-if
                thenop,tail = self.split_head_tail(tail," ")
                elseop,tail = self.split_head_tail(tail," ")
                tail = ( thenop if self.s.pop() else elseop ) + ' ' + tail
            elif head == '."':          # printable text
                value,tail = self.split_head_tail(tail,'"')
                key  ,tail = self.split_head_tail(tail," ")
                self.words[key] = lambda : print(f"{value}")
            elif head == '"':           # quote to stack
                key,tail = self.split_head_tail(tail,'"')
                self.s.append(key)
            elif head == '(':           # ignore ( comment )
                head,tail = self.split_head_tail(tail,")")
                head,tail = self.split_head_tail(tail," ")
            elif head == '\\':          # ignore rest of line \ comment
                tail = ''
            elif head == 'see':         # show method for a word 
                key,tail = self.split_head_tail(tail," ")
                print(inspect.getsource(self.words[key]).strip())
            elif head == '@':           # store tos in existing variable on stack
                key,tail = self.split_head_tail(tail," ")
                self.words[key] = lambda value = self.s.pop() : self.s.append(value)
            else:
                try: isNumeric = float(head) ; self.s.append(int(float(head)) if int(float(head)) == float(head) else float(head))  # add to stack if numeric
                except ValueError:      # new word like variable n
                    self.words[head] = lambda value = self.s.pop() : self.s.append(value)
Forth = PyForth()                       # init
while (user_input := input()) != "end": Forth.interpret(user_input)
#while (user_input := input("type 'end' to exit: ")) != "end": Forth.interpret(user_input)


################################################################
### testing loop # : t --loop loop ; 5 t

## testing variable assigment and usage    
# 1 2 3 + * x x x * y y . ==> x,y = 5,25

## test greeting loop
#: t -- dup 0 < >r if greeting ; 5 t loop

# add MOD as remainder ( n n -- n % n )

# : fibo >r over over + dup . dup r> over over > if fibo ;
# 0 1 21 fibo  ( 0 1 -- 0 1 1 2 3 5 8 13 21 )

# ." greater " .greater
# ." lesser " .lesser
# 1 2 < if .greater else .lesser
# 1 2 > if .greater else .lesser
# else was problematic, create IIF next

################################################################
# done
################################################################


# add see operator requires a decompiling library that I cannot import
# when creating a new function or variable, add to see stack so that see can say what is in it

# loop utilizing IF statement
# : t dup 3 < dup >r if drop r> if t ; 1 2 3 4 5 6 t .. ( n > 3 == > drop -- 1 2 3 )

# forget t \ removes word 't'

# add MOD as remainder ( n n -- n % n )

# add comments encapulated in parens ( n -- n ) or \ remaining line comment starts with '\'
# : t 1 2 > ( n > n -- bool ) . ;

################################################################
# todo
################################################################

# need immediate iif ( n n cond -- if trueOp falseOp )

# add arrays and maybe file read/write

# test looping construct
"""
" *" star
: .*s dup . star + ;
: loops -- >r .*s r> dup 0 < if loops ;
star 5 loops

output:
* 
** 
*** 
**** 
***** 

"""

# ( grow stars 1:5:1 )
"""

" *" star
: add_star star + ;
: copy_print dup . ;
: save_stars dup >l ;
: track_loops >r ;
: reduce_loops r> -- ;
: continue_loop? dup 0 < iif True nip;
: fetch_saved_stars l> ;
: show_stars . ;
: drop2 drop drop ;
: grow* track_loops copy_print save_stars add_star reduce_loops continue_loop? if grow* ;
: shrink* l> dup . len 1 < if shrink* ;
star 5 grow* ( print groing triangle followed by shrinking triangle ) shrink*

"""

# hello whirled
"""
" hello whirled" .
"""

# test calc largest fibo sequence under 99
"""
Forth = PyForth()            # init
Forth.interpret(': fibo swap over + ;')
Forth.interpret(': fiboLoop >r fibo dup r> swap over > if fiboLoop ;')
Forth.interpret('0 1 99 fiboLoop drop drop')
print(f"first fibonacci above 99 is {Forth.s.pop()}")
"""

# test calc largest fibo sequence under 99
"""
import PyForth

Forth = PyForth()            # init

Forth.interpret(': initFibo 0 1 ;') # first two nubers of fibonacci sequence
Forth.interpret(': nextFibo swap over + ;') # next fibo is sum of two prior
Forth.interpret(': fiboLoop >r nextFibo dup r> swap over > if fiboLoop ;') # loop until goal
Forth.interpret(': Cleanup drop drop') # cleanup excess stack
Forth.interpret('initFibo 99 fiboLoop Cleanup') # put it all together and find the largest fibo below 99

print(f"largest fibonacci under 99 is {Forth.s.pop()}") # show me the money
"""
# cointdown with decreasing wait time
"""

: wait " time.sleep(self.s.pop())" eval drop;
: countdown dup . dup 200 swap / wait -- dup 0 < iif countdown drop;
99 countdown


"""

# test multi line replacing \n with ' '
"""
1
2
3 4
.. ( show stack )
+
+
+
.
( should print 10 )
.. ( show stack )
"""

# test storing a value into a variable
"""
3 three_or_five ( n -- ) \ places the value of 3 into variable called three_or_five
.. ( empty stack ) \ 
5 @ three_or_five ( n -- ) \ replaces 3 with 5
three_or_five ( n -- n ) \ puts 5 on the stack
. ( prints 5 )
"""
