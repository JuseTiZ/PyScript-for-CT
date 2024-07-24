import re
import sys
import os
from scipy.stats import chi2
import time
from typing import List, Tuple

def help_info() -> None:
    print("This script is used to call codeML.\nUsage: python3 callCodeml.py Dir treeFile cpuNum\n")

def get_args() -> Tuple[str, List[str], str, int]:
    args = sys.argv[1:]
    if len(args) < 3:
        help_info()
        sys.exit(1)
    
    dir_path = os.path.abspath(args[0])
    if not os.path.isdir(dir_path):
        help_info()
        sys.exit(1)
    
    tree_file = os.path.abspath(args[1])
    try:
        cpu_num = int(args[2])
    except ValueError:
        help_info()
        sys.exit(1)
    
    seqs = [x for x in os.listdir(dir_path) if not x.startswith('.')]
    return dir_path, seqs, tree_file, cpu_num

def create_dir(base_dir: str, name: str) -> None:
    dirs = [
        f'{base_dir}/',
        f'{base_dir}/{name}',
        f'{base_dir}/{name}/null',
        f'{base_dir}/{name}/alte'
    ]
    for dir_path in dirs:
        os.makedirs(dir_path, exist_ok=True)

def create_ctl(base_dir: str, dir_path: str, name: str, tree_file: str) -> None:
    ctl_null = f'''
    seqfile = {dir_path}/{name}
    treefile = {tree_file}
    outfile = {base_dir}/{name}/null/{name}_null.res
    noisy = 9
    verbose = 0
    runmode = 0
    seqtype = 1
    CodonFreq = 2
    clock = 0
    aaDist = 0
    model = 2
    NSsites = 2
    icode = 0
    Mgene = 0
    fix_kappa = 0
    kappa = 2
    fix_omega = 1
    omega = 1
    fix_alpha = 1
    alpha = .0
    Malpha = 0
    ncatG = 3
    getSE = 0
    RateAncestor = 0
    fix_blength = 0
    method = 0
    Small_Diff = .45e-6
    cleandata = 1
    '''
    ctl_alte = ctl_null.replace(f'{base_dir}/{name}/null/{name}_null.res', f'{base_dir}/{name}/alte/{name}_alte.res')\
                       .replace('fix_omega = 1', 'fix_omega = 0')\
                       .replace('omega = 1', 'omega = 1.5')
    
    with open(f'{base_dir}/{name}/null/null_profile.ctl', 'w') as f:
        f.write(ctl_null)
    with open(f'{base_dir}/{name}/alte/alte_profile.ctl', 'w') as f:
        f.write(ctl_alte)

def run_create(base_dir: str, dir_path: str, seqs: List[str], tree_file: str) -> None:
    for name in seqs:
        create_dir(base_dir, name)
        create_ctl(base_dir, dir_path, name, tree_file)
    
    with open(f'{base_dir}/codeml.sh', 'w') as f:
        f.write('''
#!/bin/bash
list=$(ls -1)
count=$(ls -1 | wc -l)
echo "Total number: $count"
dir=$(pwd)
echo "Start Now..."
for i in $list
do
    {
    echo "cd $dir/$i/null; codeml ./null_profile.ctl > log.txt; cd $dir/$i/alte; codeml ./alte_profile.ctl > log.txt" >> paml_command
    }
done
wait
''')
    print(f"{time.strftime('%Y-%m-%d %H:%M:%S')} Files created.\n")

def run_codeml(base_dir: str, num: int) -> None:
    os.chdir(base_dir)
    os.system('bash codeml.sh')
    os.system(f'cat paml_command | parallel --no-notice -j {num}')
    print(f"\n{time.strftime('%Y-%m-%d %H:%M:%S')} Codeml Done...\n")

def get_res(path: str) -> Tuple[float, int, float]:
    with open(path, "r") as f:
        t = f.read()
        kappa = float(re.findall(r"kappa\s*=\s*([\d\.]+)", t)[0])
        lnL = float(re.findall(r'lnL\s*\(.*\)\s*=\s*([-\d\.]+)', t)[0])
        np = int(re.findall(r'lnL\s*\(.*\)\s*=\s*[-\d\.]+\s*\(\s*(\d+)', t)[0])
        return lnL, np, kappa

def run_stat(base_dir: str, name: str) -> None:
    try:
        path_alte = f'{base_dir}/{name}/alte/{name}_alte.res'
        path_null = f'{base_dir}/{name}/null/{name}_null.res'
        
        lnL0, np0, _ = get_res(path_null)
        lnL1, np1, kappa = get_res(path_alte)
        
        lnl = abs(lnL0 - lnL1) * 2
        np = abs(np0 - np1)
        pvalue = 1 - chi2.cdf(lnl, np)
        
        with open(f'{base_dir}/result.tsv', 'a') as f:
            f.write(f"{name}\t{lnL0}\t{lnL1}\t{np0}\t{np1}\t{kappa}\t{pvalue}\n")
    except Exception as e:
        print(f"{time.strftime('%Y-%m-%d %H:%M:%S')} {name} failed to stats: {e}")

def main() -> None:
    start_time = time.strftime('%Y%m%d-%H%M%S')
    base_dir = f"{os.getcwd()}/WorkingDir_{start_time}"
    
    dir_path, seqs, tree_file, cpu_num = get_args()
    run_create(base_dir, dir_path, seqs, tree_file)
    run_codeml(base_dir, cpu_num)
    
    for name in seqs:
        run_stat(base_dir, name)
    
    print(f'Total time used: {time.time() - start_time:.2f} seconds\n')

if __name__ == "__main__":
    t0 = time.time()
    main()
    print(f'Total time used: {time.time() - t0:.2f} seconds\n')
