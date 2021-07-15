import argparse
import json
import pathlib
import shutil
from mako.template import Template
from collections import defaultdict
from collections import ChainMap




ISSUE_TEMPLATE = r''' **Status** (for commit ${current_hash})**:**
${message_tcc}\

**Current dhrystone MIPS for TCCJIT** **:** ${new_mips_tcc}\

**Previous best for TCCJIT** (recorded in commit ${best_hash_tcc})**:** ${best_mips_tcc}, difference ${f'{best_diff_tcc}'}\


**Status** (for commit ${current_hash})**:**
${message_gcc}\

**Current dhrystone MIPS for GCCJIT** **:** ${new_mips_gcc}\

**Previous best for GCCJIT** (recorded in commit ${best_hash_gcc})**:** ${best_mips_gcc}, difference ${f'{best_diff_gcc}'}\


**Status** (for commit ${current_hash})**:**
${message_llvm}\

**Current dhrystone MIPS for LLVMJIT** **:** ${new_mips_llvm}\

**Previous best for LLVMJIT** (recorded in commit ${best_hash_llvm})**:** ${best_mips_llvm}, difference ${f'{best_diff_llvm}'}\

<sub>This comment was created automatically, please do not change!</sub>
'''

WIKI_TEMPLATE = r'''**Performance Metrics**
<br/>
<br/>
<br/>
**Status for the TCC Just-In-Time Engine** (for commit ${current_hash_wiki})**:**
${message_tcc}
<br/>
<br/>
**Current dhrystone MIPS for TCCJIT** **:** ${new_mips_tcc}
<br/>
<br/>
**Previous best for TCCJIT** (recorded in commit ${best_hash_tcc_wiki})**:** ${best_mips_tcc}, difference ${f'{best_diff_tcc}'}
<br/>
<br/>
<br/>
**Status for the GCC Just-In-Time Engine** (for commit ${current_hash_wiki})**:**
${message_gcc}
<br/>
<br/>
**Current dhrystone MIPS for GCCJIT** **:** ${new_mips_gcc}
<br/>
<br/>
**Previous best for GCCJIT** (recorded in commit ${best_hash_gcc_wiki})**:** ${best_mips_gcc}, difference ${f'{best_diff_gcc}'}
<br/>
<br/>
<br/>
**Status for the LLVM Just-In-Time Engine** (for commit ${current_hash_wiki})**:**
${message_llvm}
<br/>
<br/>
**Current dhrystone MIPS for LLVMJIT** **:** ${new_mips_llvm}
<br/>
<br/>
**Previous best for LLVMJIT** (recorded in commit ${best_hash_llvm_wiki})**:** ${best_mips_llvm}, difference ${f'{best_diff_llvm}'}
<br/>
<br/>
<br/>

**Graphical Analysis for the last 50 commits:**
<br/>
<br/>
[[performance_metrics.svg]]


'''



def main(new_file, old_file, current_hash, tolerance, no_update, repo_url):
    issue_template = Template(text=ISSUE_TEMPLATE)
    wiki_template = Template(text=WIKI_TEMPLATE)


    new_path = pathlib.Path(new_file)
    old_path = pathlib.Path(old_file)


    if not new_path.exists(): #checks whether new path exists or not
        raise ValueError('file to compare does not exist!')

    if not old_path.exists():
        print('WARN: file to compare against does not exist, assuming first compare')
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
    new_mips = [new_dict.get('mips_tcc'), new_dict.get('mips_gcc'), new_dict.get('mips_llvm')]
    best_mips = [old_dict.get('best_mips_tcc', 0.00000001), old_dict.get('best_mips_gcc', 0.00000001), old_dict.get('best_mips_llvm', 0.00000001)]
    best_hash = [old_dict.get('best_hash_tcc', None), old_dict.get('best_hash_gcc', None), old_dict.get('best_hash_llvm', None)]
    regressed_hash = [old_dict.get('regressed_hash_tcc', None), old_dict.get('regressed_hash_gcc', None), old_dict.get('regressed_hash_llvm', None)]
    old_best_hash = []
    message = []

    best_diff = []

    current_hash=current_hash[:8]
    old_best_mips = best_mips

    #maximum number of elements to be stored
    buffer_size = 50

    #getting commit number from dictionary

    commit = len(old_dict['mips_tcc'])#old_dict.get('commit_number',1)
    print("commit")
    print(commit)

    if commit <= buffer_size:
        old_dict["hash_count"].append(current_hash)
        for i in range(len(jit_engines)):
            for j in range(len(to_plot)):
              old_dict[f'{to_plot[j]}_{jit_engines[i]}'].append(new_dict.get(f'{to_plot[j]}_{jit_engines[i]}'))



    else:
        old_dict["hash_count"].append(current_hash)
        old_dict["hash_count"].pop(0)
        for i in range(len(jit_engines)):
            for j in range(len(to_plot)):
               old_dict[f'{to_plot[j]}_{jit_engines[i]}'].append(new_dict.get(f'{to_plot[j]}_{jit_engines[i]}'))
               old_dict[f'{to_plot[j]}_{jit_engines[i]}'].pop(0)





    for i in range(len(jit_engines)):


        old_best_hash.append(best_hash[i])
        best_diff.append(new_mips[i] / best_mips[i] - 1)
        print("")
        print(best_diff)

        regressed = False


        if best_diff[i] < -tolerance:
            print('major regression')
            if regressed_hash[i] is None:
              message.append(f'⚠ Major regression introduced! ⚠')
              regressed_hash[i] = current_hash
              print(regressed_hash)
            else:
              message.append(f'⚠ Major regression since commit  {f"[{regressed_hash[i]}](https://github.com/{repo_url}/commit/{regressed_hash[i]})"} ⚠')
              regressed = True


        elif new_mips[i] > best_mips[i]:
            print('new best')
            message.append(f'🥇 New best performance!')
            best_mips[i] = new_mips[i]
            best_hash[i] = current_hash
            regressed_hash[i] = None

        else:
            if regressed_hash[i] is not None:
                message.append('Regression cleared')

            else:
                message.append(f'No significant performance change.')
                print('no significant change')
                regressed_hash[i] = None



        old_dict[f'best_mips_{jit_engines[i]}'] = best_mips[i]
        old_dict[f'best_hash_{jit_engines[i]}'] = best_hash[i]
        old_dict[f'regressed_hash_{jit_engines[i]}'] = regressed_hash[i]


    print(old_dict)


    if not no_update:
        with open(new_path, 'w') as f1:
            json.dump(old_dict, f1)



    if repo_url:

        templates = [issue_template, wiki_template]
        output_files = ['mips_issue_text.md', 'wiki_text.md']
        best_hash_tcc_wiki = f"[{old_best_hash[0]}](https://github.com/{repo_url}/commit/{old_best_hash[0]})"
        best_hash_gcc_wiki = f"[{old_best_hash[1]}](https://github.com/{repo_url}/commit/{old_best_hash[1]})"
        best_hash_llvm_wiki = f"[{old_best_hash[2]}](https://github.com/{repo_url}/commit/{old_best_hash[2]})"
        current_hash_wiki = f"[{current_hash}](https://github.com/{repo_url}/commit/{current_hash})"


        for index, fname in enumerate(output_files):
            with open(fname, 'w') as fw:
                fw.write(templates[index].render(

                    current_hash = current_hash,
                    current_hash_wiki = current_hash_wiki,

                    best_hash_tcc = old_best_hash[0],
                    best_hash_gcc = old_best_hash[1],
                    best_hash_llvm = old_best_hash[2],

                    best_hash_tcc_wiki = best_hash_tcc_wiki,
                    best_hash_gcc_wiki = best_hash_gcc_wiki,
                    best_hash_llvm_wiki = best_hash_llvm_wiki,

                    new_mips_tcc = new_mips[0],
                    new_mips_gcc = new_mips[1],
                    new_mips_llvm = new_mips[2],

                    message_tcc = message[0],
                    message_gcc = message[1],
                    message_llvm = message[2],

                    best_mips_tcc = best_mips[0],
                    best_mips_gcc = best_mips[1],
                    best_mips_llvm = best_mips[2],

                    best_diff_tcc = best_diff[0],
                    best_diff_gcc = best_diff[1],
                    best_diff_llvm = best_diff[2]

                ))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('new_file')
    parser.add_argument('old_file')
    parser.add_argument('git_commit_hash')
    parser.add_argument('-t', '--tolerance', default=0.2)
    parser.add_argument('-n', '--no_update', action='store_true')
    parser.add_argument('-r', '--repo_url')


    args = parser.parse_args()

    main(args.new_file, args.old_file, args.git_commit_hash, args.tolerance, args.no_update, args.repo_url)