# mf2mrbayes.py
# Author: Juse
# Transform result from modelfinder to format used in Mrbayes.
# Usage: python mf2mrbayes.py xxx.best_scheme.nex

import sys
import os

mf_result = open(sys.argv[1],"r")
abs_path = os.path.abspath(sys.argv[1])
op_path = os.path.dirname(abs_path)

numPar = 0
numMol = 0
conPar = ''
conPar_set = []
conMol = ''

# Reference: https://github.com/dongzhang0725/PhyloSuite/blob/master/PhyloSuite/src/Lg_Mrbayes.py
dict_models = {"JC": "1", "F81": "1", "K80": "2", "HKY": "2", "TrNef": "6", "TrN": "6", "K81": "6",
               "K81uf": "6", "K2P": "2", "JC69": "1", "HKY85": "2", "K3P": "6",
               "TIMef": "6", "TIM": "6", "TVMef": "6", "TVM": "6", "SYM": "6", "GTR": "6", "TPM2": "6",
               "TPM2uf": "6", "TPM3": "6", "TPM3uf": "6", "TIM2ef": "6", "TIM2": "6", "TIM3ef": "6",
               "TIM3": "6"}

for line in mf_result:
    # 处理分区集信息
    if line.strip().startswith('charset'):
        numPar += 1
        ParPos = line.split('=')[1].strip()
        conPar += f'charset subset{numPar} = {ParPos}\n'
        conPar_set.append(f'subset{numPar}')
    # 处理分区模型信息
    elif ':' in line:
        model_name = line.split(':')[0].strip()
        numMol += 1
        if '+G' in model_name and '+I' in model_name:
            rates = " rates=invgamma"
        elif '+G' in model_name:
            rates = " rates=gamma"
        elif '+I' in model_name:
            rates = " rates=propinv"
        else:
            rates = ''
        model_used = model_name.split('+')[0]
        if model_used in dict_models:
            # nt序列
            conMol += f'lset applyto=({numMol}) nst={dict_models[model_used]}{rates};\n'
        else:
            # aa序列
            conMol += f"lset applyto=({numMol}){rates};\n"
            conMol += f"prset applyto=({numMol}) aamodelpr=fixed({model_used.lower()});\n"
            if '+F' in model_name:
                conMol += f"prset applyto=({numMol}) statefreqpr=fixed(empirical);\n"

# 生成分区名
parnam = f'partition Names = {len(conPar_set)}:{", ".join(conPar_set)};\n' \
         f'set partition=Names;\n'

# 汇总输出
total_output = conPar + parnam + conMol
total_output = total_output.replace("amodelpr=fixed(jtt)", "amodelpr=fixed(jones)")
total_output = total_output.replace("  ", " ")

with open(f'{op_path}/Mrbayes_par.txt', 'w') as t:
    t.write(total_output)

print('Finished!')