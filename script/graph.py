import argparse
import json
import pathlib
import shutil
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict
from collections import ChainMap




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


    if isinstance(old_dict["mips_tcc"], list):

        print("old_dict is list!")
        old_dict = old_dict

    else:
        keys_to_keep = {"best_mips_tcc", "best_hash_tcc", "regressed_hash_tcc", "best_mips_gcc", "best_hash_gcc", "regressed_hash_gcc", "best_mips_llvm", "best_hash_llvm", "regressed_hash_llvm" }
        old_dict_keep = { key:value for key,value in old_dict.items() if key in keys_to_keep}
        keys_to_extract = {"mips_tcc", "Simulation_Time_tcc", "CPU_Time_tcc", "CPU_Cycle_tcc", "mips_gcc", "Simulation_Time_gcc", "CPU_Time_gcc", "CPU_Cycle_gcc", "mips_llvm", "Simulation_Time_llvm", "CPU_Time_llvm", "CPU_Cycle_llvm"}
        old_dict_extract = { key:value for key,value in old_dict.items() if key in keys_to_extract}
        dict_to_list_extract = old_dict_extract.items()
        old_dict_extract = defaultdict(list)
        # iterating over list of tuples
        for key, val in dict_to_list_extract:

            old_dict_extract[key].append(val)


        old_dict = dict(ChainMap(old_dict_keep, old_dict_extract))
        print(old_dict)


    to_plot = [ "mips", "Simulation_Time", "CPU_Time", "CPU_Cycle"]
    jit_engines = ["tcc", "gcc", "llvm"]
    graph_data = {}


    #maximum number of elements to be stored
    buffer_size = 50

    #getting commit number from dictionary

    commit = old_dict.get('commit_number',1)

    if commit <= buffer_size:
        for i in range(len(jit_engines)):
            for j in range(len(to_plot)):
              old_dict[f'{to_plot[j]}_{jit_engines[i]}'].append(new_dict.get(f'{to_plot[j]}_{jit_engines[i]}'))


    else:
        for i in range(len(jit_engines)):
            for j in range(len(to_plot)):
               old_dict[f'{to_plot[j]}_{jit_engines[i]}'].append(new_dict.get(f'{to_plot[j]}_{jit_engines[i]}'))
               old_dict[f'{to_plot[j]}_{jit_engines[i]}'].pop(0)




    old_dict["commit_number"] = commit + 1
    print(old_dict)

    with open(old_path, 'w') as f1:
            json.dump(old_dict, f1)




    #plotting mips


    commit_number = np.arange(0,old_dict['commit_number'],1)
    mips_tcc = np.array(old_dict["mips_tcc"])
    mips_gcc = np.array(old_dict["mips_gcc"])
    mips_llvm = np.array(old_dict["mips_llvm"])

    fig_mips = plt.figure()
    plt.plot(commit_number, mips_tcc)
    plt.plot(commit_number, mips_gcc)
    plt.plot(commit_number, mips_llvm)
    plt.legend(["MIPS_tcc", "MIPS_gcc", "MIPS_llvm"])
    plt.title('MIPS value for the last 50 commits')
    plt.xlabel('commit number')
    plt.ylabel('MIPS')

    fig_mips.savefig('/home/ge75guy/Desktop/etiss_new/script/mips.png')

    #plotting simulation time

    commit_number = np.arange(0,old_dict['commit_number'],1)
    Simulation_Time_tcc = np.array(old_dict["Simulation_Time_tcc"])
    Simulation_Time_gcc = np.array(old_dict["Simulation_Time_gcc"])
    Simulation_Time_llvm = np.array(old_dict["Simulation_Time_llvm"])

    fig_Simulation_Time = plt.figure()
    plt.plot(commit_number, Simulation_Time_tcc)
    plt.plot(commit_number, Simulation_Time_gcc)
    plt.plot(commit_number, Simulation_Time_llvm)
    plt.title('Simulation Time for the last 50 commits')
    plt.xlabel('commit number')
    plt.ylabel('Simulation Time')
    fig_Simulation_Time.savefig('Simulation_Time.png')



    #plotting CPU time

    commit_number = np.arange(0,old_dict['commit_number'],1)
    CPU_Time_tcc = np.array(old_dict["CPU_Time_tcc"])
    CPU_Time_gcc = np.array(old_dict["CPU_Time_gcc"])
    CPU_Time_llvm = np.array(old_dict["CPU_Time_llvm"])

    fig_CPU_Time = plt.figure()
    plt.plot(commit_number, CPU_Time_tcc)
    plt.plot(commit_number, CPU_Time_gcc)
    plt.plot(commit_number, CPU_Time_llvm)
    plt.title('CPU Time for the last 50 commits')
    plt.xlabel('commit number')
    plt.ylabel('CPU Time')
    fig_CPU_Time.savefig('CPU_Time.png')


    #plotting CPU Cycle

    commit_number = np.arange(0,old_dict['commit_number'],1)
    CPU_Cycle_tcc = np.array(old_dict["CPU_Cycle_tcc"])
    CPU_Cycle_gcc = np.array(old_dict["CPU_Cycle_gcc"])
    CPU_Cycle_llvm = np.array(old_dict["CPU_Cycle_llvm"])

    fig_CPU_Cycle = plt.figure()
    plt.plot(commit_number, CPU_Cycle_tcc)
    plt.plot(commit_number, CPU_Cycle_gcc)
    plt.plot(commit_number, CPU_Cycle_llvm)
    plt.title('CPU Cycle for the last 50 commits')
    plt.xlabel('commit number')
    plt.ylabel('CPU Cycle')
    fig_CPU_Cycle.savefig('CPU_Cycle.png')



    output_files = ['mips.png', 'Simulation_Time.png', 'CPU_Time.png', 'CPU_Cycle.png']



if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('new_file')
    parser.add_argument('old_file')
    args = parser.parse_args()

    main(args.new_file, args.old_file)










