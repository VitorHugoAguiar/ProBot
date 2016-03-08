#!/usr/bin/python

# First program to execute, where we choose the midi device
print ('\nChoose the midi device you want to use:')
print ('\n1 - Joystick')
print ('2 - Keyboard')
print ('3 - UC33')

userChoice=input('\nYour choice is: ')
options = {'1': ['Joystick.py'], '2': ['keyboard.py'], '3': ['UC33.py']}
file=options[userChoice]

print(file[0]+ " is now running. Enjoy!")
exec(open(file[0]).read())


