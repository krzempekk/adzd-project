import numpy as np
import matplotlib.pyplot as plt
import sys

result_file = sys.argv[1] if len(sys.argv) > 1 else "results.csv"
plots_dir = sys.argv[2] if len(sys.argv) > 2 else "plots/"

PLOTS_COUNT = 1

data = np.genfromtxt(result_file, delimiter=';')

x = data[0, 1:]
y = data[1:, 1:]

labels = data[1:, 0]
speedup = [y[i, 0] / y[i] for i in range(PLOTS_COUNT)]
effectiveness = [speedup[i] / x for i in range(PLOTS_COUNT)]
karp_flatt = [(1 / speedup[i] - 1 / x) / (1 - 1 / x) for i in range(PLOTS_COUNT)]

print(x, y)

for i in range(PLOTS_COUNT):
    plt.plot(x, speedup[i])

plt.title("Speedup for tests on Kubernetes cluster")

plt.xlabel("Number of cores")
plt.xticks(x)

plt.ylabel("Speedup")
plt.yticks(x)

plt.grid(linestyle="--")
# plt.legend(title="Problem size")

plt.savefig(f"{plots_dir}/speedup.png")
plt.clf()

for i in range(PLOTS_COUNT):
    plt.plot(x, effectiveness[i])

plt.title("Effectiveness of tests on Kubernetes cluster")

plt.xlabel("Number of cores")
plt.xticks(x)

plt.ylabel("Effectiveness")
plt.yticks(np.arange(0, 1.2, 0.1))

plt.grid(linestyle="--")
# plt.legend(title="Problem size")

plt.savefig(f"{plots_dir}/effectiveness.png")
plt.clf()

for i in range(PLOTS_COUNT):
    plt.plot(x, karp_flatt[i])

plt.title("Karp-Flatt metric for tests on Kubernetes cluster")

plt.xlabel("Number of cores")
plt.xticks(x)

plt.ylabel("Karp-Flatt metric")

plt.grid(linestyle="--")
# plt.legend(title="Problem size")

plt.savefig(f"{plots_dir}/karp-flatt.png")
plt.clf()
