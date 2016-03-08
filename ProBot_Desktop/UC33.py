#!/usr/bin/python

import sys, pygame, pygame.midi, zmq, time, math
import ZMQCommunication

Pub_Sub=ZMQCommunication.publisher_and_subscriber()

# set up pygame
pygame.init()
pygame.midi.init()

# open a specific midi device
device=3
inp = pygame.midi.Input(device)

class UC33():
	def __init__(self, id=0, value=0, Matrix=0, KpP_UC33=0, KiP_UC33=0, KdP_UC33=0, KpV_UC33=0, KiV_UC33=0, KdV_UC33=0, KpA_UC33=0, KiA_UC33=0, KdA_UC33=0):
		self.id=id
		self.value=value		
		self.Matrix = [0 for x in range(34)]
		self.KpP_UC33=KpP_UC33
		self.KiP_UC33=KiP_UC33
		self.KdP_UC33=KdP_UC33
		self.KpV_UC33=KpV_UC33
		self.KiV_UC33=KiV_UC33
		self.KdV_UC33=KdV_UC33
		self.KpA_UC33=KpA_UC33
		self.KiA_UC33=KiA_UC33
		self.KdA_UC33=KdA_UC33
	
	def mainRoutine(self):

	
		# run the event loop
		while True:
			if inp.poll():
				# no way to find number of messages in queue
				# so we just specify a high max value
				midi_events = inp.read(1000)	
				self.id=midi_events[0][0][1]			
				self.value= midi_events[0][0][2]
				idInt=int(self.id)	
				self.Matrix[idInt]=self.value	
				self.KpP_UC33=(0.1*self.Matrix[25]+0.01*self.Matrix[17]+0.001*self.Matrix[9]-0.1*self.Matrix[1])
				self.KiP_UC33=(0.1*self.Matrix[26]+0.01*self.Matrix[18]+0.001*self.Matrix[10]-0.1*self.Matrix[2])
				self.KdP_UC33=(0.1*self.Matrix[27]+0.01*self.Matrix[19]+0.001*self.Matrix[11]-0.1*self.Matrix[3])
				self.KpV_UC33=(0.1*self.Matrix[28]+0.01*self.Matrix[20]+0.001*self.Matrix[12]-0.1*self.Matrix[4])
				self.KiV_UC33=(0.1*self.Matrix[29]+0.01*self.Matrix[21]+0.001*self.Matrix[13]-0.1*self.Matrix[5])
				self.KdV_UC33=(0.1*self.Matrix[30]+0.01*self.Matrix[22]+0.001*self.Matrix[14]-0.1*self.Matrix[6])
				self.KpA_UC33=(0.1*self.Matrix[31]+0.01*self.Matrix[23]+0.001*self.Matrix[15]-0.1*self.Matrix[7])
				self.KiA_UC33=(0.1*self.Matrix[32]+0.01*self.Matrix[24]+0.001*self.Matrix[16]-0.1*self.Matrix[8])
				self.KdA_UC33=(-0.1*self.Matrix[33])
				print (" KpP %.3f\n" % self.KpP_UC33,"KiP %.3f\n" % self.KiP_UC33, "KdP %.3f\n" % self.KdP_UC33, "KpV %.3f\n" % self.KpV_UC33, "KiV %.3f\n" % self.KiV_UC33, "KdV %.3f\n" % self.KdV_UC33, "KpA %.3f\n" % self.KpA_UC33, "KiA %.3f\n" % self.KiA_UC33, "KdA %.3f\n" % self.KdA_UC33)
				publisher=Pub_Sub.publisher('UC33', self.id, self.value)
			
	def main(self):
        	UC33.mainRoutine()

if __name__ == '__main__':
	UC33 = UC33()
	UC33.main()
		
