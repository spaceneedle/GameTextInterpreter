# ITA2 BAUDOT Library

mode = 0

letters = "@E\nA SIU$DRJNFCKTZLWHYPQOBG^MXV~"  # $ = CR, ^ = shift numbers, ~ = shift letters
#          01 234567890123456789012345678901
#                     1         2         3
numbers = "@3\n- $87%=4',!:(5\")2#6019?&^./;~"    # $ = bell, = WRU?, ^ = shift numbers, ~ = shift to letters
#          01 234567890123456 789012345678901"
#                     1          2        3

# converts ASCII to ITA2

def a2ita(character):
   if character == "^": return bin(27).split("b")[1].zfill(5)
   if character == "~": return bin(31).split("b")[1].zfill(5)
   for i in range(0,31):
     if mode == 0:
      if character == letters[i]: return bin(i).split("b")[1].zfill(5)
     if mode == 1:
      if character == numbers[i]: return bin(i).split("b")[1].zfill(5)
   return "00000"

# converts a block of 10 characters into 5 byte ITA2 (40 bits)

def a2itablock(string):
   bits = ""
   binary = ""
   oldstring = string
   string = ""
   mode = 0
   for i in range(0,len(oldstring)):   # pre-processor to insert control characters
       if mode == 0:
          if (oldstring[i].isnumeric() == True) or (oldstring[i] == "-") or (oldstring[i] == ",") or (oldstring[i] == ".") or (oldstring[i] == "\"") or (oldstring[i] == "?"):    
             string = string + "^"
             mode = 1
             print "switch to number"
       else:
          if (oldstring[i].isnumeric() == False) or (oldstring[i] != "\n") or (oldstring[i] != " ") or (oldstring[i] != "\n") or (oldstring[i] != "-") or (oldstring[i] != ",") or (oldstring[i] != ".") or (oldstring[i] != "\"") or (oldstring[i] != "?"):
             string = string + "~"
             mode = 0
             print "switch to string"
       string = string + oldstring[i]
   mode = 0
   for x in range(0,len(string),8):
    bits = ""
    for i in range(0,9):
       try:
          bits = bits + a2ita(string[i+x])
       except:
          bits = bits + "00000"
    for i in range(0,39,8):
       binary = binary + chr(int(bits[i:i+8],2))
   if len(binary) % 5 == 0:
       binary = binary + chr(0)    
   return binary

# function that calls ITA2 lookup table for baudot()

def b2a(value):
   if mode == 0:
      return letters[value]
   if mode == 1:
      return numbers[value]


# decodes ITA2

def baudot(string):
   bits = ""
   output = ""
   for i in range(0,len(string)):
      bits = bits + bin(ord(string[i])).split("b")[1].zfill(8)
   for i in range(0,len(bits),5):
      output = output + b2a(int(bits[i:i+5],2))
   return output

