import pathlib
import json
import argparse

def main(files):

    path = []
    dict = []
    mips_value = []
    for index, value in enumerate(files):
        path.append(pathlib.Path(files[index]))

        with open(path[index], 'r') as file:
            dict.append(json.load(file))
        mips_value.append(dict[index]['mips'])

    average_mips = sum(mips_value)/len(mips_value)
    dict[0]['mips'] = average_mips

    with open(path[0], 'w') as file:
        json.dump(dict[0], file)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("files", nargs="+")
    args = parser.parse_args()
    main(args.files)
