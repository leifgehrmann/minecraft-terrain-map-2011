class Column():
	def __init__(self):
		self.columnHeight = 0;
		self.columnOffset = 0;
		self.columnChance = 0;
		self.blockValues = [];
		self.blockData = [];
	def setColumnOffset(self,d):
		self.columnOffset=d;
	def setColumnChance(self,c):
		self.columnChance=c;
	def addBlockValueAndData(self,value,data):
		self.columnHeight+=1;
		self.blockValues.append(value);
		self.blockData.append(data);
	def addBlockValue(self,value):
		self.columnHeight+=1;
		self.blockValues.append(value);
		self.blockData.append(0);
	def getBlockValueAt(self,index):
		return self.blockValues[index];
	def getBlockDataAt(self,index):
		return self.blockData[index];