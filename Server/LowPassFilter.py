filteredDataFR=[0,0,0,0]
filteredDataLR=[0,0,0,0]
LPFgainFR=0.1
LPFgainLR=0.33

class LowPassFilter():
	def lowPassFilterFR(self, directionForward, directionReverse):	
		filteredDataFR[0]=directionForward*LPFgainFR+filteredDataFR[1]*(1-LPFgainFR)
		filteredDataFR[1]=filteredDataFR[0]

		filteredDataFR[2]=directionReverse*LPFgainFR+filteredDataFR[3]*(1-LPFgainFR)
		filteredDataFR[3]=filteredDataFR[2]
		
		return filteredDataFR[0],filteredDataFR[2],
		
	
	def lowPassFilterLR(self, directionLeft, directionRight):
		filteredDataLR[0]=directionLeft*LPFgainLR+filteredDataLR[1]*(1-LPFgainLR)
		filteredDataLR[1]=filteredDataLR[0]

		filteredDataLR[2]=directionRight*LPFgainLR+filteredDataLR[3]*(1-LPFgainLR)
		filteredDataLR[3]=filteredDataLR[2]
		
		return filteredDataLR[0],filteredDataLR[2]
