#!/usr/bin/python

# Python Standart Library Imports
import SocketFile
import LowPassFilter
import ProBotConstantsFile
import decimal

Pub_Sub = SocketFile.SocketClass()
LPF = LowPassFilter.LowPassFilter()
Pconst = ProBotConstantsFile.Constants()

class WebPageClass():

    def __init__(self, PositionRef=0, TurnMotorRight=0, TurnMotorLeft=0, down=0, up=0, left=0, right=0):
        self.PositionRef = PositionRef
        self.TurnMotorRight = TurnMotorRight
        self.TurnMotorLeft = TurnMotorLeft
	self.up=up
	self.down=down
	self.left=left
	self.right=right

    def WebPage_Values(self):
        # Readings from the WebPage
        subscriber = Pub_Sub.subscriber()

        if subscriber is None:
            subscriber = 0
 
        else:
	    incomingMsg = subscriber.split(" ") 

	    if incomingMsg[0]=="web":
		self.up = incomingMsg[1]
		self.down = incomingMsg[2]
		self.left = incomingMsg[3]
		self.right = incomingMsg[4]

	    Forward = float(decimal.Decimal(self.up))
	    Reverse = -float(decimal.Decimal(self.down))
	    Left = float(decimal.Decimal(self.left))
	    Right = -float(decimal.Decimal(self.right))

	    ForwardReverse=Forward+Reverse
	    LeftRight=Left+Right

	    ForwardReverse=LPF.lowPassFilterFR(ForwardReverse)
	    LeftRight=LPF.lowPassFilterLR(LeftRight)
	    self.PositionRef = -float(ForwardReverse*Pconst.ajustFR)
	    self.TurnMotorRight = float(LeftRight*Pconst.ajustLR)
	    self.TurnMotorLeft = -float(LeftRight*Pconst.ajustLR)


        return  round(self.PositionRef, 5), round (self.TurnMotorRight, 5), round(self.TurnMotorLeft, 5)
