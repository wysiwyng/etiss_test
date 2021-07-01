import argparse
import json
import pathlib
import shutil
import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict


def main(new_file, old_file):
    new_path = pathlib.Path(new_file)
    old_path = pathlib.Path(old_file)


    if not new_path.exists(): #checks whether new path exists or not
        raise ValueError('file does not exist!')

    if not old_path.exists():
        print('WARN: file  does not exist, assuming first entry to buffer')
        shutil.copy(new_path, old_path)

    with open(new_path, 'r') as f1, open(old_path, 'r') as f2:
        new_dict = json.load(f1)
        old_dict = json.load(f2)


    to_plot = [ "mips", "Simulation_Time", "CPU_Time", "CPU_Cycle"]
    jit_engines = ["TCC", "GCC", "LLVM"]
    graph_data = {}


    #converting dict to list
    dict_to_list = old_dict.items()

    #creating dictionary of lists
    old_dict = defaultdict(list)

    # iterating over list of tuples
    for key, val in dict_to_list:
        old_dict[key].append(val)

    #maximum number of elements to be stored
    buffer_size = 51

    #getting commit number from dictionary

    commit = old_dict.get('commit_number',0)

    if commit < buffer_size:
        for i in range(len(jit_engines)):
            old_dict[f'{to_plot[0]}_{jit_engines[i]}'].append(new_dict.get(f'{to_plot[0]}_{jit_engines[i]}'))
            old_dict[f'{to_plot[1]}_{jit_engines[i]}'].append(new_dict.get(f'{to_plot[1]}_{jit_engines[i]}'))
            old_dict[f'{to_plot[2]}_{jit_engines[i]}'].append(new_dict.get(f'{to_plot[2]}_{jit_engines[i]}'))
            old_dict[f'{to_plot[3]}_{jit_engines[i]}'].append(new_dict.get(f'{to_plot[3]}_{jit_engines[i]}'))

    else:
        for i in range(len(jit_engines)):
            old_dict[f'{to_plot[0]}_{jit_engines[i]}'].append(new_dict.get(f'{to_plot[0]}_{jit_engines[i]}'))
            old_dict[f'{to_plot[1]}_{jit_engines[i]}'].append(new_dict.get(f'{to_plot[1]}_{jit_engines[i]}'))
            old_dict[f'{to_plot[2]}_{jit_engines[i]}'].append(new_dict.get(f'{to_plot[2]}_{jit_engines[i]}'))
            old_dict[f'{to_plot[3]}_{jit_engines[i]}'].append(new_dict.get(f'{to_plot[3]}_{jit_engines[i]}'))
            old_dict[f'{to_plot[0]}_{jit_engines[i]}'].pop(0)
            old_dict[f'{to_plot[1]}_{jit_engines[i]}'].pop(0)
            old_dict[f'{to_plot[2]}_{jit_engines[i]}'].pop(0)
            old_dict[f'{to_plot[3]}_{jit_engines[i]}'].pop(0)



    old_dict["commit_number"] = commit + 1




    #plotting mips

    commit_number = np.arange(0,old_dict['commit_number']+1,1)
    mips_TCC = np.array(old_dict["mips_tcc"])
    mips_GCC = np.array(old_dict["mips_gcc"])
    mips_LLVM = np.array(old_dict["mips_llvm"])

    fig_mips = plt.figure()
    plt.plot(commit_number, mips_TCC)
    plt.plot(commit_number, mips_GCC)
    plt.plot(commit_number, mips_LLVM)
    plt.legend(["MIPS_TCC", "MIPS_GCC", "MIPS_LLVM"])
    plt.title('MIPS value for the last 50 commits')
    plt.xlabel('commit number')
    plt.ylabel('MIPS')

    fig_mips.savefig('mips.png')

    #plotting simulation time

    commit_number = np.arange(0,old_dict['commit_number']+1,1)
    Simulation_Time_TCC = np.array(old_dict["Simulation_Time_tcc"])
    Simulation_Time_GCC = np.array(old_dict["Simulation_Time_gcc"])
    Simulation_Time_LLVM = np.array(old_dict["Simulation_Time_llvm"])

    fig_Simulation_Time = plt.figure()
    plt.plot(commit_number, Simulation_Time_TCC)
    plt.plot(commit_number, Simulation_Time_GCC)
    plt.plot(commit_number, Simulation_Time_LLVM)
    plt.title('Simulation Time for the last 50 commits')
    plt.xlabel('commit number')
    plt.ylabel('Simulation Time')
    fig_Simulation_Time.savefig('Simulation_Time.png')



    #plotting CPU time

    commit_number = np.arange(0,old_dict['commit_number']+1,1)
    CPU_Time_TCC = np.array(old_dict["CPU_Time_tcc"])
    CPU_Time_GCC = np.array(old_dict["CPU_Time_gcc"])
    CPU_Time_LLVM = np.array(old_dict["CPU_Time_llvm"])

    fig_CPU_Time = plt.figure()
    plt.plot(commit_number, CPU_Time_TCC)
    plt.plot(commit_number, CPU_Time_GCC)
    plt.plot(commit_number, CPU_Time_LLVM)
    plt.title('CPU Time for the last 50 commits')
    plt.xlabel('commit number')
    plt.ylabel('CPU Time')
    fig_CPU_Time.savefig('CPU_Time.png')


    #plotting CPU Cycle

    commit_number = np.arange(0,old_dict['commit_number']+1,1)
    CPU_Cycle_TCC = np.array(old_dict["CPU_Cycle_tcc"])
    CPU_Cycle_GCC = np.array(old_dict["CPU_Cycle_gcc"])
    CPU_Cycle_LLVM = np.array(old_dict["CPU_Cycle_llvm"])

    fig_CPU_Cycle = plt.figure()
    plt.plot(commit_number, CPU_Cycle_TCC)
    plt.plot(commit_number, CPU_Cycle_GCC)
    plt.plot(commit_number, CPU_Cycle_LLVM)
    plt.title('CPU Cycle for the last 50 commits')
    plt.xlabel('commit number')
    plt.ylabel('CPU Cycle')
    fig_CPU_Cycle.savefig('CPU_Cycle.png')




if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('new_file')
    parser.add_argument('old_file')
    args = parser.parse_args()

    main(args.new_file, args.old_file)










