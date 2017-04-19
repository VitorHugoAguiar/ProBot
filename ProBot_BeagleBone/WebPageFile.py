#!/usr/bin/python

# Python Standart Library Imports
import SocketWebPageFile
import LowPassFilter
import ProBotConstantsFile
import decimal

Pub_Sub = SocketWebPageFile.SocketClass()
LPF = LowPassFilter.LowPassFilter()
Pconst = ProBotConstantsFile.Constants()

class WebPageClass():

    def __init__(self, PositionRef=0, TurnMotorRight=0, TurnMotorLeft=0, down=0, up=0, left=0, right=0, count=0):
        self.PositionRef = PositionRef
        self.TurnMotorRight = TurnMotorRight
        self.TurnMotorLeft = TurnMotorLeft
	self.up=up
	self.down=down
	self.left=left
	self.right=right
	self.count=count

    def WebPage_Values(self):
       	subscriber = Pub_Sub.subscriber() # Readings from the WebPage
	if self.count>=100:
        	self.PositionRef=0
       	        self.TurnMotorRight=0
                self.TurnMotorLeft=0
		self.count=100
                
 	if subscriber is None:
		subscriber=0
		self.count+=1	
        else:
	    	self.count=0
		incomingMsg1 = subscriber.replace("[", "")
	    	incomingMsg2 = incomingMsg1.replace("'", "")
	    	incomingMsg3 = incomingMsg2.replace("]", "") 
	    	incomingMsg4 = incomingMsg3.split(",")    
		self.up = incomingMsg4[0]
	    	self.down = incomingMsg4[1]
	    	self.left = incomingMsg4[2]
	    	self.right = incomingMsg4[3]    	    		
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
				
        return  [round(self.PositionRef, 5), round (self.TurnMotorRight, 5), round(self.TurnMotorLeft, 5)]
