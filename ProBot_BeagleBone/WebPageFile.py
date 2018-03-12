#!/usr/bin/python

# Python Standart Library Imports
import decimal
import memcache
import math

# Local files
import LowPassFilter
import ProBotConstantsFile

# Initialization of classes from local files
LPF = LowPassFilter.LowPassFilter()
Pconst = ProBotConstantsFile.Constants()

shared = memcache.Client([('localhost', 15)], debug=0)

class WebPageClass():

    def __init__(self):
        self.PositionRef = 0
        self.TurnMotorRight = 0
        self.TurnMotorLeft = 0
	self.up = 0
	self.down = 0
	self.left = 0
	self.right = 0
	self.limit = 0.75
	self.radius = 0.02
	self.ajustFR = 0.046
        self.ajustLR = 0.008


    def WebPage_Values(self):
	keysValues = shared.get('keys')
	
	if keysValues is None:
		self.up = 0
		self.down = 0
		self.left = 0
		self.right = 0	
		
        else:
		self.up, self.down, self.left, self.right = keysValues.split(" ")
				
		Forward = float(decimal.Decimal(self.up))
		Reverse = -float(decimal.Decimal(self.down))
		Left = float(decimal.Decimal(self.left))
		Right = -float(decimal.Decimal(self.right))
	    	
        	Forward = max(0, min(Forward, self.limit))
        	Reverse = max(-self.limit, min(Reverse, 0))
        	Left = max(0, min(Left, self.limit))
        	Right = max(-self.limit, min(Right, 0))
		
		self.PositionRef = -float(Forward+Reverse)* self.ajustFR

        	if (self.PositionRef > 0):
          		self.PositionRef = math.sqrt((self.radius*self.radius) + (self.PositionRef*self.PositionRef)) - self.radius	

        	else:
			self.PositionRef = -math.sqrt((self.radius*self.radius) + (self.PositionRef*self.PositionRef)) + self.radius		
		
		LeftRight=LPF.lowPassFilter(Left+Right, 'directionLR')
		self.PositionRef = LPF.lowPassFilter(self.PositionRef, 'directionFR')
	
		self.TurnMotorRight = float(LeftRight*self.ajustLR)
		self.TurnMotorLeft = -float(LeftRight*self.ajustLR)
		
        return  [round(self.PositionRef, 5), round (self.TurnMotorRight, 5), round(self.TurnMotorLeft, 5)]
