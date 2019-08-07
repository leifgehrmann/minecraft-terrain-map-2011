import sys
mcEditorLocation = "/Users/leifgehrmann/Documents/Programming/python/minecraftTerrainEditor/"
sys.path.append(mcEditorLocation)
import Column
import Color

def getTerrainInfo(fileName):
  	file = open(fileName);
  	terrainInfo = dict();
	while 1:
		lines = file.readlines(100000)
		if not lines:
			break;
		for line in lines:
			if line.find("#")==0:
				pass;
			else:
				# Parse data
				data = line.split(",");
				data_color = Color.HexStringToInt(data[0]);
				data_column_chance  = float(data[1]);
				data_column_offset  = int(data[2]);
				
				# Create new Column
				column=Column.Column();
				column.setColumnChance(data_column_chance);
				column.setColumnOffset(data_column_offset);
				
				# Add data to column
				for i in range(3,len(data),2):
					column.addBlockValueAndData(int(data[i]),int(data[i+1]));
				
				# Add column to the dictionary. If key already exists,
				# append to the column array already in it.
				if data_color in terrainInfo:
					terrainInfo[data_color].append(column);
				else:
					columns = [column];
					terrainInfo[data_color] = columns;
	return terrainInfo;