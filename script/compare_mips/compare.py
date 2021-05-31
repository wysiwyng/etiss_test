import argparse
import json
import pathlib
import shutil

from mako.template import Template

ISSUE_TEMPLATE = r'''**Status** (for commit ${current_hash})**:**

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
<p><b>Status</b> (for commit <a href=${final_current_hash}>${current_hash}</a>)<b>:</b>
${message_tcc}<br/>
<b>Current dhrystone MIPS for TCCJIT</b> <b>:</b> ${new_mips_tcc}<br/>
<b>Previous best for TCCJIT</b> (recorded in commit <a href="https://github.com/${repo_url}/commit/${old_best_hash}">${best_hash}</a>)<b>:</b> ${best_mips_tcc}, difference ${f'{best_diff_tcc:+.2%}'}<br/>
<b>Status</b> (for commit <a href="https://github.com/${repo_url}/commit/${final_current_hash}">${current_hash}</a>)<b>:</b>
${message_gcc}<br/>
<b>Current dhrystone MIPS for GCCJIT</b> <b>:</b> ${new_mips_gcc}<br/>
<b>Previous best for GCCJIT</b> (recorded in commit <a href="https://github.com/${repo_url}/commit/${old_best_hash}">${best_hash}</a>)<b>:</b> ${best_mips_gcc}, difference ${f'{best_diff_gcc:+.2%}'}<br/>
<b>Status</b> (for commit <a href="https://github.com/${repo_url}/commit/${final_current_hash}">${current_hash}</a>)<b>:</b>
${message_llvm}<br/>
<b>Current dhrystone MIPS for LLVMJIT</b> <b>:</b> ${new_mips_llvm}<br/>
<b>Previous best for LLVMJIT</b> (recorded in commit <a href="https://github.com/${repo_url}/commit/${old_best_hash}">${best_hash}</a>)<b>:</b> ${best_mips_llvm}, difference ${f'{best_diff_llvm:+.2%}'}</br>
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

    new_mips_tcc = new_dict['mips_tcc']
    new_mips_gcc = new_dict['mips_gcc']
    new_mips_llvm = new_dict['mips_llvm']

    old_best_mips_tcc = best_mips_tcc = old_dict.get('best_mips_tcc', 0.00000001)
    old_best_mips_gcc = best_mips_gcc = old_dict.get('best_mips_gcc', 0.00000001)
    old_best_mips_llvm = best_mips_llvm = old_dict.get('best_mips_llvm', 0.00000001)

    temp_best_hash=old_dict.get('best_hash', None)
    old_best_hash = best_hash = temp_best_hash[:8]
    regressed_hash = old_dict.get('regressed_hash', None)

    best_diff_tcc = new_mips_tcc / best_mips_tcc - 1
    best_diff_gcc = new_mips_gcc / best_mips_gcc - 1
    best_diff_llvm = new_mips_llvm / best_mips_llvm - 1

    regressed = False



    if best_diff_tcc < -tolerance and best_diff_gcc < -tolerance and best_diff_llvm < -tolerance:
        message_tcc = f'⚠ Major regression since commit {regressed_hash} ⚠'
        print('major regression')
        message_gcc = f'⚠ Major regression since commit {regressed_hash} ⚠'
        print('major regression')
        message_llvm = f'⚠ Major regression since commit {regressed_hash} ⚠'
        print('major regression')
        if regressed_hash is None:
            message_tcc = f'⚠ Major regression introduced! ⚠'
            message_gcc = f'⚠ Major regression introduced! ⚠'
            message_llvm = f'⚠ Major regression introduced! ⚠'
            regressed_hash = current_hash
        regressed = True

    elif new_mips_tcc > best_mips_tcc and new_mips_gcc > best_mips_gcc and new_mips_llvm > best_mips_llvm:
        print('new best')
        message_tcc = '🥇 New best performance for TCCJIT!'
        print('new best')
        message_gcc = '🥇 New best performance for GCCJIT!'
        print('new best')
        message_llvm = '🥇 New best performance for LLVMJIT!'
        best_mips_tcc = new_mips_tcc
        best_mips_gcc = new_mips_gcc
        best_mips_llvm = new_mips_llvm
        best_hash = current_hash
        regressed_hash = None

    else:
        if regressed_hash is not None:
            message_tcc = 'Regression cleared'
            print('regression cleared')
            message_gcc = 'Regression cleared'
            print('regression cleared')
            message_llvm = 'Regression cleared'
            print('regression cleared')
        else:
            message_tcc = 'No significant performance change for TCCJIT'
            print('no significant change')
            message_gcc = 'No significant performance change for GCCJIT'
            print('no significant change')
            message_llvm = 'No significant performance change for LLVMJIT'
            print('no significant change')
        regressed_hash = None

    new_dict['best_mips_tcc'] = best_mips_tcc
    new_dict['best_mips_gcc'] = best_mips_gcc
    new_dict['best_mips_llvm'] = best_mips_llvm
    new_dict['best_hash'] = best_hash
    new_dict['regressed_hash'] = regressed_hash

    final_current_hash=current_hash[:8]

    if not no_update:
        with open(new_path, 'w') as f1:
            json.dump(new_dict, f1)

    with open('mips_issue_text.md', 'w') as f1:
        f1.write(issue_template.render(
            current_hash=final_current_hash,
            best_hash=old_best_hash,

            new_mips_tcc=new_mips_tcc,
            message_tcc=message_tcc,
            best_mips_tcc=old_best_mips_tcc,
            best_diff_tcc=best_diff_tcc,

            new_mips_gcc=new_mips_gcc,
            message_gcc=message_gcc,
            best_mips_gcc=old_best_mips_gcc,
            best_diff_gcc=best_diff_gcc,

            new_mips_llvm=new_mips_llvm,
            message_llvm=message_llvm,
            best_mips_llvm=old_best_mips_llvm,
            best_diff_llvm=best_diff_llvm
        ))

    if repo_url:



     with open('mips_issue_text.html', 'w') as f2:
        f2.write(html_template.render(
            current_hash=final_current_hash,
            best_hash=old_best_hash,

            new_mips_tcc=new_mips_tcc,
            message_tcc=message_tcc,
            best_mips_tcc=old_best_mips_tcc,
            best_diff_tcc=best_diff_tcc,

            new_mips_gcc=new_mips_gcc,
            message_gcc=message_gcc,
            best_mips_gcc=old_best_mips_gcc,
            best_diff_gcc=best_diff_gcc,

            new_mips_llvm=new_mips_llvm,
            message_llvm=message_llvm,
            best_mips_llvm=old_best_mips_llvm,
            best_diff_llvm=best_diff_llvm
        ))


    if repo_url:
            final_current_hash = f"[{final_current_hash[:8]}](https://github.com/{repo_url}/commit/{final_current_hash})"
            old_best_hash = f"[{old_best_hash[:8]}](https://github.com/{repo_url}/commit/{old_best_hash})"

    with open('wiki_text.md', 'w') as f1:
            f1.write(wiki_template.render(
            current_hash=final_current_hash,
            best_hash=old_best_hash,

            new_mips_tcc=new_mips_tcc,
            message_tcc=message_tcc,
            best_mips_tcc=old_best_mips_tcc,
            best_diff_tcc=best_diff_tcc,

            new_mips_gcc=new_mips_gcc,
            message_gcc=message_gcc,
            best_mips_gcc=old_best_mips_gcc,
            best_diff_gcc=best_diff_gcc,

            new_mips_llvm=new_mips_llvm,
            message_llvm=message_llvm,
            best_mips_llvm=old_best_mips_llvm,
            best_diff_llvm=best_diff_llvm
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

