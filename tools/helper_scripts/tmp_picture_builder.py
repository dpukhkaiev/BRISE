__author__ = 'dmitrii'

def plot_evaluation():
    import matplotlib.pyplot as plt
    import mpl_toolkits.axisartist as AA
    savings = [0.679753524053]
    penalty = [0.123370314964]
    percent = [31.25]
    fig = plt.figure(1)
    ax = AA.Subplot(fig, 1, 1, 1)
    fig.add_subplot(ax)
    ax.set_xlim(0,100)
    ax.set_ylim(0,1)
    plt.plot(percent, savings, '-o', color="b", label="Energy savings [%]")
    plt.plot(percent, penalty, '-o', color ="r", label="Energy penalty [%]")
    plt.xlabel("Subset of data [%]")

    plt.legend(loc=1)
    plt.savefig("../evaluation/savings_penalty")
        #return

plot_evaluation()