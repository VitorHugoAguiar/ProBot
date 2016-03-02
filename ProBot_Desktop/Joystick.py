import pygame
import ZMQCommunication
import LowPassFilter

# Initialization of classes from local files
Pub_Sub = ZMQCommunication.publisher_and_subscriber()
LPF=LowPassFilter.LowPassFilter()

# Initialization of the pygame 
pygame.init()
pygame.joystick.init()
clock = pygame.time.Clock() 

class Joystick():
	def __init__(self, done=0):
		self.done=False

	def mainRoutine(self):
		# -------- Main Program Loop -----------
		while self.done==False:
    		# EVENT PROCESSING STEP
    			for event in pygame.event.get(): # User did something
        			if event.type == pygame.QUIT: # If user clicked close
            				self.done=True # Flag that we are done so we exit this loop

    			for i in range(1):
        			joystick = pygame.joystick.Joystick(0)
        			joystick.init()
   				
   				# Potenciometers
        			axis1 = joystick.get_axis( 1 )
        			axis2 = joystick.get_axis( 2 )

        			directionForwardReverse=float(axis1)
        			directionLeftTRight=float(axis2)

        			FilteredValuesFR=LPF.lowPassFilterFR(-directionForwardReverse)
        			FilteredValuesLR=LPF.lowPassFilterLR(-directionLeftTRight)
    			
        			publisher=Pub_Sub.publisher('joystick', FilteredValuesFR, FilteredValuesLR)
        			
				# Limit to 20 frames per second
        			clock.tick(20)
		pygame.quit ()

	def main(self):
		Joystick.mainRoutine()

if __name__ == '__main__':
    Joystick = Joystick()
    Joystick.main()
