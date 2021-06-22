import pathlib
import json
import argparse



# Valid for 5 test runs, have to change if necessary

def main(file_one, file_two, file_three, file_four, file_five):
    path_one = pathlib.Path(file_one)
    path_two = pathlib.Path(file_two)
    path_three = pathlib.Path(file_three)
    path_four = pathlib.Path(file_four)
    path_five = pathlib.Path(file_five)

    with open(path_one, 'r') as f1, open(path_two, 'r') as f2, open(path_three, 'r') as f3, open(path_four, 'r') as f4, open(path_five, 'r') as f5:
        dict_one = json.load(f1)
        dict_two = json.load(f2)
        dict_three = json.load(f3)
        dict_four = json.load(f4)
        dict_five = json.load(f5)

        new_mips_sum = dict_one['mips'] + dict_two['mips'] + dict_three['mips'] + dict_four['mips'] + dict_five['mips']
        new_mips = new_mips_sum/5
        dict_five['mips']= new_mips
        with open(path_five, 'w') as f5:
            json.dump(dict_five, f5)




if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('file_one')
    parser.add_argument('file_two')
    parser.add_argument('file_three')
    parser.add_argument('file_four')
    parser.add_argument('file_five')


    args = parser.parse_args()
    main(args.file_one, args.file_two, args.file_three, args.file_four, args.file_five)
