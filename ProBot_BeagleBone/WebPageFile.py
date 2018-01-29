#!/usr/bin/python

# Python Standart Library Imports
import decimal
import memcache
import math

# Local files
import LowPassFilter
import ProBotConstantsFile

shared = memcache.Client([('127.0.0.1', 15)], debug=0)

# Initialization of classes from local files
LPF = LowPassFilter.LowPassFilter()
Pconst = ProBotConstantsFile.Constants()

class WebPageClass():

    def __init__(self, PositionRef=0, TurnMotorRight=0, TurnMotorLeft=0, down=0, up=0, left=0, right=0, count=0, limit=0.56, radius=0.0008):
        self.PositionRef = PositionRef
        self.TurnMotorRight = TurnMotorRight
        self.TurnMotorLeft = TurnMotorLeft
	self.up=up
	self.down=down
	self.left=left
	self.right=right
	self.count=count
	self.limit=limit
	self.radius=radius
    def WebPage_Values(self):
	keysValues = shared.get('keys')

	if self.count>=100:
        	self.PositionRef=0
       	        self.TurnMotorRight=0
                self.TurnMotorLeft=0
		self.count=100

 	if keysValues is None:
		keysValues=0
		self.count+=1
        else:
	    	self.count=0
		self.up, self.down, self.left, self.right = keysValues.split(" ")
		
		Forward = float(decimal.Decimal(self.up))
	    	Reverse = -float(decimal.Decimal(self.down))
	    	Left = float(decimal.Decimal(self.left))
	    	Right = -float(decimal.Decimal(self.right))
	    	
                Forward = max(0, min(Forward, self.limit))
                Reverse = max(-self.limit, min(Reverse, 0))
                Left = max(0, min(Left, self.limit))
                Right = max(-self.limit, min(Right, 0))
		
	    	LeftRight=LPF.lowPassFilterLR(Left+Right)
		self.PositionRef = -float(Forward+Reverse)* Pconst.ajustFR

        	if (self.PositionRef > 0):
			self.PositionRef = math.sqrt((self.radius*self.radius)+(self.PositionRef*self.PositionRef))-self.radius	

        	else:
			self.PositionRef = -math.sqrt((self.radius*self.radius)+(self.PositionRef*self.PositionRef))+self.radius		

	    	self.TurnMotorRight = float(LeftRight*Pconst.ajustLR)
	    	self.TurnMotorLeft = -float(LeftRight*Pconst.ajustLR)
		
        return  [round(self.PositionRef, 5), round (self.TurnMotorRight, 5), round(self.TurnMotorLeft, 5)]
