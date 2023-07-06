from matplotlib.lines import Line2D
from matplotlib.patches import Rectangle
import numpy as np

v_ship = np.array([0, 1, 2, 3])
h_ship = np.array([0, 0, 0, 0])
type_ship = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]
colors = ['g', 'b', 'm', 'y']

inf = 100

def show_ships(ax, best, field_size):
    rect = Rectangle((0, 0), field_size + 1, field_size + 1, fill = None, edgecolor = 'r')

    for i in range(field_size + 1):
        ax.add_line(Line2D((i + 0.5, i + 0.5), (0 + 0.5, field_size+ 0.5), color = '#aaa'))
        ax.add_line(Line2D((0 + 0.5, field_size + 0.5), (i + 0.5, i + 0.5), color = '#aaa'))

    t_n = 0
    for i in range(0, len(best), 3):
        x = best[i]
        y = best[i + 1]
        r = best[i + 2]
        t = type_ship[t_n]
        t_n += 1

        if r == 1:
            ax.plot(v_ship[:t] + x, h_ship[:t] + y, ' sb', markersize = 18, alpha = 0.8, markerfacecolor = colors[t - 1])
        else:
            ax.plot(h_ship[:t] + x, v_ship[:t] + y, ' sb', markersize = 18, alpha = 0.8, markerfacecolor = colors[t - 1])

    ax.add_patch(rect)

    P0 = np.zeros((field_size, field_size))
    P = np.ones((field_size + 6, field_size + 6)) * inf
    P[1:field_size + 1, 1:field_size + 1] = P0

    th = 1
    h = np.ones((3, 6)) * th
    ship_one = np.ones((1, 4)) * 10
    v = np.ones((6, 3)) * th

    for *ship, t in zip(*[iter(best)] * 3, type_ship):
        if ship[-1] == 0:
            sh = np.copy(h[:, :t + 2])
            sh[1, 1:t + 1] = ship_one[0, :t]
            P[ship[0] - 1:ship[0] + 2, ship[1] - 1:ship[1] + t + 1] += sh
        else:
            sh = np.copy(v[:t + 2, :])
            sh[1:t + 1, 1] = ship_one[0, :t]
            P[ship[0] - 1:ship[0] + t + 1, ship[1] - 1:ship[1] + 2] += sh


    # for i in range(len(P)):
    #     for j in range(len(P[i])):
    #         if P[i][j] > 0 and P[i][j] < 10:
    #             P[i][j] = 1
    #         if P[i][j] >= 20 and i != 0 and j != 0 and i <= 10 and j <= 10:
    #             P[i][j] += 200
    #         if P[i][j] % 10 != 0 and P[i][j] >= 10 and i != 0 and j != 0 and i <= 10 and j <= 10:
    #             P[i][j] += 50
    #         if (i == 0 or j == 0 or i > 10 or j > 10) and (P[i][j] < 110):
    #             P[i][j] = 100


    # s = 0
    # for i in range(len(P)):
    #     for j in range(len(P[i])):
    #         if i != 0 and j != 0 and i <= 10 and j <= 10:
    #             s += P[i][j]
    #         else:
    #             if P[i][j] >= inf + 10:
    #                 s += P[i][j] 


    # print(P, "\n\n", s, "\n")

