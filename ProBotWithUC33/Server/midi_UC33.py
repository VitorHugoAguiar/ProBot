import sys, pygame, pygame.midi, zmq, time, math
 
# set up pygame
pygame.init()
pygame.midi.init()

# list all midi devices
for x in range( 0, pygame.midi.get_count() ):
	print pygame.midi.get_device_info(x)
 
# open a specific midi device
device=3
inp = pygame.midi.Input(device)


# We wait for 1 subscriber
SUBSCRIBERS_EXPECTED = 1
def main():
	context = zmq.Context()

	# Socket to talk to clients
	publisher = context.socket(zmq.PUB)
	# set SNDHWM, so we don't drop messages for slow subscribers
	publisher.sndhwm = 1100000
	publisher.bind('tcp://*:5561')

	# Socket to receive signals
	syncservice = context.socket(zmq.REP)
	syncservice.bind('tcp://*:5562')

	# Get synchronization from subscribers
	subscribers = 0
	while subscribers < SUBSCRIBERS_EXPECTED:
		# wait for synchronization request
		msg = syncservice.recv()
		# send synchronization reply
		syncservice.send(b'')
		subscribers += 1
		print("+1 subscriber (%i/%i)" % (subscribers, SUBSCRIBERS_EXPECTED))
	
	KpP_decimas=0
	KpP1_decimas=0
	KpP_centesimas=0
	KpP_milesimas=0
	KpPTotal=0
	
	KiP_decimas=0
	KiP1_decimas=0
	KiP_centesimas=0
	KiP_milesimas=0
	KiPTotal=0

	KdP_decimas=0
	KdP1_decimas=0
	KdP_centesimas=0
	KdP_milesimas=0
	KdPTotal=0

	KpA_decimas=0
	KpA1_decimas=0
	KpA_centesimas=0
	KpA_milesimas=0
	KpATotal=0
	
	KiA_decimas=0
	KiA1_decimas=0
	KiA_centesimas=0
	KiA_milesimas=0
	KiATotal=0

	KdA_decimas=0
	KdA1_decimas=0
	KdA_centesimas=0
	KdA_milesimas=0
	KdATotal=0

	KpV_decimas=0
	KpV1_decimas=0
	KpV_centesimas=0
	KpV_milesimas=0
	KpVTotal=0
	
	KiV_decimas=0
	KiV1_decimas=0
	KiV_centesimas=0
	KiV_milesimas=0
	KiVTotal=0
	
	KdV_decimas=0
	KdVTotal=0
	
	# run the event loop
	while True:
		if inp.poll():
			# no way to find number of messages in queue
			# so we just specify a high max value
			midi_events = inp.read(1000)	
			id=midi_events[0][0][1]			
			value= midi_events[0][0][2]
			publisher.send(b'%d %d' % (id, value),zmq.NOBLOCK)

			KpPTotal=float(KpP_decimas-KpP1_decimas+KpP_centesimas+KpP_milesimas)
			KiPTotal=float(KiP_decimas-KiP1_decimas+KiP_centesimas+KiP_milesimas)
			KdPTotal=float(KdP_decimas-KdP1_decimas+KdP_centesimas+KdP_milesimas)

		
			KpATotal=float(KpA_decimas-KpA1_decimas+KpA_centesimas+KpA_milesimas)
			KiATotal=float(KiA_decimas-KiA1_decimas+KiA_centesimas+KiA_milesimas)
			KdATotal=float(KdA_decimas-KdA1_decimas+KdA_centesimas+KdA_milesimas)

			KpVTotal=float(KpV_decimas-KpV1_decimas+KpV_centesimas+KpV_milesimas)
			KiVTotal=float(KiV_decimas-KiV1_decimas+KiV_centesimas+KiV_milesimas)
			
			KdVTotal=KdV_decimas

			if id==25 or id==1:			
				if id==25:				
					KpP_decimas=value*0.1
				if id==1:
					KpP1_decimas=value*0.1					
				print  "KpP_decimas= ", KpP_decimas-KpP1_decimas, "KpPTotal= ", KpPTotal
			
			if id==17:
				KpP_centesimas =value*0.01
				print "KpP_centesimas= ", KpP_centesimas,"KpPTotal= ", KpPTotal			
			if id==9:			
				KpP_milesimas =value*0.001
				print "KpP_milesimas= ", KpP_milesimas,"KpPTotal= ", KpPTotal
			
			if id==26 or id==2:			
				if id==26:							
					KiP_decimas=value*0.1
				if id==2:							
					KiP1_decimas=value*0.1
				print  "KiP_decimas= ", KiP_decimas-KiP_decimas, "KiPTotal= ", KiPTotal
			if id==18:
				KiP_centesimas =value*0.01
				print "KiP_centesimas= ", KiP_centesimas,"KiPTotal= ", KiPTotal			
			if id==10:
				KiP_milesimas =value*0.001
				print "KiP_milesimas= ", KiP_milesimas,"KiPTotal= ", KiPTotal

			if id==27 or id==3:			
				if id==27:				
					KdP_decimas=value*0.1
				if id==3:				
					KdP1_decimas=value*0.1
				print  "KdP_decimas= ", KdP_decimas-KdP1_decimas, "KdPTotal= ", KdPTotal
			if id==19:
				KdP_centesimas =value*0.01
				print "KdP_centesimas= ", KdP_centesimas,"KdPTotal= ", KdPTotal			
			if id==11:
				KdP_milesimas =value*0.001
				print "KdP_milesimas= ", KdP_milesimas,"KdPTotal= ", KdPTotal
			



			if id==28 or id==4:			
				if id==28:				
					KpA_decimas=value*0.1
				if id==4:				
					KpA1_decimas=value*0.1
				print  "KpA_decimas= ", KpA_decimas-KpA1_decimas, "KpATotal= ", KpATotal
			if id==20:
				KpA_centesimas =value*0.01
				print "KpA_centesimas= ", KpA_centesimas,"KpATotal= ", KpATotal			
			if id==12:
				KpA_milesimas =value*0.001
				print "KpA_milesimas= ", KpA_milesimas,"KpATotal= ", KpATotal
			
			if id==29 or id==5:
				if id==29:			
					KiA_decimas=value*0.1
				if id==5:			
					KiA1_decimas=value*0.1
				print  "KiA_decimas= ", KiA_decimas-KiA1_decimas, "KiATotal= ", KiATotal
			if id==21:
				KiA_centesimas =value*0.01
				print "KiA_centesimas= ", KiA_centesimas,"KiATotal= ", KiATotal			
			if id==13:
				KiA_milesimas =value*0.001
				print "KiA_milesimas= ", KiA_milesimas,"KiATotal= ", KiATotal

			if id==30 or id==6:			
				if id==30:				
					KdA_decimas=value*0.1
				if id==6:				
					KdA1_decimas=value*0.1
				print  "KdA_decimas= ", KdA_decimas-KdA1_decimas, "KdATotal= ", KdATotal
			if id==22:
				KdA_centesimas =value*0.01
				print "KdA_centesimas= ", KdA_centesimas,"KdATotal= ", KdATotal			
			if id==14:
				KdA_milesimas =value*0.001
				print "KdA_milesimas= ", KdA_milesimas,"KdATotal= ", KdATotal

			
			if id==31 or id==7:
				if id==31:
					KpV_decimas =value*0.1
				if id==7:
					KpV1_decimas =value*0.1
				print "KpV_decimas= ", KpV_decimas,"KpVTotal= ", KpVTotal	

			if id==23:
				KpV_centesimas =value*0.01
				print "KpV_centesimas= ", KpV_centesimas,"KpVTotal= ", KpVTotal			
			if id==15:			
				KpV_milesimas =value*0.001
				print "KpV_milesimas= ", KpV_milesimas,"KpVTotal= ", KpVTotal

			if id==32 or id==8:
				if id==32:				
					KiV_decimas =value*0.1
				if id==8:				
					KiV1_decimas =value*0.1
				print "KiV_decimas= ", KiV_decimas,"KiVTotal= ", KiVTotal			
			if id==24:
				KiV_centesimas =value*0.01
				print "KiV_centesimas= ", KiV_centesimas,"KiVTotal= ", KiVTotal			
			if id==16:
				KiV_milesimas =value*0.001
				print "KiV_milesimas= ", KiV_milesimas,"KiVTotal= ", KiVTotal
			
			if id==33:				
				KdV_decimas =value*0.1
				print "KdV_decimas= ", KdV_decimas,"KdVTotal= ", KdVTotal


			
			#print id, value

if __name__ == '__main__':
	main()

		
