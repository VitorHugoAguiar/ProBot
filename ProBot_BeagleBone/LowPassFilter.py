#!/usr/bin/python

# Low Pass Filter used to obtain a smooth response from the joysticks potenciomenters, the keyboard's arrows and the touch joysticks
filteredDataFR=[0,0]
filteredDataLR=[0,0]
LPFgainFR = 1
LPFgainLR = 0.8

# We use two filters, one to Forward/Reverse situation and one for the Turn situation
class LowPassFilter():

	def lowPassFilterFR(self, directionForwardReverse):

		filteredDataFR[0]=directionForwardReverse*LPFgainFR+filteredDataFR[1]*(1-LPFgainFR)
		filteredDataFR[1]=filteredDataFR[0]
		return filteredDataFR[0]


	def lowPassFilterLR(self, directionLeftRight):

		filteredDataLR[0]=directionLeftRight*LPFgainLR+filteredDataLR[1]*(1-LPFgainLR)
		filteredDataLR[1]=filteredDataLR[0]
		return filteredDataLR[0]

