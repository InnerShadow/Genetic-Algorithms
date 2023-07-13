from matplotlib.lines import Line2D
from matplotlib.patches import Rectangle
import numpy as np

def show_greed(ax, field, start, finish):
    ax.set_xlim(-2, len(field) + 3)
    ax.set_ylim(-2, len(field) + 3)

    ax.add_patch(Rectangle(start, 1, 1, facecolor = 'green'))
    ax.add_patch(Rectangle(finish, 1, 1, facecolor = 'red'))

    for i in range(len(field) + 1):
        ax.add_line(Line2D((i, i), (0, len(field)), color = '#aaa'))
        ax.add_line(Line2D((0, len(field)), (i, i), color = '#aaa'))

    for i in range(len(field)):
        for j in range(len(field)):
            if field[j][i] == 1:
                ax.add_patch(Rectangle((i, j), 1, 1, facecolor = 'black'))


def show_path(ax, best, field, start, finish, color, linewidth):
    ax.set_xlim(-2, len(field) + 3)
    ax.set_ylim(-2, len(field) + 3)

    currntX = start[1] + 0.5
    currntY = start[0] + 0.5
    for i in best:
        if i == 1:
            ax.add_line(Line2D((currntY, currntY + 1), (currntX, currntX), color = color, linewidth = linewidth))
            currntY += 1
        if i == 2:
            ax.add_line(Line2D((currntY, currntY - 1), (currntX, currntX), color = color, linewidth = linewidth))
            currntY -= 1
        if i == 3:
            ax.add_line(Line2D((currntY, currntY), (currntX, currntX + 1), color = color, linewidth = linewidth))
            currntX += 1
        if i == 4:
            ax.add_line(Line2D((currntY, currntY), (currntX, currntX - 1), color = color, linewidth = linewidth))
            currntX -= 1
        if currntX == finish[1] + 0.5 and currntY == finish[0] + 0.5:
            break

