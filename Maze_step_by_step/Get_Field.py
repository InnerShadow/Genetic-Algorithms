
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
			if random.random() < 0.2:
				if (j == start[1] and i == start[0]) or (j == finish[1] and i == finish[0]):
					continue
				matrix[j][i] = 1

	return matrix