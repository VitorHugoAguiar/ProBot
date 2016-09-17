import sys
import os

ip_server=raw_input( "\nPlease enter the ProBot's Server ip: ")
confirm=raw_input ("Confirm (Y/N)?\n")

if (confirm=="n" or confirm=="N"):
  os.execv(sys.executable, ['python'] + sys.argv)
elif (confirm=="y" or confirm=="Y"):
  print "OK!"
else:
  print "Try Again"
  os.execv(sys.executable, ['python'] + sys.argv)
# Read in the file
filedata = None
with open('WebClient.py', 'r') as file :
  filedata = file.read()

# Replace the target string
filedata = filedata.replace('ip_server', ip_server)

# Write the file out again
with open('WebClient.py', 'w') as file:
  file.write(filedata)
