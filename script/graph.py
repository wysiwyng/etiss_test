import argparse
import json
import pathlib
import matplotlib
from numpy.core.fromnumeric import size
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

def main(file ):
    file_path = pathlib.Path(file)
    if not file_path.exists():
        raise ValueError('file does not exist!')

    with open(file_path, 'r') as f1:
        file_dict = json.load(f1)

    to_plot = [ "mips", "Simulation_Time"]
    jit_engines = ["tcc", "gcc", "llvm"]
    fig, axs = plt.subplots(nrows=2, ncols=1, figsize=(40,40))
    fig.suptitle('Performance Metrics', size=80)
    axs = axs.flatten()

    commit = file_dict["hash_count"]

    for j in range(len(to_plot)):

        for i in range(len(jit_engines)):

            axs[j].plot(commit, np.array(file_dict[f'{to_plot[j]}_{jit_engines[i]}']) )
            axs[j].set_xticks(np.arange(len(commit)))
            axs[j].set_xticklabels(commit)
            axs[j].tick_params(axis='x', rotation=45)
            for tick in axs[j].xaxis.get_major_ticks():
                tick.label.set_fontsize(25)
            for tick in axs[j].yaxis.get_major_ticks():
                tick.label.set_fontsize(30)
            axs[j].legend([f'{to_plot[j]}_{jit_engines[0]}', f'{to_plot[j]}_{jit_engines[1]}', f'{to_plot[j]}_{jit_engines[2]}'], prop={"size":20})
            axs[j].set_title(f'{to_plot[j]} value for the last 50 commits', size = 30)
            axs[j].set_xlabel('commit hash', size = 25)
            axs[j].set_ylabel(f'{to_plot[j]}', size = 25)

    image_format = 'svg'
    image_name = 'performance_metrics.svg'

    fig.savefig(image_name, format= image_format, bbox_inches='tight',pad_inches = 0)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('file')

    args = parser.parse_args()

    main(args.file)









