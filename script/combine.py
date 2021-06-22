import pathlib
import json
import argparse


#program valid for three jit engines

def main(file_one, file_two, file_three): #can I make these variable?

    jit_engines = ["tcc", "gcc", "llvm"]
    dictionary = ["dict_one", "dict_two", "dict_three"]

    path_one = pathlib.Path(file_one)
    path_two = pathlib.Path(file_two)
    path_three = pathlib.Path(file_three)


    with open(path_one, 'r') as f1, open(path_two, 'r') as f2, open(path_three, 'r') as f3:


        dict_one = json.load(f1)
        dict_two = json.load(f2)
        dict_three = json.load(f3)
        dict_one = {k: round(v, 2) for k, v in dict_one.items()}
        dict_two = {k: round(v, 2) for k, v in dict_two.items()}
        dict_three = {k: round(v, 2) for k, v in dict_three.items()}


        #replacing keys with jit engine attribute

        #dict_one creation

        dict_one[f'mips_{jit_engines[0]}'] = dict_one.pop('mips')
        dict_one[f'Simulation_Time_{jit_engines[0]}'] = dict_one.pop('Simulation_Time')
        dict_one[f'CPU_Time_{jit_engines[0]}'] = dict_one.pop('CPU_Time')
        dict_one[f'CPU_Cycle_{jit_engines[0]}'] = dict_one.pop('CPU_Cycle')
        print(dict_one)

        #dict_two_creation

        dict_two[f'mips_{jit_engines[1]}'] = dict_two.pop('mips')
        dict_two[f'Simulation_Time_{jit_engines[1]}'] = dict_two.pop('Simulation_Time')
        dict_two[f'CPU_Time_{jit_engines[1]}'] = dict_two.pop('CPU_Time')
        dict_two[f'CPU_Cycle_{jit_engines[1]}'] = dict_two.pop('CPU_Cycle')
        print(dict_two)

        #dict_three_creation

        dict_three[f'mips_{jit_engines[2]}'] = dict_three.pop('mips')
        dict_three[f'Simulation_Time_{jit_engines[2]}'] = dict_three.pop('Simulation_Time')
        dict_three[f'CPU_Time_{jit_engines[2]}'] = dict_three.pop('CPU_Time')
        dict_three[f'CPU_Cycle_{jit_engines[2]}'] = dict_three.pop('CPU_Cycle')
        print(dict_three)



        final_dict = dict(list(dict_one.items()) + list(dict_two.items()) + list(dict_three.items()))


    print(final_dict)



    with open(path_one, 'w') as f1:
            json.dump(final_dict, f1)


if __name__ == '__main__':
       parser = argparse.ArgumentParser()

       parser.add_argument('file_one')
       parser.add_argument('file_two')
       parser.add_argument('file_three')



       args = parser.parse_args()
       main(args.file_one, args.file_two, args.file_three)
