#!/usr/bin/python

# Low Pass Filter used to obtain a smooth response from the joysticks potenciomenters, the keyboard's arrows, the touch joysticks and encoders
class LowPassFilter():

	def __init__(self):
		self.filteredDataFR = [0,0]
		self.filteredDataLR = [0,0]
		self.filteredDataER = [0,0]
		self.filteredDataEL = [0,0]
		self.LPFgainFR = 0.035
		self.LPFgainLR = 0.8
		self.LPFgainEncoders = 0.3

	def lowPassFilter(self, value, type):
		GenericFilter = { 
          		'directionFR': [self.filteredDataFR, self.LPFgainFR],
          		'directionLR': [self.filteredDataLR, self.LPFgainLR],
          		'EncoderR': [self.filteredDataER, self.LPFgainEncoders],
          		'EncoderL': [self.filteredDataEL, self.LPFgainEncoders]}

        	GenericVariables = GenericFilter[type]
		GenericVariables[0][0] = value * GenericVariables[1] + GenericVariables[0][1] * (1 - GenericVariables[1])
                GenericVariables[0][1] = GenericVariables[0][0]
		
                return GenericVariables[0][0]

