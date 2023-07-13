
import numpy as np
import random

def Get_clear_field(field_size):

	matrix = np.zeros((field_size, field_size))

	for i in range(field_size):
		matrix[i][0] = 1
		matrix[i][field_size - 1] = 1

		matrix[0][i] = 1
		matrix[field_size - 1][i] = 1

	return matrix

def Get_one_onbtacle_field(field_size):

	matrix = np.zeros((field_size, field_size))

	for i in range(field_size):
		matrix[i][0] = 1
		matrix[i][field_size - 1] = 1

		matrix[0][i] = 1
		matrix[field_size - 1][i] = 1

	for i in range(23, 40):
		matrix[i][28] = 1

	for j in range(28, 43):
		matrix[43][j] = 1

	for j in range(32, 43):
		matrix[15][j] = 1

	for i in range(5, 28):
		matrix[i][10] = 1

	return matrix

def Get_random_field(field_size, start, finish):

	matrix = np.zeros((field_size, field_size))

	for i in range(field_size):
		matrix[i][0] = 1
		matrix[i][field_size - 1] = 1

		matrix[0][i] = 1
		matrix[field_size - 1][i] = 1

	for i in range(field_size):
		for j in range(field_size):
			if random.random() < 0.3:
				if (j == start[1] and i == start[0]) or (j == finish[1] and i == finish[0]):
					continue
				matrix[j][i] = 1

	return matrix


def GetMazeField(field_size, start, finish):
	matrix = np.zeros((field_size, field_size))

	matrix[20][4] = 1
	matrix[20][46] = 1 

	for i in range(4, 47):
		matrix[21][i] = 1
		matrix[19][i] = 1

	matrix[21][20] = 1
	matrix[20][21] = 1
	matrix[12][21] = 1
	matrix[12][20] = 1
	matrix[12][22] = 1
	matrix[12][23] = 1
	matrix[24][20] = 1
	matrix[24][21] = 1
	matrix[24][22] = 1
	matrix[22][21] = 1
	matrix[20][44] = 1
	matrix[33][43] = 1
	matrix[33][45] = 1
	matrix[14][43] = 1
	matrix[33][8] = 1
	matrix[14][45] = 1
	matrix[31][34] = 1
	matrix[26][34] = 1
	matrix[14][36] = 1
	matrix[9][7] = 1
	matrix[10][38] = 1
	matrix[15][37] = 1
	matrix[21][45] = 1
	matrix[35][41] = 1
	matrix[34][48] = 1
	matrix[19][47] = 1


	for i in range(12, 19):
		matrix[i][19] = 1
		matrix[i][23] = 1

	for i in range(21, 25):
		matrix[i][19] = 1
		matrix[i][23] = 1
	
	for i in range(14, 19):	
		matrix[i][21] = 1

	for i in range(21, 34):	
		matrix[i][44] = 1
		matrix[i][42] = 1
		matrix[i][46] = 1

	for i in range(14, 19):
		matrix[i][42] = 1
		matrix[i][44] = 1
		matrix[i][46] = 1

	for i in range(21, 34):
		matrix[i][7] = 1
		matrix[i][9] = 1

	for i in range(9, 35):
		matrix[32][i] = 1
		matrix[30][i] = 1
		matrix[25][i] = 1
		matrix[27][i] = 1

	for i in range(21, 25):
		matrix[i][29] = 1
		matrix[i][31] = 1

	for i in range(23, 37):
		matrix[13][i] = 1
		matrix[15][i] = 1

	for i in range(9, 19):
		matrix[i][8] = 1
		matrix[i][6] = 1

	for i in range(8, 39):
		matrix[11][i] = 1
		matrix[9][i] = 1

	for i in range(12, 16):
		matrix[i][36] = 1
		matrix[i][38] = 1

	for i in range(21, 36):
		matrix[i][40] = 1
		matrix[i][42] = 1

	for i in range(42, 49):
		matrix[35][i] = 1
		matrix[33][i] = 1

	for i in range(19, 33):
		matrix[i][48] = 1

	matrix[19][20] = 0
	matrix[19][22] = 0
	matrix[21][20] = 0
	matrix[21][22] = 0
	matrix[21][43] = 0
	matrix[32][44] = 0
	matrix[19][43] = 0
	matrix[15][44] = 0
	matrix[21][8] = 0
	matrix[31][9] = 0
	matrix[26][9] = 0
	matrix[25][30] = 0
	matrix[21][30] = 0
	matrix[14][23] = 0
	matrix[19][7] = 0
	matrix[10][8] = 0
	matrix[11][37] = 0
	matrix[14][36] = 0
	matrix[21][41] = 0
	matrix[34][42] = 0
	matrix[33][47] = 0
	matrix[20][46] = 0
		

	return matrix