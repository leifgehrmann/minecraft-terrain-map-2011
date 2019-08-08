import sys

# Returns data in the format of an array, where:
# 0. Minimum Height
# 1. Maximum Height
# 2. Bedrock Level height
def getElevationInfo(fileName):
  	file = open(fileName);
  	info = [0,0,0];
  	index = 0;
	while 1:
		lines = file.readlines(100000)
		if not lines:
			break;
		for line in lines:
			if line.find("#")==0:
				pass;
			else:
				data = line.split(",");
				for i in range(0,len(data)):
					if index<3:
						info[index] = int(data[i]);
						index = index + 1;
	print(info);
	return info;
