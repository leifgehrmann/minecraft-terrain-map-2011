import sys

# Returns data in the format of an array, where:
# 0. The block values for each variation of color from 0-15
# 1. The minimum height from which a particular block must be from the ground.
# 2. The probability for each block to occur. The probabilities are cummulative.
# 3. Minimum probability, Maximum Probability, The size of the ore.
def getDepositInfo(fileName):
  	file = open(fileName);
  	info = [[1,1,1,1,1,1,1,1,1,1,1,1],
  		[0,0,0,0,0,0,0,0,0,0,0,0],
  		[0,0,0,0,0,0,0,0,0,0,0,0],
  		[0,0,0,0,0,0,0,0,0,0,0,0]];
  	index = 0;
  	part  = 0;
	while 1:
		lines = file.readlines(1)
		if not lines:
			break;
		for line in lines:
			if line.find("#")==0:
				pass;
			else:
				data = line.split(",");
				for i in range(0,len(data)):
					info[part][index] = int(data[i]);
					index = index + 1;
				part = part+1;
				index = 0;
	print(info);
	return info;