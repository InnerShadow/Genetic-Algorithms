from matplotlib.lines import Line2D

vertex = ((0, 1), (1, 1), (0.5, 0.8), (0.1, 0.5), (0.8, 0.2), (0.4, 0))

xOffset = 0.0105
yOffset = 0.0205

vx = [v[0] for v in vertex]
vy = [v[1] for v in vertex]

def show_graph(ax, best, start, Matrix, inf):

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
        ax.text(vertex[i][0] - xOffset, vertex[i][1] - 0.0205, str(i), fontsize = 15)
