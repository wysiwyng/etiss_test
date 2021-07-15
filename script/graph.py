import argparse
#import PIL
#from PIL import Image

import json
import pathlib
import shutil
import matplotlib
from numpy.core.fromnumeric import size
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
#from collections import defaultdict
#from collections import ChainMap




def main(file ): #, image):
    file_path = pathlib.Path(file)
    #image_path = pathlib.Path(image)



    if not file_path.exists(): #checks whether new path exists or not
        raise ValueError('file does not exist!')






    with open(file_path, 'r') as f1:
        file_dict = json.load(f1)


    to_plot = [ "mips", "Simulation_Time"]

    jit_engines = ["tcc", "gcc", "llvm"]
    #figure: svg image output
    #put commit hashes in xlabel, xaxis

    fig, axs = plt.subplots(nrows=1, ncols=2, figsize=(40,15))
    fig.suptitle('Performance Metrics', size=80)
    axs = axs.flatten()

    commit = file_dict["hash_count"]

    for j in range(len(to_plot)):

        for i in range(len(jit_engines)):

            axs[j].plot(commit, np.array(file_dict[f'{to_plot[j]}_{jit_engines[i]}']) )
            #axs[j].set_xticks(np.arange(len(commit)), commit)
            axs[j].set_xticks(np.arange(len(commit)))
            axs[j].set_xticklabels(commit)
            axs[j].tick_params(axis='x', rotation=45)
            for tick in axs[j].xaxis.get_major_ticks():
                tick.label.set_fontsize(10)
            for tick in axs[j].yaxis.get_major_ticks():
                tick.label.set_fontsize(20)
            axs[j].legend([f'{to_plot[j]}_{jit_engines[0]}', f'{to_plot[j]}_{jit_engines[1]}', f'{to_plot[j]}_{jit_engines[2]}'])
            axs[j].set_title(f'{to_plot[j]} value for the last 50 commits', size = 30)
            axs[j].set_xlabel('commt hash', size = 25)
            axs[j].set_ylabel(f'{to_plot[j]}', size = 25)



    image_format = 'svg'
    image_name = 'performance_metrics.svg'


    fig.savefig(image_name, format= image_format, dpi=1200)
    #command line arg

    # if not image_path.exists(): #checks whether new path exists or not
    #     print("no image file exists, assuming first image dump")
    #     shutil.copy(image_name, image_path)


    # with open(image_path, 'w') as f2:
    #         f2.write(fig.savefig(image_name, format= image_format, dpi=1200))





if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('file')
    #parser.add_argument('image')
    args = parser.parse_args()

    main(args.file)#, args.image)










