import random
import matplotlib.pyplot as plt
import time

import numpy as np

from deap import base, algorithms
from deap import creator
from deap import tools

ONE_MAX_LENGTH = 100   

POPULATION_SIZE = 200   
P_CROSSOVER = 0.7       
P_MUTATION = 0.3        
MAX_GENERATIONS = 50    

def oneMaxFitness(individual):
    return sum(individual), 

def __main__():

    creator.create("FitnessMax", base.Fitness, weights = (1.0,))
    creator.create("Individual", list, fitness = creator.FitnessMax)

    toolbox = base.Toolbox()
    toolbox.register("zeroOrOne", random.randint, 0, 1)
    toolbox.register("individualCreator", tools.initRepeat, creator.Individual, toolbox.zeroOrOne, ONE_MAX_LENGTH)
    toolbox.register("populationCreator", tools.initRepeat, list, toolbox.individualCreator)

    toolbox.register("evaluate", oneMaxFitness)
    toolbox.register("select", tools.selTournament, tournsize = 3)
    toolbox.register("mate", tools.cxOnePoint)
    toolbox.register("mutate", tools.mutFlipBit, indpb = 1.0 / ONE_MAX_LENGTH)

    population = toolbox.populationCreator(n = POPULATION_SIZE)

    generationCounter = 0

    fitnessValues = list(map(oneMaxFitness, population))

    for individual, fitnessValue in zip(population, fitnessValues):
        individual.fitness.values = fitnessValue

    stats = tools.Statistics(lambda ind : ind.fitness.values)
    stats.register("max", np.max)
    stats.register("avg", np.mean)
    $stats.register("values", np.array)

    population, logbook = algorithms.eaSimple(population, toolbox, cxpb = P_CROSSOVER, mutpb = P_MUTATION, 
        ngen = MAX_GENERATIONS, stats = stats, verbose = True)

    maxFitnessValues, meanFitnessValues, vals = logbook.select("max", "avg", "values")

    plt.ion()
    fig, ax = plt.subplots()

    line, = ax.plot(vals[0], ' o', markersize = 1)
    ax.set_ylim(40, 110)

    for i in vals:
        line.set_ydata(i)

        plt.draw()
        plt.gcf().canvas.flush_events()

        time.sleep(0.5)

    plt.ioff()
    plt.show()

    plt.plot(maxFitnessValues, color='red')
    plt.plot(meanFitnessValues, color='green')
    plt.xlabel('Generation')
    plt.ylabel('Max/Avg Fintness')
    plt.show()

if(__name__ == '__main__'):
    __main__()
