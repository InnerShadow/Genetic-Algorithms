import random
import matplotlib.pyplot as plt
import time

import numpy as np

from deap import base, algorithms
from deap import creator
from deap import tools

from Get_Elitizme import eaSimpleElitizme
from Show_path import show_path
from Get_Field import Get_test_field

FIELD_SIZE = 50

POPULATION_SIZE = 50
P_CROSSOVER = 0.9
P_MUTATION = 0.3
MAX_GENERATIONS = 50
HALL_OF_FAME_SIZE = 1

start = (3, 25)
finish = (45, 25)

# field:
	# 0 - avaliable cell
	# 1 - barrier

#path:
	# 0 - stay
	# 1 - up
	# 2 - down
	# 3 - right
	# 4 - left

def randomPath(total):
	path = []
	for n in range(total):
		ships.extend([random.randint(1, FIELD_SIZE), random.randint(1, FIELD_SIZE), random.randint(0, 1)])

	return creator.Individual(ships)

def __main__():
	field = Get_test_field(FIELD_SIZE)

	plt.ion()
	fig, ax = plt.subplots()
	fig.set_size_inches(6, 6)

	ax.set_xlim(-2, FIELD_SIZE + 3)
	ax.set_ylim(-2, FIELD_SIZE + 3)

	show_path(ax, (1, 1, 1, 1, 3, 3, 3, 2, 2, 4, 4, 4, 4, 4, 4), field, start, finish)

	plt.ioff()
	plt.show()

	#print(field)


if __name__ == '__main__':
	__main__()
