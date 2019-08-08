#!/usr/bin/python2.6 -tt

import sys
import random
import math

mcEditorLocation = "/Users/leifgehrmann/Documents/Programming/python/pymclevel/"
sys.path.append(mcEditorLocation)
import mclevel

# class definitions
class Column():
	
	def __init__(self,id):
		self.height = 0;
		self.displacement = 0;
		self.blockValues = [];
		self.blockData = [];
		self.identifier = id;
	def setDisplacement(self,d):
		self.displacement=d;
	def addBlockAndData(self,value,data):
		self.height+=1;
		self.blockValues.append(value);
		self.blockData.append(data);
	def addBlock(self,value):
		self.height+=1;
		self.blockValues.append(value);
		self.blockData.append(0);
	def getBlockValueAt(self,index):
		return self.blockValues[index];
	def getBlockDataAt(self,index):
		return self.blockData[index];

def getHeight(chunk,xPos,zPos):
	count=127
	height=127
	while (count>=0):
		if (chunk.Blocks[xPos,zPos,count]!=0):
			height=count;
			break;
		else:
			count=count-1;
	return height;

def replaceColumn(chunk,xPos,zPos,column):
	height = getHeight(chunk,xPos,zPos)+1;
	height-= column.displacement;
	index  = column.height-1;
	for i in range(height-column.height,height):
		if i>=0 and i<=127:
			chunk.Blocks[xPos,zPos,i] = column.getBlockValueAt(index);
			chunk.Data[xPos,zPos,i] = column.getBlockDataAt(index);
			index-=1;
	#if name == "Alice" or name =="nick":
	#	name = name + "???"	
	#print "hello", name 

def main():
	worldLocation = "/Users/leifgehrmann/Library/Application Support/minecraft/saves/"
	worldName = "OverworldTest"
	world = mclevel.fromFile(worldLocation+worldName);
	chunkPositions = list(world.allChunks);
	numberOfChunks = len(chunkPositions);
	numberOfChunks = 1;
	for i in range(0, numberOfChunks):
		xPos, zPos = chunkPositions[6];
		chunk = world.getChunk(xPos,zPos);
		c = Column(0);
		c.addBlockAndData(35,1);
		c.addBlockAndData(35,4);
		c.addBlock(17);
		for x in range(0,15):
			for z in range(0,15):
				replaceColumn(chunk,x,z,c);
		# chunk.Blocks[:,:,64:] = 0;
		chunk.chunkChanged();
	# world.generateLights();
	world.saveInPlace();
	if len(sys.argv) > 1:
		Hello(sys.argv[1])

if __name__ == "__main__":
	main()