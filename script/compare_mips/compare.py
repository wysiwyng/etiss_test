import argparse
import json
import pathlib
import shutil

from mako.template import Template

ISSUE_TEMPLATE = r'''**Status** (for commit ${current_hash})**:** ${message_tcc}

**Current dhrystone MIPS for TCCJIT** **:** ${new_mips_tcc}
**Previous best for TCCJIT** (recorded in commit ${best_hash_tcc})**:** ${best_mips_tcc}, difference ${f'{best_diff_tcc:+.2%}'}

**Status** (for commit ${current_hash})**:** ${message_gcc}

**Current dhrystone MIPS for GCCJIT** **:** ${new_mips_gcc}
**Previous best for GCCJIT** (recorded in commit ${best_hash_gcc})**:** ${best_mips_gcc}, difference ${f'{best_diff_gcc:+.2%}'}

**Status** (for commit ${current_hash})**:** ${message_llvm}

**Current dhrystone MIPS for LLVMJIT** **:** ${new_mips_llvm}
**Previous best for LLVMJIT** (recorded in commit ${best_hash_llvm})**:** ${best_mips_llvm}, difference ${f'{best_diff_llvm:+.2%}'}


<sub>This comment was created automatically, please do not change!</sub>
'''

def main(new_file_tcc, old_file_tcc, new_file_gcc, old_file_gcc, new_file_llvm, old_file_llvm, current_hash, tolerance, no_update):
    issue_template = Template(text=ISSUE_TEMPLATE)

    new_path_tcc = pathlib.Path(new_file_tcc)
    old_path_tcc = pathlib.Path(old_file_tcc)
    new_path_gcc = pathlib.Path(new_file_tcc)
    old_path_gcc = pathlib.Path(old_file_tcc)
    new_path_llvm = pathlib.Path(new_file_tcc)
    old_path_llvm = pathlib.Path(old_file_tcc)

    if not new_path_tcc.exists(): #checks whether new tcc path exists or not
        raise ValueError('tcc file to compare does not exist!')
    if not new_path_gcc.exists(): #checks whether new gcc path exists or not
        raise ValueError('gcc file to compare does not exist!')
    if not new_path_llvm.exists(): #checks whether new llvm path exists or not
        raise ValueError('llvm file to compare does not exist!')

    if not old_path_tcc.exists():
        print('WARN: tcc file to compare against does not exist, assuming first compare')
        shutil.copy(new_path_tcc, old_path_tcc)
    if not old_path_gcc.exists():
        print('WARN: gcc file to compare against does not exist, assuming first compare')
        shutil.copy(new_path_gcc, old_path_gcc)
    if not old_path_llvm.exists():
        print('WARN: llvm file to compare against does not exist, assuming first compare')
        shutil.copy(new_path_llvm, old_path_llvm)

    with open(new_path_tcc, 'r') as f_tcc_1, open(old_path_tcc, 'r') as f_tcc_2, open(new_path_gcc, 'r') as f_gcc_1, open(old_path_gcc, 'r') as f_gcc_2, open(new_path_llvm, 'r') as f_llvm_1, open(old_path_llvm, 'r') as f_llvm_2:
        new_dict_tcc = json.load(f_tcc_1)
        old_dict_tcc = json.load(f_tcc_2)
        new_dict_gcc = json.load(f_gcc_1)
        old_dict_gcc = json.load(f_gcc_2)
        new_dict_llvm = json.load(f_llvm_1)
        old_dict_llvm = json.load(f_llvm_2)


    #TCCJIT

    new_mips_tcc = new_dict_tcc['mips']

    old_best_mips_tcc = best_mips_tcc = old_dict_tcc.get('best_mips', 0.00000001)
    old_best_hash_tcc = best_hash_tcc = old_dict_tcc.get('best_hash', None)
    regressed_hash_tcc = old_dict_tcc.get('regressed_hash', None)
    best_diff_tcc = new_mips_tcc / best_mips_tcc - 1

    regressed_tcc = False

    if best_diff_tcc < -tolerance:
        message_tcc = f'TCC: ⚠ Major regression since commit {regressed_hash_tcc} ⚠'
        print('TCC: major regression')
        if regressed_hash_tcc is None:
            message_tcc = f'TCC : ⚠ Major regression introduced! ⚠'
            regressed_hash_tcc = current_hash
        regressed_tcc = True

    elif new_mips_tcc > best_mips_tcc:
        print('TCC: new best')
        message_tcc = '🥇 New best performance for TCCJIT!'
        best_mips_tcc = new_mips_tcc
        best_hash_tcc = current_hash
        regressed_hash_tcc = None

    else:
        if regressed_hash_tcc is not None:
            message_tcc = 'TCC: Regression cleared'
            print('TCC: regression cleared')
        else:
            message_tcc = 'No significant performance change for TCCJIT since last commit'
            print('no significant change for TCCJIT since last commit')
        regressed_hash_tcc = None

    new_dict_tcc['best_mips'] = best_mips_tcc
    new_dict_tcc['best_hash'] = best_hash_tcc
    new_dict_tcc['regressed_hash'] = regressed_hash_tcc

    if not no_update:
        with open(new_path_tcc, 'w') as f1:
            json.dump(new_dict_tcc, f1)


    #GCCJIT

    new_mips_gcc = new_dict_gcc['mips']

    old_best_mips_gcc = best_mips_gcc = old_dict_gcc.get('best_mips', 0.00000001)
    old_best_hash_gcc = best_hash_gcc = old_dict_gcc.get('best_hash', None)
    regressed_hash_gcc = old_dict_gcc.get('regressed_hash', None)
    best_diff_gcc = new_mips_gcc / best_mips_gcc - 1

    regressed_gcc = False

    if best_diff_gcc < -tolerance:
        message_gcc = f'GCC: ⚠ Major regression since commit {regressed_hash_gcc} ⚠'
        print('GCC: major regression')
        if regressed_hash_gcc is None:
            message_gcc = f'GCC: ⚠ Major regression introduced! ⚠'
            regressed_hash_gcc = current_hash
        regressed_gcc = True

    elif new_mips_gcc > best_mips_gcc:
        print('GCC: new best')
        message_gcc = '🥇 New best performance for GCCJIT!'
        best_mips_gcc = new_mips_gcc
        best_hash_gcc = current_hash
        regressed_hash_gcc = None

    else:
        if regressed_hash_gcc is not None:
            message_gcc = 'GCC: Regression cleared'
            print('GCC: regression cleared')
        else:
            message_gcc = 'No significant performance change for GCCJIT since last commit'
            print('no significant change for GCCJIT since last commit')
        regressed_hash_gcc = None

    new_dict_gcc['best_mips'] = best_mips_gcc
    new_dict_gcc['best_hash'] = best_hash_gcc
    new_dict_gcc['regressed_hash'] = regressed_hash_gcc

    if not no_update:
        with open(new_path_gcc, 'w') as f1:
            json.dump(new_dict_gcc, f1)

    #LLVMJIT
    new_mips_llvm = new_dict_llvm['mips']
    old_best_mips_llvm = best_mips_llvm = old_dict_llvm.get('best_mips', 0.00000001)
    old_best_hash_llvm = best_hash_llvm = old_dict_llvm.get('best_hash', None)
    regressed_hash_llvm = old_dict_llvm.get('regressed_hash', None)
    best_diff_llvm = new_mips_llvm / best_mips_llvm - 1

    regressed_llvm = False

    if best_diff_llvm < -tolerance:
        message_llvm = f'LLVM: ⚠ Major regression since commit {regressed_hash_llvm} ⚠'
        print('LLVM: major regression')
        if regressed_hash_llvm is None:
            message_llvm = f'LLVM: ⚠ Major regression introduced! ⚠'
            regressed_hash_llvm = current_hash
        regressed_llvm = True

    elif new_mips_llvm > best_mips_llvm:
        print('LLVM: new best')
        message_llvm = '🥇 New best performance for LLVMJIT!'
        best_mips_llvm = new_mips_llvm
        best_hash_llvm = current_hash
        regressed_hash_llvm = None

    else:
        if regressed_hash_llvm is not None:
            message_llvm = 'LLVM: Regression cleared'
            print('LLVM: regression cleared')
        else:
            message_llvm = 'No significant performance change for LLVMJIT since last commit'
            print('no significant change for LLVMJIT since last commit')
        regressed_hash_llvm = None

    new_dict_llvm['best_mips'] = best_mips_llvm
    new_dict_llvm['best_hash'] = best_hash_llvm
    new_dict_llvm['regressed_hash'] = regressed_hash_llvm

    if not no_update:
        with open(new_path_llvm, 'w') as f1:
            json.dump(new_dict_llvm, f1)



    with open('mips_issue_text.md', 'w') as f1:
        f1.write(issue_template.render(
            current_hash=current_hash,

            new_mips_tcc=new_mips_tcc,
            message_tcc=message_tcc,
            best_mips_tcc=old_best_mips_tcc,
            best_hash_tcc=old_best_hash_tcc,
            best_diff_tcc=best_diff_tcc,

            new_mips_gcc=new_mips_gcc,
            message_gcc=message_gcc,
            best_mips_gcc=old_best_mips_gcc,
            best_hash_gcc=old_best_hash_gcc,
            best_diff_gcc=best_diff_gcc,

            new_mips_llvm=new_mips_llvm,
            message_llvm=message_llvm,
            best_mips_llvm=old_best_mips_llvm,
            best_hash_llvm=old_best_hash_llvm,
            best_diff_llvm=best_diff_llvm
        ))



if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('new_file_tcc')
    parser.add_argument('old_file_tcc')
    parser.add_argument('new_file_gcc')
    parser.add_argument('old_file_gcc')
    parser.add_argument('new_file_llvm')
    parser.add_argument('old_file_llvm')
    parser.add_argument('git_commit_hash')
    parser.add_argument('-t', '--tolerance', default=0.2)
    parser.add_argument('-n', '--no_update', action='store_true')

    args = parser.parse_args()

    main(args.new_file_tcc, args.old_file_tcc, args.new_file_gcc, args.old_file_gcc, args.new_file_llvm, args.old_file_llvm, args.git_commit_hash, args.tolerance, args.no_update)