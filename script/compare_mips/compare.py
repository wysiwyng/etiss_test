import argparse
import json
import pathlib
import shutil
from mako.template import Template



ISSUE_TEMPLATE = r''' **Status** (for commit ${current_hash})**:**
${message_tcc}\

**Current dhrystone MIPS for TCCJIT** **:** ${new_mips_tcc}\

**Previous best for TCCJIT** (recorded in commit ${best_hash})**:** ${best_mips_tcc}, difference ${f'{best_diff_tcc:+.2%}'}\


**Status** (for commit ${current_hash})**:**
${message_gcc}\

**Current dhrystone MIPS for GCCJIT** **:** ${new_mips_gcc}\

**Previous best for GCCJIT** (recorded in commit ${best_hash})**:** ${best_mips_gcc}, difference ${f'{best_diff_gcc:+.2%}'}\


**Status** (for commit ${current_hash})**:**
${message_llvm}\

**Current dhrystone MIPS for LLVMJIT** **:** ${new_mips_llvm}\

**Previous best for LLVMJIT** (recorded in commit ${best_hash})**:** ${best_mips_llvm}, difference ${f'{best_diff_llvm:+.2%}'}\

<sub>This comment was created automatically, please do not change!</sub>
'''

WIKI_TEMPLATE = r'''**Status** (for commit ${current_hash})**:**
${message_tcc}<br/>
**Current dhrystone MIPS for TCCJIT** **:** ${new_mips_tcc}<br/>
**Previous best for TCCJIT** (recorded in commit ${best_hash})**:** ${best_mips_tcc}, difference ${f'{best_diff_tcc:+.2%}'}<br/>
**Status** (for commit ${current_hash})**:**
${message_gcc}<br/>
**Current dhrystone MIPS for GCCJIT** **:** ${new_mips_gcc}<br/>
**Previous best for GCCJIT** (recorded in commit ${best_hash})**:** ${best_mips_gcc}, difference ${f'{best_diff_gcc:+.2%}'}<br/>
**Status** (for commit ${current_hash})**:**
${message_llvm}<br/>
**Current dhrystone MIPS for LLVMJIT** **:** ${new_mips_llvm}<br/>
**Previous best for LLVMJIT** (recorded in commit ${best_hash})**:** ${best_mips_llvm}, difference ${f'{best_diff_llvm:+.2%}'}
'''

HTML_TEMPLATE= r'''
<html>
<head>
<title>Performance Metrics</title>
</head>
<body>
<h1>Performance Metrics for the three JIT engines from the last commit</h1>
<p><b>Status</b> (for commit <a href=${link_to_current_hash}>${current_hash}</a>)<b>:</b>
${message_tcc}<br/>
<b>Current dhrystone MIPS for TCCJIT</b> <b>:</b> ${new_mips_tcc}<br/>
<b>Previous best for TCCJIT</b> (recorded in commit <a href=${link_to_old_best_hash_tcc}>${best_hash}</a>)<b>:</b> ${best_mips_tcc}, difference ${f'{best_diff_tcc:+.2%}'}<br/>
<b>Status</b> (for commit <a href=${link_to_current_hash}>${current_hash}</a>)<b>:</b>
${message_gcc}<br/>
<b>Current dhrystone MIPS for GCCJIT</b> <b>:</b> ${new_mips_gcc}<br/>
<b>Previous best for GCCJIT</b> (recorded in commit <a href=${link_to_old_best_hash_gcc}>${best_hash}</a>)<b>:</b> ${best_mips_gcc}, difference ${f'{best_diff_gcc:+.2%}'}<br/>
<b>Status</b> (for commit <a href=${link_to_current_hash}>${current_hash}</a>)<b>:</b>
${message_llvm}<br/>
<b>Current dhrystone MIPS for LLVMJIT</b> <b>:</b> ${new_mips_llvm}<br/>
<b>Previous best for LLVMJIT</b> (recorded in commit <a href=${link_to_old_best_hash_llvm}>${best_hash}</a>)<b>:</b> ${best_mips_llvm}, difference ${f'{best_diff_llvm:+.2%}'}</br>
</body>
</html>
'''

def main(new_file, old_file, current_hash, tolerance, no_update, repo_url):
    issue_template = Template(text=ISSUE_TEMPLATE)
    wiki_template = Template(text=WIKI_TEMPLATE)
    html_template = Template(text=HTML_TEMPLATE)

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

    print(type(old_dict["mips_tcc"]))
    print(type(new_dict["mips_tcc"]))





    jit_engines = ["tcc", "gcc", "llvm"]
    new_mips = [new_dict.get('mips_tcc'), new_dict.get('mips_gcc'), new_dict.get('mips_llvm')]
    best_mips = [old_dict.get('best_mips_tcc', 0.00000001), old_dict.get('best_mips_gcc', 0.00000001), old_dict.get('best_mips_llvm', 0.00000001)]
    best_hash = [old_dict.get('best_hash_tcc', None), old_dict.get('best_hash_gcc', None), old_dict.get('best_hash_llvm', None)]
    regressed_hash = [old_dict.get('regressed_hash_tcc', None), old_dict.get('regressed_hash_gcc', None), old_dict.get('regressed_hash_llvm', None)]
    old_best_hash = []
    message = []
    best_diff = []

    for i in range(len(jit_engines)):


        old_best_hash.append(best_hash[i])
        best_diff.append(new_mips[i] / best_mips[i] - 1)
        print("")
        print(best_diff)

        regressed = False
        current_hash = current_hash[:8]

        if best_diff[i] < -tolerance:
            print('major regression')
            if regressed_hash[i] is None:
              message.append(f'⚠ Major regression introduced! ⚠')
              regressed_hash[i] = current_hash
              print(regressed_hash)
            else:
              message.append(f'⚠ Major regression since commit {f"[{regressed_hash[i]}](https://github.com/{repo_url}/commit/{regressed_hash[i]})"} ⚠') #cannot put a dictionary value here :( )
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



        new_dict[f'best_mips_{jit_engines[i]}'] = best_mips[i]
        new_dict[f'best_hash_{jit_engines[i]}'] = best_hash[i]
        new_dict[f'regressed_hash_{jit_engines[i]}'] = regressed_hash[i]



    if not no_update:
        with open(new_path, 'w') as f1:
            json.dump(new_dict, f1)



    if repo_url:

        templates = [issue_template, wiki_template, html_template]
        output_files = ['mips_issue_text.md', 'mips_issue_text.html', 'wiki_text.md']
        link_to_current_hash = f"https://github.com/{repo_url}/commit/{current_hash}"
        link_to_old_best_hash_tcc = [f"https://github.com/{repo_url}/commit/{old_best_hash[0]}"]
        link_to_old_best_hash_gcc = [f"https://github.com/{repo_url}/commit/{old_best_hash[1]}"]
        link_to_old_best_hash_llvm = [f"https://github.com/{repo_url}/commit/{old_best_hash[2]}"]

        for index, fname in enumerate(output_files):
            with open(fname, 'w') as fw:
                fw.write(templates[index].render(

                    current_hash = current_hash,

                    link_to_current_hash = link_to_current_hash,

                    link_to_old_best_hash_tcc = link_to_old_best_hash_tcc,
                    link_to_old_best_hash_gcc = link_to_old_best_hash_gcc,
                    link_to_old_best_hash_llvm = link_to_old_best_hash_llvm,

                    best_hash_tcc = old_best_hash[0],
                    best_hash_gcc = old_best_hash[1],
                    best_hash_llvm = old_best_hash[2],

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
                    best_diff_llvm = best_diff[2],

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