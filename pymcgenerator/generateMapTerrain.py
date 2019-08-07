#!/usr/bin/python2.6 -tt

import sys
import Image
import random
import math
import time
import datetime

mcEditorLocation = "/Users/leifgehrmann/Documents/Programming/python/pymceditor/"
sys.path.append(mcEditorLocation)
import Column
import Color
import ImgParse
import ElevationParse
import TerrainParse
import DepositParse

mcEditorLocation = "/Users/leifgehrmann/Documents/Programming/python/pymclevel/"
sys.path.append(mcEditorLocation)
import mclevel

def totalSeconds(td):
	return (td.microseconds + (td.seconds + td.days * 24 * 3600) * 10**6) / 10**6;

def selectColumn(columns):
	# print "-----";
	chance_net = 1;
	for column in columns:
		chance_ran = random.random()*chance_net;
		chance_cur = column.columnChance;
		# print chance_net, chance_cur;
		if chance_cur>=chance_ran:
			# print "Afrm";
			return column;
		else:
			# print "Fail";
			chance_net = chance_net-chance_cur;

def replaceColumn(chunk,xPos,yPos,elevation,column):
	height = elevation;
	height+= column.columnOffset;
	index  = column.columnHeight-1;
	for i in range(height-column.columnHeight,height):
		if i>=0 and i<=127:
			chunk.Blocks[xPos,yPos,i] = column.getBlockValueAt(index);
			chunk.Data[xPos,yPos,i] = column.getBlockDataAt(index);
			index-=1;
			
def InsertCube(chunk,xPos,yPos,zMax,block,size):
	if zMax>size+1:
		if xPos>16-size:
			xPos = 16-size;
		if yPos>16-size:
			yPos = 16-size;
		zPos = random.randint(size+1,zMax);
		for x in range(xPos,xPos+size):
			for y in range(yPos,yPos+size):
				if chunk.Blocks[x,y,zPos]==1:
					chunk.Blocks[x,y,zPos-size:zPos] = block;

def main():
	# START UP INFORMATION
	print "MAP TERRAIN GENERATOR";
	print "Description: This script opens a world, and uses images to generate";
	print "             custom terrain in the minecraft world. For more help";
	print "             see readme.txt.";
	print "- author : Leif Gehrmann";
	print "- date   : 2011.05.28";
	# REQUEST PARAMETERS
	# World selection
	worldName           = raw_input("Enter in World Name: ");
	worldLocation       = "/Users/leifgehrmann/Library/Application Support/minecraft/saves/"
	world = mclevel.fromFile(worldLocation+worldName);
	# Image information
	#infoElevation       = ElevationParse.getElevationInfo(raw_input("Enter in Elevation Info file: "));
	#infoTerrain         = TerrainParse.getTerrainInfo(raw_input("Enter in Terrain Info file: "));
	#infoDeposit         = DepositParse.getDepositInfo(raw_input("Enter in Deposit Info file: "));
	infoElevation      = ElevationParse.getElevationInfo("info/eart.txt");
	infoTerrain        = TerrainParse.getTerrainInfo("info/tart.txt");
	infoDeposit        = DepositParse.getDepositInfo("info/d.txt");
	# Image selection
	imageElevation      = Image.open(raw_input("Enter in Elevation Map: "));
	imageTerrain        = Image.open(raw_input("Enter in Terrain Map: "));
	#imageElevation      = Image.open("maps/E.58.006.png");
	#imageTerrain        = Image.open("maps/T.58.006.png");
	# Transformation parameters
 	imageOffset         = [0,0];
	imageOffsetText     = raw_input("Map Offset relative to World origin (x,y): ").split(',');
	imageOffset[0]      = int(imageOffsetText[0]);
	imageOffset[1]      = int(imageOffsetText[1]);
	# Final parameters
	relightText = raw_input("Should chunks be processed for light? (true,false): ")
	relight = False;
	if relightText in ['true', '1', 't', 'y', 'yes']:
		relight = True;
	
	# DOING SOME GEOMETRIC MATH
	# Here we get the variables for how many chunks need
	# to be accessed, so we don't do unnecessary work.
	imageDimensions = ImgParse.getSize(imageElevation);
	absoluteMinimumX = imageOffset[0];
	absoluteMinimumY = imageOffset[1];
	absoluteMaximumX = absoluteMinimumX + imageDimensions[0];
	absoluteMaximumY = absoluteMinimumY + imageDimensions[1];
	chunkMinimumX = absoluteMinimumX/16;
	chunkMinimumY = absoluteMinimumY/16;
	chunkMaximumX = absoluteMaximumX/16;
	chunkMaximumY = absoluteMaximumY/16;
	if absoluteMinimumX<0:
		chunkMinimumX = chunkMinimumX -1;
	if absoluteMinimumY<0:
		chunkMinimumY = chunkMinimumY -1;
	if absoluteMaximumX<0:
		chunkMaximumX = chunkMaximumX -1;
	if absoluteMaximumY<0:
		chunkMaximumY = chunkMaximumY -1;
	
	# PREPARE PROCESSING
	# Create Memory Variables so that we don't create and delete
	# space each time we do something.
	elevation = [[0 for _ in range(16)] for _ in range(16)];
	terrain = [[0 for _ in range(16)] for _ in range(16)];
	imagePosX = 0;
	imagePosY = 0;
	# Create variables of statistical value
	temporaryDelta = datetime.timedelta(days=356);
	worldTimingStart = datetime.datetime.now()
	worldTimingEnd   = datetime.datetime.now()
	worldRelightTimingStart = datetime.datetime.now()
	worldRelightTimingEnd   = datetime.datetime.now()
	worldRelightTimingTotal = datetime.timedelta(days=0);
	chunksTimingStart = datetime.datetime.now()
	chunksTimingEnd   = datetime.datetime.now()
	chunksTimingMaximum = 0;
	chunksTimingMinimum = 0;
	chunksCompleted = 0;
	chunksCompletedPercentage = 0;
	chunksTotal=(chunkMaximumX-chunkMinimumX+1)*(chunkMaximumY-chunkMinimumY+1);
	chunksPerPercentage = float(chunksTotal)/100;
	
	
	# PROCESSING
	for chunkPosX in range(chunkMinimumX, chunkMaximumX+1):
		for chunkPosY in range(chunkMinimumY, chunkMaximumY+1):
			chunksTimingStart = datetime.datetime.now()
			# fetch the chunk from the world
			try:
				world.createChunk(chunkPosY,-chunkPosX);
			except ValueError:
				pass
			chunk = world.getChunk(chunkPosY,-chunkPosX);
			# loop through each column of that particular chunk.
			for blockPosX in range(0, 16):
				for blockPosY in range(0, 16):
					# Get the image data for the particular chunk
					worldPosX = blockPosX + chunkPosX*16;
					worldPosY = blockPosY + chunkPosY*16;
					imgPosX = worldPosX - imageOffset[0];
					imgPosY = worldPosY - imageOffset[1];
					elevation[blockPosX][blockPosY] = ImgParse.getPixelAt(imageElevation,imgPosX,imgPosY);
					valid = not (elevation[blockPosX][blockPosY]==[-1,-1,-1,-1]) and not (elevation[blockPosX][blockPosY][3]==0);
					height = 0;
					if valid:
						terrain[blockPosX][blockPosY] = Color.HexStringToInt(ImgParse.getHexAt(imageTerrain,imgPosX,imgPosY));
					# Create Elevation & Bedrock
					if valid:
						height = int(float(elevation[blockPosX][blockPosY][0]*(infoElevation[1]-infoElevation[0])/256)+infoElevation[0]);
						chunk.Blocks[blockPosY,15-blockPosX,height-1:128] = 0;
						chunk.Blocks[blockPosY,15-blockPosX,0:height] = 24;
					# Create Terrain 
					if valid:
						column = Column.Column();
						if terrain[blockPosX][blockPosY] in infoTerrain:
							column = selectColumn(infoTerrain[terrain[blockPosX][blockPosY]]);
						else:
							column = selectColumn(infoTerrain[Color.getNearestColor(terrain[blockPosX][blockPosY],infoTerrain.keys())]);
						replaceColumn(chunk,blockPosY,15-blockPosX,height,column);
					# Create Deposits
					'''
					if valid and blockPosX<15 and blockPosY<15:
						index = 0;
						sum = 0;
						cur = 0;
						for i in range(0,8):
							sum += infoDeposit[2][i];
						cur = random.randint(0,sum);
						sum = 0;
						for i in range(0,8):
							sum += infoDeposit[2][i];
							if sum>cur:
								if infoDeposit[0][i]!=1:
									InsertCube(chunk,blockPosX,blockPosY,height-infoDeposit[1][i],infoDeposit[0][i],infoDeposit[3][0]);
								break;
					'''
			chunk.Blocks[0:16,0:16,0:infoElevation[2]] = 7;
			chunk.chunkChanged();
			chunksTimingEnd = datetime.datetime.now()
			temporaryDelta = chunksTimingEnd - chunksTimingStart;
			if chunksTimingMaximum < totalSeconds(temporaryDelta):
				chunksTimingMaximum = totalSeconds(temporaryDelta);
			if chunksTimingMinimum > totalSeconds(temporaryDelta):
				chunksTimingMinimum = totalSeconds(temporaryDelta);
			chunksCompleted = chunksCompleted + 1;
			if (math.floor(100*chunksCompleted/float(chunksTotal))>chunksCompletedPercentage):
				chunksCompletedPercentage = chunksCompletedPercentage+1;
				if relight:
					worldRelightTimingStart = datetime.datetime.now();
					world.generateLights();
					worldRelightTimingEnd   = datetime.datetime.now()
					worldRelightTimingTotal = worldRelightTimingTotal + (worldRelightTimingEnd - worldRelightTimingStart);
				world.saveInPlace();
				print chunksCompletedPercentage, "/ 100";
	if relight:
		world.generateLights();
	world.saveInPlace();
	worldTimingEnd = datetime.datetime.now()
	
	
	print "CONGRATULATIONS";
	print "The processing is now completed, here are a few statistics, so that";
	print "you have an idea of how long it takes to perform tasks on such a";
	print "large region.";
	print " ";
	print "Total Time              ", str(worldTimingEnd-worldTimingStart);
	print "Total Chunks            ", chunksTotal;
	print "Total Time per Chunk (s)", float(totalSeconds(worldTimingEnd-worldTimingStart))/float(chunksTotal);
	print "Minimum Time for a Chunk", chunksTimingMinimum;
	print "Maximum Time for a Chunk", chunksTimingMaximum;
	if relight:
		print "Total Time Relighting", str(worldRelightTimingTotal);
		print "Total Time Relighting per Chunk", float(totalSeconds(worldRelightTimingTotal))/float(chunksTotal);
	
	
if __name__ == "__main__":
	main()