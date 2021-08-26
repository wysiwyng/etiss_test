import argparse
import json
from pathlib import Path
from mako.template import Template
from collections import defaultdict
import statistics
import matplotlib
from numpy.core.fromnumeric import size
from numpy.lib.arraypad import pad
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from itertools import chain, islice





#template to be published under an issue as a comment
ISSUE_TEMPLATE = r'''
**Performance Statistics**

% for jit_engine_name, old_best_hash, best_hash_link, new_mips, message, best_mips, best_diff in zip_form:

**Status** (for commit ${current_hash})**:**

${jit_engine_name} jit engine's performance message: ${message}\

**Current dhrystone MIPS for ${jit_engine_name} JIT** **:** ${new_mips}\

**Previous best for ${jit_engine_name} JIT** (recorded in commit ${old_best_hash})**:** ${best_mips}, difference ${f'{best_diff:.2%}'}\


% endfor

<sub>This comment was created automatically, please do not change!</sub>
'''
#template to be published in Github wiki
WIKI_TEMPLATE = r'''
% for jit_engine_name, old_best_hash, best_hash_link, new_mips, message, best_mips, best_diff in zip_form:
**Status for the ${jit_engine_name} Just-In-Time Engine** (for commit ${current_hash_wiki})**:**
${message}
<br/>
**Current dhrystone MIPS for ${jit_engine_name} JIT** **:** ${new_mips}
<br/>
**Previous best for ${jit_engine_name} JIT** (recorded in commit ${best_hash_link})**:** ${best_mips}, difference  ${f'{best_diff:.2%}'}
<br/>
<br/>
% endfor
**Graphical Analysis for the last 50 commits:**
<br/>
<br/>
[[performance_metrics.svg]]


'''
# Declaration of Global Variables:

KEY_TO_COMPARE= "mips" # the key from the input files to compare across engines
MAX_HISTORY = 50 # max amount of past data to keep
TOLERANCE = 0.2

def calculating_performance_metrics(input_files, stats_file, wiki_md, issue_md, graph_file, current_hash, repo_url):

    current_hash = current_hash[:8] #truncating hash value to first 8 characters

    ### Averaging out the MIPS and Simulation Time for the given number of runs:###

    runs = defaultdict(list)
    # get engine name and run no from filename of input
    # input files should have the format "run_<engine name>_<run no>.json"
    for index, fname in enumerate(input_files):
            filepath = Path(input_files[index])
            placeholder, engine, run_no = filepath.stem.split("_") # fails if format isn't correct
            run_no = int(run_no)
            with open(filepath, 'r') as f:
                in_dict = json.load(f)
            runs[engine].append(in_dict[KEY_TO_COMPARE])

    # Averaing out
    runs_avg = runs_avg = {key:statistics.mean(value)  for key, value in runs.items()}


    ### Comparing the MIPS value of the current run with previous best MIPS: ###

    #instantiating dictionaries and lists

    messages = dict() # to store messages of the performance metric of the corresponding engine
    stats = defaultdict(dict) # store output results in a dict of dicts.
    diffs = dict() # to store the difference between the current MIPS and the previous best


    stats_file = Path(stats_file) # the path of the output file

    if not stats_file.exists(): # first time performance measured
        # filling up the stats dictionary with values from the current run
        for engine, value in runs_avg.items():
            stats[engine] = {
                KEY_TO_COMPARE: [(value, current_hash)],
                "best_" + KEY_TO_COMPARE: value,
                "best_hash" : current_hash,
                "regressed_hash" : None
            }

    else:
        with open(stats_file, 'r') as f: # load already existing previous statistics
           stats = json.load(f)


        for engine, value in runs_avg.items(): #comes within else

            if engine not in stats: # adding a new engine
                stats[engine] = {
                    KEY_TO_COMPARE: [(value, current_hash)],
                    "best_" + KEY_TO_COMPARE: value,
                    "best_hash" : current_hash,
                    "regressed_hash" : None,
                    "message": "no file to compare, assuming first entry"
                }

            else:
                stats[engine][KEY_TO_COMPARE].append((value,current_hash)) # adding the MIPS from current run
                stats[engine][KEY_TO_COMPARE]= stats[engine][KEY_TO_COMPARE][-MAX_HISTORY:] # for first time run. No need to add current run value; already done earlier

                best = stats[engine]["best_" + KEY_TO_COMPARE]

                diff = value / best - 1
                diffs[engine] = diff

            # Comparison logic:

            if value > best:
                stats[engine][f"best_" + KEY_TO_COMPARE] = value
                stats[engine][f"best_hash"] = current_hash[:8]
                messages[engine] = f'🥇 New best performance!'

            elif diff < -TOLERANCE:
                if stats[engine]["regressed_hash"] is None:
                    stats[engine]["regressed_hash"] = current_hash[:8]
                    messages[engine] = "Regression introduced"
                else:
                    messages[engine] = "Regressed since commit " + stats[engine]['regressed_hash']

            else:
                if stats[engine]["regressed_hash"] is not None:
                    stats[engine]["regressed_hash"] = None
                    messages[engine] = "Regression cleared"
                else:
                    messages[engine] = "No significant performance change"


    # Template rendering for issue and Github Wiki:

    issue_template = Template(text=ISSUE_TEMPLATE)
    wiki_template = Template(text=WIKI_TEMPLATE)
    templates = [issue_template, wiki_template]

    # Instantiating useful lists needed for template rendering:
    output_files = [issue_md, wiki_md]
    best_hash = []
    best_hash_link = []
    best_mips = []
    new_mips = []
    jit_engines = []
    message = messages.values()
    best_diff = diffs.values()
    current_hash_wiki = f"[{current_hash}](https://github.com/{repo_url}/commit/{current_hash})"

    for engine, nested_dict in stats.items():
        jit_engines.append(engine)
        best_mips.append(nested_dict["best_mips"])
        new_mips.append(nested_dict["mips"][-1])
        best_hash.append(nested_dict["best_hash"])
        best_hash_ = nested_dict["best_hash"]
        best_hash_link.append(f"[{best_hash_}](https://github.com/{repo_url}/commit/{best_hash_})")

    zip_form = zip(jit_engines, best_hash, best_hash_link, new_mips, message, best_mips, best_diff)
    zip_list = list(zip_form)


    # Graphical Analysis of Performance Metrics:
    fig = plt.figure(figsize=(20,20))

    for engine in stats:
        commit_history=list(chain.from_iterable(islice(item, 1, 2) for item in stats[engine][KEY_TO_COMPARE]))
        print(commit_history)
        mips_value= list(chain.from_iterable(islice(item, 0, 1) for item in stats[engine][KEY_TO_COMPARE]))
        print(mips_value)
        plt.plot(commit_history, mips_value, label=f'{KEY_TO_COMPARE}_{engine}')

    plt.xticks(fontsize=15,rotation =45)
    plt.title(f'MIPS values for the last  {len(commit_history)} commits', size=50)
    plt.xlabel("Commit History", size=30)
    plt.ylabel("MIPS", size=30)


    # Save figure
    fig.savefig(graph_file, bbox_inches='tight',pad_inches = 0.5)

    # Save statistics file
    with open(stats_file, 'w') as f:
       json.dump(stats, f)

    # Render Templates

    if repo_url:

        for index, fname in enumerate(output_files):
            with open(fname, 'w') as fw:
                fw.write(templates[index].render(

                    current_hash = current_hash,
                    current_hash_wiki = current_hash_wiki,
                    zip_form = zip_list
                )
                )


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("input_files", nargs="+")
    parser.add_argument('-o', help='arguments', dest='stats_file', action='store')
    parser.add_argument('-i', '--issue_md')
    parser.add_argument('-w', '--wiki_md')
    parser.add_argument('-gr','--graph_file')
    parser.add_argument('-g','--current_hash')
    parser.add_argument('-r', '--repo_url')
    args = parser.parse_args()


calculating_performance_metrics(args.input_files, args.stats_file, args.issue_md, args.wiki_md, args.graph_file, args.current_hash, args.repo_url)