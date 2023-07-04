from matplotlib.lines import Line2D
from random import randrange
import traceback
import logging 

xOffset = 0.0105
yOffset = 0.0205

posible_spots = (0, 1, 0.2, 0.4, 0.6, 0.8)

def show_graph(ax, best, start, Matrix, inf):

    if len(Matrix) == 6 :
        vertex = ((0, 1), (1, 1), (0.5, 0.8), (0.1, 0.5), (0.8, 0.2), (0.4, 0))
    else: 
        vertex = [[0 for x in range(2)] for y in range(len(Matrix))]
        for i in range(len(vertex)):
            x, y = randrange(len(posible_spots)), randrange(len(posible_spots))
            try:
                index = vertex.index((posible_spots[x], posible_spots[y]))
                i -= 1
                continue
            except Exception as e:
                vertex[i] = (posible_spots[x], posible_spots[y])

    vx = [v[0] for v in vertex]
    vy = [v[1] for v in vertex]

    for i in range(len(Matrix)) :
        for j in range(len(Matrix[i])) :
            if i != j and Matrix[i][j] != inf :
                #print(i, " ", j)
                ax.add_line(Line2D((vertex[i][0], vertex[j][0]), (vertex[i][1], vertex[j][1]), color = '#aaa'))
                ax.text((vertex[i][0] + vertex[j][0]) / 2, (vertex[i][1] + vertex[j][1]) / 2, str(Matrix[i][j]))                

    for i, v in enumerate(best):
        if i == start:
            continue

        prev = start
        v = v[:v.index(i) + 1]
        for j in v:
            ax.add_line(Line2D((vertex[prev][0], vertex[j][0]), (vertex[prev][1], vertex[j][1]), color = 'r'))
            prev = j

    ax.plot(vx, vy, ' ob', markersize = 15)

    for i in range(len(vertex)):
        if i != start:
            ax.text(vertex[i][0] - xOffset, vertex[i][1] - yOffset, str(i), fontsize = 15)
        else: 
            ax.text(vertex[i][0] - xOffset, vertex[i][1] - yOffset, str(i), fontsize = 15, color = 'r')

