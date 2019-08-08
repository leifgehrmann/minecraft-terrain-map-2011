import math

def getSize(image):
	return image.size;

def getRedAt(image,x,y):
	r = getPixelAt(image,x,y);
	return r;
def getGreenAt(image,x,y):
	r,g = getPixelAt(image,x,y);
	return g;
def getBlueAt(image,x,y):
	r,g,b = getPixelAt(image,x,y);
	return b;
	
def getPixelAt(image,x,y):
	dimensions = getSize(image);
	if x>= 0 and x<dimensions[0]:
		if y>= 0 and y<dimensions[1]:
			return image.getpixel((x,y));
	return [-1,-1,-1,-1];
	
def getHexAt(image,x,y):
	rgb = getPixelAt(image,x,y);
	rgb = [rgb[0],rgb[1],rgb[2]];
	return "".join(map(chr, rgb)).encode('hex')
def getBrightnessAt(image,x,y):
	r,g,b = getPixelAt(image,x,y);
	return math.sqrt(math.pow(r,2)+math.pow(g,2)+math.pow(b,2));
