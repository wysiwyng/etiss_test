import argparse
import json
import pathlib
import shutil

from mako.template import Template

ISSUE_TEMPLATE = r''' **Status** (for commit ${current_hash})**:**
${message_TCC}\

**Current dhrystone MIPS for TCCJIT** **:** ${new_mips_TCC}\

**Previous best for TCCJIT** (recorded in commit ${best_hash})**:** ${best_mips_TCC}, difference ${f'{best_diff_TCC:+.2%}'}\


**Status** (for commit ${current_hash})**:**
${message_GCC}\

**Current dhrystone MIPS for GCCJIT** **:** ${new_mips_GCC}\

**Previous best for GCCJIT** (recorded in commit ${best_hash})**:** ${best_mips_GCC}, difference ${f'{best_diff_GCC:+.2%}'}\


**Status** (for commit ${current_hash})**:**
${message_LLVM}\

**Current dhrystone MIPS for LLVMJIT** **:** ${new_mips_LLVM}\

**Previous best for LLVMJIT** (recorded in commit ${best_hash})**:** ${best_mips_LLVM}, difference ${f'{best_diff_LLVM:+.2%}'}\

<sub>This comment was created automatically, please do not change!</sub>
'''

WIKI_TEMPLATE = r'''**Status** (for commit ${current_hash})**:**
${message_TCC}<br/>
**Current dhrystone MIPS for TCCJIT** **:** ${new_mips_TCC}<br/>
**Previous best for TCCJIT** (recorded in commit ${best_hash})**:** ${best_mips_TCC}, difference ${f'{best_diff_TCC:+.2%}'}<br/>
**Status** (for commit ${current_hash})**:**
${message_GCC}<br/>
**Current dhrystone MIPS for GCCJIT** **:** ${new_mips_GCC}<br/>
**Previous best for GCCJIT** (recorded in commit ${best_hash})**:** ${best_mips_GCC}, difference ${f'{best_diff_GCC:+.2%}'}<br/>
**Status** (for commit ${current_hash})**:**
${message_LLVM}<br/>
**Current dhrystone MIPS for LLVMJIT** **:** ${new_mips_LLVM}<br/>
**Previous best for LLVMJIT** (recorded in commit ${best_hash})**:** ${best_mips_LLVM}, difference ${f'{best_diff_LLVM:+.2%}'}
'''

HTML_TEMPLATE= r'''
<html>
<head>
<title>Performance Metrics</title>
</head>
<body>
<h1>Performance Metrics for the three JIT engines from the last commit</h1>
<p><b>Status</b> (for commit <a href=${link_to_current_hash}>${current_hash}</a>)<b>:</b>
${message_TCC}<br/>
<b>Current dhrystone MIPS for TCCJIT</b> <b>:</b> ${new_mips_TCC}<br/>
<b>Previous best for TCCJIT</b> (recorded in commit <a href=${link_to_old_best_hash_TCC}>${best_hash}</a>)<b>:</b> ${best_mips_TCC}, difference ${f'{best_diff_TCC:+.2%}'}<br/>
<b>Status</b> (for commit <a href=${link_to_current_hash}>${current_hash}</a>)<b>:</b>
${message_GCC}<br/>
<b>Current dhrystone MIPS for GCCJIT</b> <b>:</b> ${new_mips_GCC}<br/>
<b>Previous best for GCCJIT</b> (recorded in commit <a href=${link_to_old_best_hash_GCC}>${best_hash}</a>)<b>:</b> ${best_mips_GCC}, difference ${f'{best_diff_GCC:+.2%}'}<br/>
<b>Status</b> (for commit <a href=${link_to_current_hash}>${current_hash}</a>)<b>:</b>
${message_LLVM}<br/>
<b>Current dhrystone MIPS for LLVMJIT</b> <b>:</b> ${new_mips_LLVM}<br/>
<b>Previous best for LLVMJIT</b> (recorded in commit <a href=${link_to_old_best_hash_LLVM}>${best_hash}</a>)<b>:</b> ${best_mips_LLVM}, difference ${f'{best_diff_LLVM:+.2%}'}</br>
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

    loop_iteration = {

    "jit_engines" : ["TCC", "GCC", "LLVM"],
    "new_mips" : [new_dict.get('mips_TCC'), new_dict.get('mips_GCC'), new_dict.get('mips_LLVM')],
    "best_mips" : [old_dict.get('best_mips_TCC', 0.00000001), old_dict.get('best_mips_GCC', 0.00000001), old_dict.get('best_mips_LLVM', 0.00000001)],
    #"best_hash" : [old_dict.get('best_hash_TCC', None), old_dict.get('best_hash_GCC', None), old_dict.get('best_hash_LLVM', None)],
    #"regressed_hash" : [old_dict.get('regressed_hash_TCC', None)[:8], old_dict.get('regfressed_hash_GCC', None)[:8], old_dict.get('regressed_hash_LLVM', None)[:8]],
    #"old_best_hash" : [],
    "message" : [],
    "best_diff" : []
    }


    best_hash = [old_dict.get('best_hash_TCC', None), old_dict.get('best_hash_GCC', None), old_dict.get('best_hash_LLVM', None)],
    regressed_hash = [old_dict.get('regressed_hash_TCC', None)[:8], old_dict.get('regfressed_hash_GCC', None)[:8], old_dict.get('regressed_hash_LLVM', None)[:8]]
    old_best_hash = []



    for i in range(len(loop_iteration["jit_engines"])):


        old_best_hash.append(loop_iteration["best_hash"][i])
        loop_iteration["best_diff"].append(loop_iteration["new_mips"][i] / loop_iteration["best_mips"][i] - 1)
        regressed = False
        current_hash = current_hash[:8]


        if loop_iteration["best_diff"][i] < -tolerance:
            print('major regression')
            if regressed_hash[i] is None:
              loop_iteration["message"].append(f'⚠ Major regression introduced! ⚠')
              regressed_hash[i] = current_hash
            else:
              loop_iteration["message"].append(f'⚠ Major regression since commit {f"[{regressed_hash[i]}](https://github.com/{repo_url}/commit/{regressed_hash[i]})"} ⚠') #cannot put a dictionary value here :( )
              regressed = True


        elif loop_iteration["new_mips"][i] > loop_iteration["best_mips"][i]:
            print('new best')
            loop_iteration["message"].append(f'🥇 New best performance for {loop_iteration["jit_engines"][i]} Just-in-Time engine!')
            loop_iteration["best_mips"][i] = loop_iteration["new_mips"][i]
            best_hash[i] = current_hash
            regressed_hash = None

        else:
            if regressed_hash[i] is not None:
                loop_iteration["message"].append('Regression cleared')

            else:
                loop_iteration["message"].append(f'No significant performance change for {loop_iteration["jit_engines"][i]} Just-in-Time engine.')
                print('no significant change')
                regressed_hash = None



        new_dict[f'best_mips_{loop_iteration["jit_engines"][i]}'] = loop_iteration["best_mips"][i]
        new_dict[f'best_hash_{loop_iteration["jit_engines"][i]}'] = best_hash[i]
        new_dict[f'regressed_hash_{loop_iteration["jit_engines"][i]}'] = regressed_hash[i]



    if not no_update:
        with open(new_path, 'w') as f1:
            json.dump(new_dict, f1)



    if repo_url:

        templates = [issue_template, wiki_template, html_template]
        output_files = ['mips_issue_text.md', 'mips_issue_text.html', 'wiki_text.md']
        link_to_current_hash = f"https://github.com/{repo_url}/commit/{current_hash}"
        link_to_old_best_hash_TCC = [f"https://github.com/{repo_url}/commit/{old_best_hash[0]}"]
        link_to_old_best_hash_GCC = [f"https://github.com/{repo_url}/commit/{old_best_hash[1]}"]
        link_to_old_best_hash_LLVM = [f"https://github.com/{repo_url}/commit/{old_best_hash[2]}"]

        for index, fname in enumerate(output_files):
            with open(fname, 'w') as fw:
                fw.write(templates[index.render(

                    current_hash = current_hash,

                    link_to_current_hash = link_to_current_hash,

                    link_to_old_best_hash_TCC = link_to_old_best_hash_TCC,
                    link_to_old_best_hash_GCC = link_to_old_best_hash_GCC,
                    link_to_old_best_hash_LLVM = link_to_old_best_hash_LLVM,

                    best_hash_TCC = old_best_hash[0],
                    best_hash_GCC = old_best_hash[1],
                    best_hash_LLVM = old_best_hash[2],

                    new_mips_TCC = loop_iteration["new_mips"][0],
                    new_mips_GCC = loop_iteration["new_mips"][1],
                    new_mips_LLVM = loop_iteration["new_mips"][2],

                    message_TCC = loop_iteration["message"][0],
                    message_GCC = loop_iteration["message"][1],
                    message_LLVM = loop_iteration["message"][2],

                    best_mips_TCC = loop_iteration["best_mips"][0],
                    best_mips_GCC = loop_iteration["best_mips"][1],
                    best_mips_LLVM = loop_iteration["best_mips"][2],

                    best_diff_TCC = loop_iteration["best_diff"][0],
                    best_diff_GCC = loop_iteration["best_diff"][1],
                    best_diff_LLVM = loop_iteration["best_diff"][2],

                )])




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