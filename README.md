# 在博客里出现过的脚本以及其用处
## id_modification.py
用于处理组装的 contig id，可以添加前缀、添加后缀或简化 id。
## longest_contig.py
用于提取组装的最长转录本。
## onego.py
将 Trinotate 输出的注释转化为一基因（转录本）对一 GO term 的形式。
## de.py
用于提取差异表达基因，专对于 Trinity 的 Pipeline 输出。
## enrichment_plot.py
用于绘制 GO 富集分析气泡图。用法：
```shell
$ python enrichment_plot.py -gef all_up.txt \
-geb onego.txt -go go_term.list \
-o outputdir \
#-t Juse -l 8 -w 8
```
```shell
$ python enrichment_plot.py -c enrichment_analysis.csv \
-o outputdir \
#-t Juse -l 8 -w 8
```
具体参数含义可以使用 python enrichment_plot.py -h 查阅。
