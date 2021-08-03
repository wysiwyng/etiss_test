import json
import argparse
from collections import defaultdict
import pathlib

def main(files):


    loop_iteration=defaultdict(list)
    results = {}
    jit_engines = []
    for index, fname in enumerate(files):
        path_file = pathlib.Path(files[index])
        name_part_a, name_part_b, engine = path_file.stem.split('_')
        jit_engines.append(engine)

    for index, fname in enumerate(files):
        with open(fname, 'r') as f:
            json_dict = json.load(f)
            print(json_dict)
            json_dict = {k: round(v, 2) for k, v in json_dict.items()}
            loop_iteration["mips"].append(json_dict["mips"])
            loop_iteration["Simulation_Time"].append(json_dict["Simulation_Time"])
            loop_iteration["CPU_Time"].append(json_dict["CPU_Time"])
            loop_iteration["CPU_cycle"].append(json_dict["CPU_cycle"])
            results[f'mips_{jit_engines[index]}'] = loop_iteration["mips"][index]
            results[f'Simulation_Time_{jit_engines[index]}'] = loop_iteration["Simulation_Time"][index]
            results[f'CPU_Time_{jit_engines[index]}'] = loop_iteration["CPU_Time"][index]
            results[f'CPU_Cycle_{jit_engines[index]}'] = loop_iteration["CPU_cycle"][index]
    results["jit_engines"] = jit_engines
    print(results)
    with open(files[0], 'w') as f1:
            json.dump(results, f1)


if __name__ == '__main__':
       parser = argparse.ArgumentParser()
       parser.add_argument("files", nargs="+")
       args = parser.parse_args()
       main(args.files)