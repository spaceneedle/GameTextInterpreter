#!/usr/bin/python
# GBI Player

pc = 0
mode = 0
import ita
col = 0

import sys
binary = sys.argv

if len(binary) != 2:
   print "Usage: python player.py <game.bin>"
   quit()

binary = binary[1]

def hasnull(string):
   for i in range(0,len(string)):
      if ord(string[i]) == 0: return 1
   return 0

f = open(binary)
code = f.read(32768)
f.close()

while 1==1:
  type = ord(code[pc]) << 8 | ord(code[pc+1])
#  print "type: "+str(type)
  if type == 65535:
          pc = pc + 2
          operation = ord(code[pc])
#          print "special operation: "+str(operation)
          if operation == 0:
                 print "** GAME OVER **\n\n"
                 buffer = ""
                 while 1==1: 
                   pc = pc + 1
                   if ord(code[pc]) == 0: break
                   buffer = buffer + code[pc]
                 print buffer 
                 a = raw_input("\n[Hit enter to reset]")
                 pc = 0
          if operation == 1:   # low resolution image
                 pc = pc + 22
                 # image not supported
          if operation == 2:   # high res image
                 pc = pc + 1024
                 # high res iage not supported
          if operation == 3:   # set variable 
                 var_name = ""
                 var_val = ""
                 while 1==1:
                   pc = pc + 1
                   if ord(code[pc]) == 0: break
                   var_name = var_name + code[pc]
                 while 1==1:
                   pc = pc + 1
                   if ord(code[pc]) == 0: break
                   var_val = var_val + code[pc]
                 storage[var_name] = var_val
                 pc = pc + 1
          if operation == 4:  # evaluate variable
                 var_name = ""
                 operator = 0
                 var_compare = ""
                 var_branch = ""
                 while 1==1:
                   pc = pc + 1
                   if ord(code[pc]) == 0: break
                   var_name = var_name + code[pc]
                 pc = pc + 1
                 operator = code[pc]
                 while 1==1:
                   pc = pc + 1
                   if ord(code[pc]) == 0: break
                   var_compare = var_compare + code[pc]
                 pc = pc + 1
                 var_branch = ord(code[pc]) << 8 | ord(code[pc+1]) & 0xFF
                 pc = pc + 2 
                 if operator == "$":
                   if storage[var_name] == var_compare: 
                      pc = var_branch
                 if operator == "<":
                   if int(storage[var_name]) < int(var_compare):
                      pc = var_branch
                 if operator == ">":
                   if storage[var_name] > var_compare: 
                      pc = var_branch
                 if operator == "l":
                   if int(storage[var_name]) <= int(var_compare):
                      pc = var_branch
                 if operator == "g":
                   if int(storage[var_name]) >= int(var_compare):
                      pc = var_branch
                 if operator == "!":
                   if storage[var_name] != var_compare:
                      pc = var_branch
          if operation == 5:
                 pc = pc + 1
                 var_branch = ord(code[pc]) << 8 | ord(code[pc+1]) & 0xFF
                 pc = var_branch
          if operation == 13:
                 pc = pc + 2
                 print "[Unsupported effect]"
          if operation == 16:
                 buffer = ""
                 while 1==1: 
                   pc = pc + 1
                   if ord(code[pc]) == 0: break
                   buffer = buffer + code[pc]
                 print buffer
                 raw_input("[Press Enter]")
                 pc = pc + 1
  else:       
   exit_a = type
   pc = pc + 2
   exit_b = ord(code[pc]) << 8 | ord(code[pc+1])
   pc = pc + 2
   exit_a_description = ""
   exit_b_description = ""
   text = ""
   while 1==1:
      if ord(code[pc]) == 0: break
      exit_a_description = exit_a_description + code[pc]
      pc = pc + 1
   pc = pc + 1
   while 1==1:
      if ord(code[pc]) == 0: break
      exit_b_description = exit_b_description + code[pc]
      pc = pc + 1
   pc = pc  +1 
   while 1==1:
      if ord(code[pc]) == 0: break
      text = text + code[pc]
      pc = pc + 1
   pc = pc + 1
   print ""
   print text
   print ""
   print "1. "+exit_a_description
   print "2. "+exit_b_description
   entry = raw_input("> ")
   if entry == "1": pc = exit_a
   if entry == "2": pc = exit_b





