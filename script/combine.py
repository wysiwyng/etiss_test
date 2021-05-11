import pathlib
import json
import argparse

def main(file_one, file_two, file_three):
    path_one = pathlib.Path(file_one)
    path_two = pathlib.Path(file_two)
    path_three = pathlib.Path(file_three)


    with open(path_one, 'r') as f1, open(path_two, 'r') as f2, open(path_three, 'r') as f3:
        dict_one = json.load(f1)
        dict_two = json.load(f2)
        dict_three = json.load(f3)

        #deleting everything except mips

        del dict_one['Simulation_Time']
        del dict_one['CPU_Time']
        del dict_one['CPU_cycle']

        print(dict_one)

        del dict_two['Simulation_Time']
        del dict_two['CPU_Time']
        del dict_two['CPU_cycle']

        print(dict_two)

        del dict_three['Simulation_Time']
        del dict_three['CPU_Time']
        del dict_three['CPU_cycle']

        print(dict_three)

        #replacing keys with jit engine attribute

        new_key_tcc= 'mips_tcc'
        old_key_tcc= 'mips'
        dict_one[new_key_tcc] = dict_one.pop(old_key_tcc)

        print(dict_one)

        new_key_gcc= 'mips_gcc'
        old_key_gcc= 'mips'
        dict_two[new_key_gcc] = dict_two.pop(old_key_gcc)

        print(dict_two)

        new_key_llvm= 'mips_llvm'
        old_key_llvm= 'mips'
        dict_three[new_key_llvm] = dict_three.pop(old_key_llvm)

        print(dict_three)



        mips_dict =dict(list(dict_one.items()) + list(dict_two.items()) + list(dict_three.items()))

        print(mips_dict)

        with open(path_one, 'w') as f1:
            json.dump(mips_dict, f1)


if __name__ == '__main__':
       parser = argparse.ArgumentParser()

       parser.add_argument('file_one')
       parser.add_argument('file_two')
       parser.add_argument('file_three')



       args = parser.parse_args()
       main(args.file_one, args.file_two, args.file_three)
