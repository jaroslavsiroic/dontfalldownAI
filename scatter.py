import sys
import pandas as pd
import matplotlib.pyplot as plt

def draw_scatter(path, save_name):
    print(path)
    print(save_name)
    df = pd.read_csv(path)
    df.set_index('Unnamed: 0', inplace=True)
    plot = df.plot.scatter('generation', 'fitness')
    plot.figure.savefig(save_name)

if __name__ == "__main__":
    if len(sys.argv) == 3:
        draw_scatter(str(sys.argv[1]), str(sys.argv[2]))