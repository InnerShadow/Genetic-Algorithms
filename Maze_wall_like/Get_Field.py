
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
	matrix[14][45] = 1


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

	matrix[19][20] = 0
	matrix[19][22] = 0
	matrix[21][20] = 0
	matrix[21][22] = 0
	matrix[21][43] = 0
	matrix[21][45] = 0
	matrix[32][44] = 0
	matrix[19][43] = 0
	matrix[15][44] = 0


		

	return matrix