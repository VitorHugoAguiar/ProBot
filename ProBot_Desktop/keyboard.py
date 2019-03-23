#!/usr/bin/python
import pygame
import ZMQCommunication
import LowPassFilter

# Initialization of classes from local files
Pub_Sub = ZMQCommunication.publisher_and_subscriber()
LPF=LowPassFilter.LowPassFilter()

pygame.init()
pygame.display.set_mode((200, 200))
clock = pygame.time.Clock() 


# Readings from the keyboard arrows, that are smoothed by the LowPass filter
class KeyBoard():
	def __init__(self, FilteredValuesFR=0, FilteredValuesLR=0,lock = 0, maxValFR=0, maxValLR=0):
		self.FilteredValuesFR=FilteredValuesFR
		self.FilteredValuesLR=FilteredValuesLR		
		self.lock = [False, False, False, False]
		self.maxValFR=maxValFR
		self.maxValLR=maxValLR
	def mainRoutine(self):
		while True:
    			for event in pygame.event.get():
        			if event.type == pygame.QUIT:
            				pygame.quit(); #sys.exit() if sys is imported
    			keys = pygame.key.get_pressed()  #checking pressed keys
	
    			if keys[pygame.K_UP]:
       				self.maxValFR=0.7
       				self.FilteredValuesFR=LPF.lowPassFilterFR(self.maxValFR)
       				self.lock[0] = True;
    			if keys[pygame.K_DOWN]:
       				self.maxValFR=-0.7
       				self.FilteredValuesFR=LPF.lowPassFilterFR(self.maxValFR)
       				self.lock[1] = True;
    			if keys[pygame.K_LEFT]:
       				self.maxValLR=0.8
       				self.FilteredValuesLR=LPF.lowPassFilterLR(self.maxValLR)
       				self.lock[2] = True;
    			if keys[pygame.K_RIGHT]:
       				self.maxValLR=-0.8
       				self.FilteredValuesLR=LPF.lowPassFilterLR(self.maxValLR)
       				self.lock[3] = True;

    			if event.type == pygame.KEYUP:
        			if event.key == pygame.K_UP:
            				self.maxValFR=0
            				self.FilteredValuesFR=LPF.lowPassFilterFR(self.maxValFR)       
            				self.lock[0] = False;
       				if event.key == pygame.K_DOWN:
            				self.maxValFR=0
            				self.FilteredValuesFR=LPF.lowPassFilterFR(self.maxValFR)   
            				self.lock[1] = False;
        			if event.key == pygame.K_LEFT:
            				self.maxValLR=0
            				self.FilteredValuesLR=LPF.lowPassFilterLR(self.maxValLR)       
            				self.lock[2] = False;
       				if event.key == pygame.K_RIGHT:
            				self.maxValLR=0
            				self.FilteredValuesLR=LPF.lowPassFilterLR(self.maxValLR)   
            				self.lock[3] = False;

    			publisher=Pub_Sub.publisher('keyboard', self.FilteredValuesFR, self.FilteredValuesLR)
    			clock.tick(20)

	def main(self):
		KeyBoard.mainRoutine()

if __name__ == '__main__':
	KeyBoard = KeyBoard()
	KeyBoard.main()	  
