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
		typeFilter = { 
          		'directionFR': [self.filteredDataFR, self.LPFgainFR],
          		'directionLR': [self.filteredDataLR, self.LPFgainLR],
          		'EncoderR': [self.filteredDataER, self.LPFgainEncoders],
          		'EncoderL': [self.filteredDataEL, self.LPFgainEncoders]}

        	variables = typeFilter[type]
		variables[0][0] = value * variables[1] + variables[0][1] * (1-variables[1])
                variables[0][1] = variables[0][0]
		
                return variables[0][0]

