#!/usr/bin/python
# compile CSV into byte code

#import ita
import sys

if len(sys.argv) != 3: 
    print "Usage: python compiler.py <source csv> <binary file output>"
    print "Compiler for GTI converts CSV files into binary byte code"
    quit()

source = sys.argv[1]
destination = sys.argv[2]

file = open(source,"r")
source = file.readlines()
file.close()

rooms = []
room_type = []
room_label = []
room_size = []
room_address = []
room_exits = []
address = {}
compiled = ""
mode = 0


for i in range(0,len(source)):
   line = source[i].split(",")
   mode = line[1]
   if mode.upper() == "ROOM":
       binary = "" 
       exit_a = line[2]
       exit_b = line[3]
       exit_a_description = line[4]
       exit_b_description = line[5]
       description = ",".join(line[6:]).rstrip()
       # binary = binary + chr(exit_a >> 8) + chr(exit_a & 0xFF)
       # binary = binary + chr(exit_b >> 8) + chr(exit_b & 0xFF)
       binary = binary + exit_a_description + chr(0)
       binary = binary + exit_b_description + chr(0)
       binary = binary + description + chr(0)
       rooms.append(binary)
       room_type.append("room")
       room_label.append(line[0])
       room_exits.append([exit_a,exit_b])
   if mode.upper() == "SPECIAL":
       if line[2].upper() == "END":
             binary = ""
             description = ",".join(line[3:])
             binary = binary + description + chr(0)
             rooms.append(binary)
             room_type.append("end")
             room_label.append(line[0])
             room_exits.append(['special','end'])
       if line[2].upper() == "TEXT":
             binary = ""
             description = ",".join(line[3:]).rstrip()
             binary = binary + description + chr(0)
             rooms.append(binary)
             room_type.append("text")
             room_label.append(line[0])
             room_exits.append(['special','text'])
       if line[2].upper() == "JUMP":
             rooms.append("")
             room_type.append("jump")
             room_label.append(line[0])
             room_exits.append([line[3].rstrip(),line[3].rstrip()])
       if line[2].upper() == "EFFECT":
             rooms.append(line[3].rstrip())
             room_type.append("effect")
             room_label.append(line[0])
             room_exits.append([line[3].rstrip(),line[3].rstrip()])
            


print "ASCII data converted. Indexing rooms complete."

# Build a list of field lengths

for i in range(0,len(rooms)):
     size = 2
     if room_type[i] == "room":
         size = size + 2
         size = size + len(rooms[i])
     if room_type[i] == "end":
         size = size + 1
         size = size + len(rooms[i])
     if room_type[i] == "text":
         size = size + 1
         size = size + len(rooms[i])
     if room_type[i] == "jump":
         size = size + 3
     if room_type[i] == "effect":
         size = size + 2
     room_size.append(size) 


print "Calculated field lenghs."

# calculate room addresses

pc = 0

for i in range(0,len(rooms)):
     room_address.append(pc)
     pc = pc + room_size[i]

print "Calculated field addresses."

for i in range(0,len(rooms)):
     address[room_label[i]] = room_address[i]

print "Label address dictionary built."

for i in range(0,len(rooms)):
#  try:
     if room_type[i] == "room":
       print room_exits[i][0]+" "+room_exits[i][1]
       compiled = compiled + chr(address[room_exits[i][0]] >> 8) + chr(address[room_exits[i][0]] & 0xFF)
       compiled = compiled + chr(address[room_exits[i][1]] >> 8) + chr(address[room_exits[i][1]] & 0xFF)
       compiled = compiled + rooms[i].rstrip()
     if room_type[i] == "end":
       compiled = compiled + chr(255) + chr(255)
       compiled = compiled + chr(0)
       compiled = compiled + rooms[i].rstrip()
     if room_type[i] == "text":
       compiled = compiled + chr(255) + chr(255)
       compiled = compiled + chr(16)
       compiled = compiled + rooms[i].rstrip()
     if room_type[i] == "jump":
       compiled = compiled + chr(255) + chr(255)
       compiled = compiled + chr(5)
       compiled = compiled + chr(address[room_exits[i][0]] >> 8) + chr(address[room_exits[i][0]] & 0xFF)
     if room_type[i] == "effect":
       compiled = compiled + chr(255) + chr(255)
       compiled = compiled + chr(13)
       compiled = compiled + chr(int(rooms[i].rstrip()))


#  except:
#     print "Cannot find destination label in room "+room_label[i]
#     quit()
 
print "Compile complete."
o = open(destination,"w")
o.write(compiled)
o.close()
print "Written to "+destination+"."
print "Final length was "+str(len(compiled))+"."

base = 12722
max = 28672
size = max - base
if len(compiled) > size:  print "Arduboy warning: memory size exceeded by "+str(len(compiled) - size)+" bytes!"

