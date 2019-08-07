import Image
import math
import struct

# @param integer Color, the RGB (not alpha)
# @param list    ColorList, a collection
# @return The nearest color (in int)
#         if fail, return -1 (this only
#		  should happen with empty lists)
def getNearestColor(color,colorList):
	apprx_val=-1;
	apprx_dif=16777216;
	# Extract RGB values from color
	sel_color_RGB=color;
	sel_color_R = Red(sel_color_RGB);
	sel_color_G = Green(sel_color_RGB);
	sel_color_B = Blue(sel_color_RGB);
	# Extract RGB values from each color
	# and compare them. Those with less
	# distance are recorded in 'apprx'
	cur_color_all = colorList;
	for i in range(len(cur_color_all)):
		cur_color_RGB=cur_color_all[i];
		cur_color_R = Red(cur_color_RGB);
		cur_color_G = Green(cur_color_RGB);
		cur_color_B = Blue(cur_color_RGB);
		# Calculate differences
		dif_val_R = math.pow(sel_color_R-cur_color_R,2);
		dif_val_G = math.pow(sel_color_G-cur_color_G,2);
		dif_val_B = math.pow(sel_color_B-cur_color_B,2);
		dif_val   = math.sqrt(dif_val_R+dif_val_G+dif_val_B);
		# Is this color closer?
		if dif_val <= apprx_dif:
			apprx_val = cur_color_all[i];
			apprx_dif = dif_val;
	return apprx_val;
def HexStringToInt(color_string):
	return int(color_string, 16);
def Red(color_int):
	return (color_int & 0xFF0000) >> 16;
def Green(color_int):
	return (color_int & 0x00FF00) >> 8;
def Blue(color_int):
	return (color_int & 0x0000FF);
def Alpha(color_int):
	return (color_int & 0x000000FF);
def IntToHexString(color_int):
	return hex(color_int)[2:];