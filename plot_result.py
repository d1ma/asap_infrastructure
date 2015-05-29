import matplotlib.pyplot as plt
import sys


def plot_cdf(result_path, xlim=None):
    with open(result_path) as inf:
        x_str = inf.readlines()
    x_runs = [float(i) for i in x_str]

    x = sorted(x_runs)
    y = [float(i+1) / len(x) for i, _ in enumerate(x)]
    print x,y



    axes = plt.subplot()
    axes.plot(x,y, 'r')
    axes.set_xlim(xlim)
    plt.savefig(result_path + ".png")


if __name__ == "__main__":
    inp = sys.argv[1]
    xmin = 0
    xmax = .350
    plot_cdf(inp, xlim=[xmin, xmax])