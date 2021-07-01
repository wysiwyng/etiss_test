import pathlib
import json
import argparse


#program valid for three jit engines

def main(file_one, file_two, file_three): #can I make these variable?

    loop_iteration={
        "jit_engines" : ["TCC", "GCC", "LLVM"],
        "mips" : [],
        "Simulation_Time" : [],
        "CPU_Time" : [],
        "CPU_cycle" : []
    }

    results = {}
    json_files = [file_one, file_two, file_three]
    # path_one = pathlib.Path(file_one)
    # print(path_one)
    # path_two = pathlib.Path(file_two)
    # path_three = pathlib.Path(file_three)

    #path = [path_one, path_two, path_three]

    for index, fname in enumerate(json_files):

        with open(fname, 'r') as f:
            json_dict = json.load(f)
            json_dict = {k: round(v, 2) for k, v in json_dict.items()}
            loop_iteration["mips"].append(json_dict["mips"])
            loop_iteration["Simulation_Time"].append(json_dict["Simulation_Time"])
            loop_iteration["CPU_Time"].append(json_dict["CPU_Time"])
            loop_iteration["CPU_cycle"].append(json_dict["CPU_cycle"])
            results[f'mips_{loop_iteration["jit_engines"][index]}'] = loop_iteration["mips"][index]
            results[f'Simulation_Time_{loop_iteration["jit_engines"][index]}'] = loop_iteration["Simulation_Time"][index]
            results[f'CPU_Time_{loop_iteration["jit_engines"][index]}'] = loop_iteration["CPU_Time"][index]
            results[f'CPU_Cycle_{loop_iteration["jit_engines"][index]}'] = loop_iteration["CPU_cycle"][index]





    with open(file_one, 'w') as f1:
            json.dump(results, f1)


if __name__ == '__main__':
       parser = argparse.ArgumentParser()

       parser.add_argument('file_one')
       parser.add_argument('file_two')
       parser.add_argument('file_three')



       args = parser.parse_args()
       main(args.file_one, args.file_two, args.file_three)
