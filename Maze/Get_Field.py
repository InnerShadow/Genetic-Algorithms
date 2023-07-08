
import numpy as np

def Get_clear_field(field_size):

	matrix = np.zeros((field_size, field_size))

	for i in range(field_size):
		matrix[i][0] = 1
		matrix[i][field_size - 1] = 1

		matrix[0][i] = 1
		matrix[field_size - 1][i] = 1

	return matrix
