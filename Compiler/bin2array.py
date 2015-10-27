# convert BIN GTI files to C++ arrays for Arduino

import sys

if len(sys.argv) != 2:
   print "Usage: bin2array.py <input binary file>"
   quit()

input = sys.argv[1]
file = open(input,"r")
 
print "const unsigned char gti[] PROGMEM = { "

col = 0

while 1==1:
   data = file.read(1)
   if data == "": break
   sys.stdout.write(str(ord(data))+",")
   col = col + 1
   if col == 90000: 
        sys.stdout.write("\n")
        col = 0
print "};"

