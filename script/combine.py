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


        #replacing keys with jit engine attribute

        new_key_mips_tcc= 'mips_tcc'
        old_key_mips_tcc= 'mips'
        new_key_Simulation_Time_tcc= 'Simulation_Time_tcc'
        old_key_Simulation_Time_tcc= 'Simulation_Time'
        new_key_CPU_Time_tcc= 'CPU_Time_tcc'
        old_key_CPU_Time_tcc= 'CPU_Time'
        new_key_CPU_Cycle_tcc= 'CPU_Cycle_tcc'
        old_key_CPU_Cycle_tcc= 'CPU_cycle'
        dict_one[new_key_mips_tcc] = dict_one.pop(old_key_mips_tcc)
        dict_one[new_key_Simulation_Time_tcc] = dict_one.pop(old_key_Simulation_Time_tcc)
        dict_one[new_key_CPU_Time_tcc] = dict_one.pop(old_key_CPU_Time_tcc)
        dict_one[new_key_CPU_Cycle_tcc] = dict_one.pop(old_key_CPU_Cycle_tcc)

        print(dict_one)

        new_key_mips_gcc= 'mips_gcc'
        old_key_mips_gcc= 'mips'
        new_key_Simulation_Time_gcc= 'Simulation_Time_gcc'
        old_key_Simulation_Time_gcc= 'Simulation_Time'
        new_key_CPU_Time_gcc= 'CPU_Time_gcc'
        old_key_CPU_Time_gcc= 'CPU_Time'
        new_key_CPU_Cycle_gcc= 'CPU_Cycle_gcc'
        old_key_CPU_Cycle_gcc= 'CPU_cycle'
        dict_two[new_key_mips_gcc] = dict_two.pop(old_key_mips_gcc)
        dict_two[new_key_Simulation_Time_gcc] = dict_two.pop(old_key_Simulation_Time_gcc)
        dict_two[new_key_CPU_Time_gcc] = dict_two.pop(old_key_CPU_Time_gcc)
        dict_two[new_key_CPU_Cycle_gcc] = dict_two.pop(old_key_CPU_Cycle_gcc)


        print(dict_two)


        new_key_mips_llvm= 'mips_llvm'
        old_key_mips_llvm= 'mips'
        new_key_Simulation_Time_llvm= 'Simulation_Time_llvm'
        old_key_Simulation_Time_llvm= 'Simulation_Time'
        new_key_CPU_Time_llvm= 'CPU_Time_llvm'
        old_key_CPU_Time_llvm= 'CPU_Time'
        new_key_CPU_Cycle_llvm= 'CPU_Cycle_llvm'
        old_key_CPU_Cycle_llvm= 'CPU_cycle'
        dict_three[new_key_mips_llvm] = dict_three.pop(old_key_mips_llvm)
        dict_three[new_key_Simulation_Time_llvm] = dict_three.pop(old_key_Simulation_Time_llvm)
        dict_three[new_key_CPU_Time_llvm] = dict_three.pop(old_key_CPU_Time_llvm)
        dict_three[new_key_CPU_Cycle_llvm] = dict_three.pop(old_key_CPU_Cycle_llvm)

        print(dict_three)



        temp_dict = dict(list(dict_one.items()) + list(dict_two.items()) + list(dict_three.items()))

    final_dict = {k: round(v, 2) for k, v in temp_dict.items()}
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
