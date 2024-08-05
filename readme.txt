This is my attempt at buildig a Forth interpreter with Python, sourcing ideas from More and Brodie books.

20240719 started coding PyForth class in Python to track available Forth words 
  (verbs: +,-,*,/,dup,dup2,drop,drop2,over,over2,fib,.fiv,.,..,stack,clear,>r,r>,r.,square,end )
  initialize Python class with:
    Forth = PyForth()
  inpu t stream controlled with Python:
    while user_input != 'end': 
      user_input = input("type 'end' to exit: ")

20240719 added word "forget" to drop the next(head) word in the input stream
  
20240721 added vars = [] as a new stack to contain newly created variables

20240721 new word "variable" added that stores new variables in vars stack
  ### add quoted text with ." text thru ending "
  ### then add arrays and maybe file read/write


20240722 left and right stacks added:  l , r = [] ,[] 
  these will be the return stack and loop control stack

20240722 cleaned up "pick" and "roll" utilizing indexing

20240722 printable words added with words starting with ." and ending in "
  " hello whirled" .

20240723 add word "if" that executes the next(head) word
  also added int and Float

  ################################################################
  ### testing loop # : t --loop loop ; 5 t
  
  ## testing variable assigment and usage    
  # 1 2 3 + * x x x * y y . ==> x,y = 5,25
  
  ## test greeting loop
  #: t -- dup 0 < >r if greeting ; 5 t loop
  
  ################################################################
  # todo
  ################################################################
  
  # add comments encapulated in parens ( n -- n ) or \ remaining line comment starts with '\'
  
  # add see operator requires a decompiling library that I cannot import
  ## migth try another stack
  
  # add arrays and maybe file read/write

20240723 added word "see" to view how a word was created in the see stack

20240723 cleanup "if"
  ################################################################
  ### testing loop # : t --loop loop ; 5 t
  
  ## testing variable assigment and usage    
  # 1 2 3 + * x x x * y y . ==> x,y = 5,25
  
  ## test greeting loop
  #: t -- dup 0 < >r if greeting ; 5 t loop
  
  ################################################################
  # todo
  ################################################################

# add comments encapulated in parens ( n -- n ) or \ remaining line comment starts with '\'

# add see operator requires a decompiling library that I cannot import
## migth try another stack

# add arrays and maybe file read/write

20240723 cleanup "see" , "if", and "else"
  ################################################################
  ### testing loop # : t --loop loop ; 5 t
  
  ## testing variable assigment and usage    
  # 1 2 3 + * x x x * y y . ==> x,y = 5,25
  
  ## test greeting loop
  #: t -- dup 0 < >r if greeting ; 5 t loop
  
  # add MOD as remainder ( n n -- n % n )
  
  ################################################################
  # done
  ################################################################
  
  # add comments encapulated in parens ( n -- n ) or \ remaining line comment starts with '\'
  # : t 1 2 > ( n > n -- bool ) . ;
  
  # add see operator requires a decompiling library that I cannot import
  # when creating a new function or variable, add to see stack so that see can say what is in it
  
  # loop utilizing IF statement
  # : t dup 3 < dup >r if drop r> if t ; 1 2 3 4 5 6 t .. ( n > 3 == > drop -- 1 2 3 )
  
  # forget t \ removes word 't'
  
  ################################################################
  # todo
  ################################################################
  
  # add arrays and maybe file read/write
  

20240724 enhanced split_heat_tail()
  ( tail,splitter -- head,tail )
  splits the tail with the given splitter like space or semicolon or double quote, returning the new head and remaining tail

  # : fibs -- >r over over dup + dup . r> < if fibs ; 0 1  5 fibs

20240724 cleanup a bunch of items
  # test if else logic
  # create pritable result words "smaller" and "larger"
  #   ." smaller " smaller ." larger " larger 
  ### compare two values and print smaller or larger
  # 2 1 < dup if smaller else larger  \ smaller
  # 2 1 > dup if smaller else larger  \ larger
  
  #### comments failing now
  # add comments encapulated in parens ( n -- n ) or \ remaining line comment starts with '\'
  # : t 1 2 > ( n > n -- bool ) . ;

20240728 fixed commenting that ignores all between "(" and ")" or remining of the line starting with "\" (clears input tail)
  added "emit" wich prints <TOS> (Top Of Stack) without a newline or carriage return

20240728 checking stack after

  ## test greeting loop
  #: t -- dup 0 < >r if greeting ; 5 t loop
  
  # add MOD as remainder ( n n -- n % n )
  
  # : fibo >r over over + dup . dup r> over over > if fibo ;
  # 0 1 21 fibo  ( 0 1 -- 0 1 1 2 3 5 8 13 21 )
  
  # add see operator requires a decompiling library that I cannot import
  # when creating a new function or variable, add to see stack so that see can say what is in it
  
  # loop utilizing IF statement
  # : t dup 3 < dup >r if drop r> if t ; 1 2 3 4 5 6 t .. ( n > 3 == > drop -- 1 2 3 )
  
  # forget t \ removes word 't'
  
  # add MOD as remainder ( n n -- n % n )
  
  # add comments encapulated in parens ( n -- n ) or \ remaining line comment starts with '\'
  # : t 1 2 > ( n > n -- bool ) . ;
  

20240729 simplified all operators - utilizing self.interpret(" forth code goes here ")
  # need immediate iif ( n n cond -- if trueOp falseOp )
  
  # add arrays and maybe file read/write
  
  # test looping construct
  """
  
  : .*s dup . " *" + ;
  : loops -- >r .*s r> dup 0 < if loops ;
  " *" 5 loops
  
  output:
  * 
  ** 
  *** 
  **** 
  ***** 
  
  """

20240729 cleanup compiler : name method ;

  # ." greater " .greater
  # ." lesser " .lesser
  # 1 2 < if .greater else .lesser
  # 1 2 > if .greater else .lesser
  # else was problematic, create IIF next

20240729 eliminate "loop", reduce cod to 93 lines
  test calls from Python and utilize Forth stack after

  import PyForth
  
  Forth = PyForth()            # init
  
  Forth.interpret(': initFibo 0 1 ;') # first two nubers of fibonacci sequence
  Forth.interpret(': nextFibo swap over + ;') # next fibo is sum of two prior
  Forth.interpret(': fiboLoop >r nextFibo dup r> swap over > if fiboLoop ;') # loop until goal
  Forth.interpret(': Cleanup drop drop') # cleanup excess stack
  Forth.interpret('initFibo 99 fiboLoop Cleanup') # put it all together and find the largest fibo below 99
  
  print(f"largest fibonacci under 99 is {Forth.stack.pop()}") # show me the money
  """

20240729 added "iff", which executes next word as the THENOP if TOS is True, or executes following word as the ELSEOP if TOS is False

20240730 added "s", aka "pick", which copies s[index] to TOS
  removed L stack in efforts to simplify

20240730 removed "variable" as it is automatically creating words that do not exist as word key and value = TOS

20240730 added "eval" wich evaluates valid Python code, will be handy to see what method is tied to a word or executing other Python library functions
  'eval'   : lambda: self.s.append(eval(f"{self.s.pop()}")),

20240801 removed see stack, utilizing eval to see into the method of a word, only works good for hard coded words, otherwise cryptic lambda function shown, but close
  added "math" to process "-,*,/,//,%,**"
  added "logic" to process "not,<,<=,>,>=,="
  still keeping words "max,min,abs", "True"=1 and "False"=0  -- previously True=-1 and False=0
  negate is basically -1*abs(n)
  added "nip" to drop s[-2]

  elif head == 'see':     # show method for a word 
    key,tail = self.split_head_tail(tail," ")
    print(inspect.getsource(self.words[key]).strip())

20240802 allow for int or float on input

         else:
                try: isNumeric = float(head) ; self.s.append(int(float(head)) if int(float(head)) == float(head) else float(head))  # add to stack if numeric
                except ValueError:               # new word like variable n
                    self.words[head] = lambda value = self.s.pop() : self.s.append(value)

20240802 cleanup if and iif and add mulit line code input or copy/paste
            elif head == 'if' :     # conditional
                if self.s.pop() in( False , 0.0 , 0 , 'False' ) :    # 'if op' executes op when TOS is true
                    head,tail = self.split_head_tail(tail," ")
            elif head == 'iif' :    # immediate-if
                thenop,tail = self.split_head_tail(tail," ")
                elseop,tail = self.split_head_tail(tail," ")
                tail = ( thenop if self.s.pop() else elseop ) + ' ' + tail

                                                             
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

20240802 testing looping structures
  \ cointdown with decreasing wait time 
  : wait " time.sleep(self.s.pop())" eval drop;
  : countdown dup . dup 200 swap / wait -- dup 0 < iif countdown drop;
  99 countdown

20240802 cleaned up comments, multi-line forth code on input, gro/shrink star looping to print half diamond
            elif head == '(':           # ignore ( comment )
                head,tail = self.split_head_tail(tail,")")
                head,tail = self.split_head_tail(tail," ")
            elif head == '\\':          # ignore rest of line \ comment
                tail = ''

  ( testing loop up and down )
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

20240802 added "len" - need to later add "right" , "left" and "cat" but using "+" now for cat
  'len'    : lambda: self.s.append(len(self.s.pop())),
                        
20240802 countdown with decreasing wait time via Pyhon import time
  : wait " time.sleep(self.s.pop())" eval drop ;
  : countdown dup . dup 200 swap / wait - dup 0  iif countown drop ;
  99 countdown

20240804 added "@" store_tos_to_this_varname -- 94 lines now - WOW !!!
           elif head == '@':           # store tos in existing variable on stack
                key,tail = self.split_head_tail(tail," ")
                self.words[key] = lambda value = self.s.pop() : self.s.append(value)
 
  ( test comments, multi line input, variable storage and retrieval )
  3 three_or_five ( n -- ) \ places the value of 3 into variable called three_or_five
  .. ( empty stack ) \ 
  5 @ three_or_five ( n -- ) \ replaces 3 with 5
  three_or_five ( n -- n ) \ puts 5 on the stack
  . ( prints 5 )








