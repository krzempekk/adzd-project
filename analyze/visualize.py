import matplotlib.pyplot as plt
import numpy as np
import itertools

# figures (X)
# 0 - pawn
# 1 - knight
# 2 - bishop
# 3 - rook
# 4 - queen
# 5 - king

# colors (Y)
# 0 - black
# 1 - white

# heatmap for figure of color: X + Y * 6

figures = ["pawn", "knight", "bishop", "rook", "queen", "king"]
colors = ["black", "white"]
all_figures = list(map(lambda x: " ".join(x), itertools.product(colors, figures)))


def get_figure_index(figure_name):
    return all_figures.index(figure_name)


all_heatmaps = np.loadtxt('../output_1/heatmap_1.txt')
figure = 'black pawn'
heatmap = all_heatmaps[get_figure_index(figure)].reshape((8, 8))
heatmap = heatmap / heatmap.max()

print(heatmap)

plt.imshow(heatmap, cmap='hot', interpolation='nearest')

plt.xticks(range(8), ['%c' % x for x in range(65, 65 + 8)])
plt.yticks(range(8), range(8, 0, -1))

plt.title(f"Heatmap of {figure} position")

plt.colorbar()

plt.show()
