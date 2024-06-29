
## Welcome to PyScipt for CT repository (English)

This repository houses a collection of Python scripts designed for comparative transcriptomics and phylotranscriptomics. Detailed usage instructions for most of these scripts are available on my blog, [Juse's Blog](https://biojuse.com/).

To facilitate ease of use, this README profile includes comprehensive explanations.

If you have any other requests for editing or formalizing content, feel free to ask!

These scripts will be interpreted in alphabetical order by name.

- [abbababa_test.py](#abbababa_testpy)
- [bedgraph_lowess.py](#bedgraph_lowesspy)
- [callCodeml.py](#callcodemlpy)
- [de.py](#depy)
- [enrichment_plot.py](#enrichment_plotpy)
- [free-ratio-calcu.py & free-ratio-omega.py](#free-ratio-calcupy--free-ratio-omegapy)
- [generate_clade-defs.py](#generate_clade-defspy)
- [get_sites.py](#get_sitespy)
- [id_modification.py](#id_modificationpy)
- [longest_contig.py](#longest_contigpy)
- [onego.py](#onegopy)
- [ortho_select.py](#ortho_selectpy)
- [OTU_replace.py](#otu_replacepy)
- [phylopypruner_batch.py](#phylopypruner_batchpy)
- [ref2spename.py](#ref2spenamepy)
- [sequence_con.py](#sequence_conpy)
- [sliding_window.py](#sliding_windowpy)
- [trim_filter.py](#trim_filterpy)

### abbababa_test.py

This script executes an `ABBA-BABA test` utilizing phylogenetic tree data. It **benchmarks against the species tree, extracting all conceivable quartets of species**. The script methodically traverses each gene tree, tallying the occurrences of `ABBA` and `BABA` patterns. Subsequently, it calculates the D-statistic and conducts a Binomial test to assess statistical significance.

Please note that this may **require a high confidence level in the species tree**, and too many species will bring huge time overhead (Modify the script to use multi-threading if necessary).

Usage:

```shell
$ python abbababa_test.py -s speciestree.treefile -g dirofgenetree -o ./abbababatest.csv
```

Parameters:

- `-s`  the species tree
- `-g`  the directory of gene trees (end with `.treefile`)
- `-o`  the output file (default: `./abbababatest.csv`)

Example output:

| p1   | p2   | p3   | o    | abba_count | baba_count | d_statistic | p_value | total_trees | abba_gene    | baba_gene    |
| ---- | ---- | ---- | ---- | ---------- | ---------- | ----------- | ------- | ----------- | ------------ | ------------ |
| x    | x    | x    | x    | 5          | 4          | 0.111111111 | 1       | 82          | OG0009150... | OG0009299... |

### bedgraph_lowess.py

This script is used for applying LOWESS smoothing to bedgraph files.

Usage:

```shell
$ python bedgraph_lowess.py -i [input] -o [output] --span [span size] --chr [chrlist]
```

Parameter details:

- `--input` or `-i`: Specifies the bedgraph file to be smoothed using LOWESS. This file should have exactly four columns, with the first column containing chromosome numbers that start with `chr`.
- `--output` or `-o`: Specifies the output file for the smoothed bedgraph.
- `--span`: Specifies the span size to be used for smoothing. The script will determine the proportion of data to be used for smoothing based on the total length of each chromosome (calculated as the difference between the last `end site` and the first `start site` in the bin).
- `--chr`: Specifies the chromosome numbers for which smoothing should be applied. For example, to use only autosomes in human chromosomes, you can specify `1-22`, or use comma-separated values like `1-22,X,Y`.

Please note that while smoothing reduces noise, it also results in some loss of information. Therefore, carefully consider your data when setting the `--span` parameter. Generally:

- The higher the data resolution, the lower the value that should be set for this parameter, and vice versa.
- The higher the requirement for detail, the lower the value that should be set for this parameter, and vice versa.

Example:

```shell
$ python bedgraph_lowess.py -i RT.bedgraph -o RT.lowess.bedgraph --span 300000 --chr 1-19
```

![](https://biojuse.com/pic2/bedgraphlowess.png)

### callCodeml.py

For positive selection detection in batches (PAML).

This script appears in [blog post](https://biojuse.com/2023/05/04/%E5%85%B3%E4%BA%8E%20PAML%20%E7%9A%84%E4%B8%80%E4%BA%8C%E4%B8%89%E4%BA%8B/).

Usage:

```shell
$ python callCodeml.py pathofmsa treeFile numofcpu
```

Parameters:

- `pathofmsa`  the path of MSA file (PML format)
- `treeFile`  the path of species tree
- `numofcpu`  the number of cpu used

All result files will be output in the folder starting with `WorkingDir` in the current directory, and statistics of all results will appear in `result.tsv` in this folder.

Example of `result.csv`:

|                         | lnL1         | lnL2         | np0  | np1  | kappa   | pvalue |
| ----------------------- | ------------ | ------------ | ---- | ---- | ------- | ------ |
| XP_027232673.1.paml.PML | -2280.164167 | -2280.164167 | 11   | 12   | 2.45436 | 1      |

### de.py

A script for extracting DEGs written for files output by Trinity pipeline. If you want to change the screening criteria, you can make corresponding adjustments.

This script appears in [blog post](https://biojuse.com/2022/12/11/%E6%AF%94%E8%BE%83%E8%BD%AC%E5%BD%95%E7%BB%84%E5%88%86%E6%9E%90%EF%BC%88%E4%BA%94%EF%BC%89%E2%80%94%E2%80%94%20%E8%BD%AC%E5%BD%95%E6%9C%AC%E5%AE%9A%E9%87%8F%E4%B8%8E%E5%B7%AE%E5%BC%82%E8%A1%A8%E8%BE%BE%E5%88%86%E6%9E%90/).

Usage:

```shell
$ python de.py xxx.DE_results DEG_up.txt DEG_down.txt
```

The output `DEG_up.txt` and `DEG_down.txt` are the lists of up-regulated and down-regulated DEGs respectively.

### enrichment_plot.py

Pipeline for GO enrichment analysis and visualization (**for transcriptome with no reference**).

This script appears in [blog post](https://biojuse.com/2022/12/19/%E6%AF%94%E8%BE%83%E8%BD%AC%E5%BD%95%E7%BB%84%E5%88%86%E6%9E%90%EF%BC%88%E5%85%AD%EF%BC%89%E2%80%94%E2%80%94%20GO%20%E5%AF%8C%E9%9B%86%E5%88%86%E6%9E%90%E4%B8%8E%E5%8F%AF%E8%A7%86%E5%8C%96/).

Usage 1:

```shell
$ python enrichment_plot.py -gef all_up.txt \
-geb onego.txt -go go_term.list \
-o outputdir \
#-t Juse -l 8 -w 8
```

Need:

- `-gef`  foreground gene sets used in the analysis, such as up- or down-regulated DEGs. e.g.

```
gene1
gene2
```

- `-geb`  background gene sets with go annotation. e.g.

```
gene1	GOxx1
gene1	GOxx2
gene2	GOxx1
......
```

- `-go`   `go_term.list` in repository, can be generate by:

```shell
$ python get_go_term.py go-basic.obo
# go-basic.obo: https://purl.obolibrary.org/obo/go/go-basic.obo
```

- `-o`  output directory

Optional:

- `-t`  title of figure
- `-l` `-w`  length and width of figure
- `-y`  y label will be GO id if set `ID`

Example output:

![](https://biojuse.com/pic/output.png)

![](https://biojuse.com/pic/enrichment_plot.png)

![](https://biojuse.com/pic/enrichment_csv.png)

Usage 2:

```shell
$ python enrichment_plot.py -c enrichment_analysis.csv \
-o outputdir \
```

When using an existing csv for analysis.

### free-ratio-calcu.py & free-ratio-omega.py

Running free ratio model in batches.

This script appears in [blog post](https://biojuse.com/2023/05/04/%E5%85%B3%E4%BA%8E%20PAML%20%E7%9A%84%E4%B8%80%E4%BA%8C%E4%B8%89%E4%BA%8B/).

```shell
$ python free-ratio_calcu.py treefile seqdir outputDir
```

The Parameters are same as `callCodeml.py`.

Summary the result:

```shell
$ python free-ratio-omega.py spename_file path_of_outfile
```

`spename_file` (species whose ω(dN/dS) value needs to be collect):

```
SpeA
SpeB
SpeC
```

Example output:

```
File	A	B	C
1	0.00733407	0.0001	0.00574998
2	0.119151	0.0917734	0.0648513
3	0.0653332	0.0288158	0.0296085
```

### generate_clade-defs.py

Generate clade definition file for DiscoVista, need to use with Juse's fork.

```shell
$ python generate_clade-defs.py anno-1.txt anno.txt
```

Detail: [blog post](https://biojuse.com/2023/07/12/DiscoVista%20%E5%8F%AF%E8%A7%86%E5%8C%96%E7%B3%BB%E7%BB%9F%E5%8F%91%E8%82%B2%E4%B8%8D%E4%B8%80%E8%87%B4/).

### get_sites.py

Extract genomic CpG site coordinate information.

To run the example for extracting CpG sites located on chromosome 21 of the hg38 human genome, you would use the following command:

```shell
$ python get_sites.py -g hg38.fa -c chr21 --merge --gzip -n GRCh38
```

- `-g` specifies the reference genome sequence file. The script is capable of automatically recognizing `.gz` compressed format files.
- `-c` is used to specify the chromosome from which you want to extract site information. This should match the sequence id within the sequence file.
- `--merge` is an optional flag that, when used, calls `bedtools` to merge the output files after the site information has been extracted. It's important to note that this option requires `bedtools` to be installed and available in your environment path.
- `--gzip` compresses the output files after the site information has been extracted (and merged, if `--merge` was specified).
- `-n` allows you to specify a prefix for the output files. If not provided, the script defaults to using the prefix of the sequence file.
- `-p` specifies the path where the output files will be saved. If this parameter is not given, the files are saved to the current working directory of the script.

Additionally：

- If the `--onlycpg` flag is included in the command, the script will exclusively generate files for CpG site locations.
- If the `--nosoftmask` flag is included in the command, the script will skip soft-masked region (Treat as N).

### id_modification.py

Modify the id in the `fasta` file.

This script appears in [blog post](https://biojuse.com/2022/11/21/%E6%AF%94%E8%BE%83%E8%BD%AC%E5%BD%95%E7%BB%84%E5%88%86%E6%9E%90%EF%BC%88%E4%B8%89%EF%BC%89%E2%80%94%E2%80%94%20%E7%BB%84%E8%A3%85%E7%9A%84%E8%B4%A8%E9%87%8F%E6%A3%80%E6%B5%8B%E4%B8%8E%E5%8E%BB%E5%86%97%E4%BD%99/).

```shell
$ python id_modification.py -m pre --string Human@ -o before.fasta -f after.fasta
```

```
before
>TRINITY_DN417604_c0_g1_i1
after
>Human@TRINITY_DN417604_c0_g1_i1
```

Choice of `-m` :

- `pre` add prefix
- `suf` add suffix
- `sim` simplify id (remove comment of description of id)

This script should only be used for **transcriptome assembly**. `Biopython` is recommended for genome `fasta` sequences.

### longest_contig.py

Extract the longest transcript from the **Trinity assembly**.

This script appears in [blog post](https://biojuse.com/2022/11/21/%E6%AF%94%E8%BE%83%E8%BD%AC%E5%BD%95%E7%BB%84%E5%88%86%E6%9E%90%EF%BC%88%E4%B8%89%EF%BC%89%E2%80%94%E2%80%94%20%E7%BB%84%E8%A3%85%E7%9A%84%E8%B4%A8%E9%87%8F%E6%A3%80%E6%B5%8B%E4%B8%8E%E5%8E%BB%E5%86%97%E4%BD%99/).

```shell
$ python longest_contig.py xxx.fasta longest.fasta
```

Note that this script only works with Trinity output.

### mf2mrbayes.py

Convert Modelfinder results into a format that can be input into mrbayes. e.g.

```shell
$ iqtree2 -s concatenation_ortho.fasta \
-spp IQ_partition.txt \
-m TESTMERGEONLY -mset mrbayes \
-nt AUTO -pre mybayes_aa
```

This script appears in [blog post](https://biojuse.com/2023/07/06/%E8%B4%9D%E5%8F%B6%E6%96%AF%E5%BB%BA%E6%A0%91%E4%B9%8B%20Mrbayes%20%E7%AF%87/).

```shell
$ python mf2mrbayes.py mybayes_aa.best_scheme.nex
```

The output `Mrbayes_par.txt` records the commands Mrbayes needs to type to specify partitioning and evolution models. e.g.

```
# mybayes_aa.best_scheme.nex
begin sets;
  charset OG0000874_OG0001754_OG0010164_OG0012298 = 1-125  8053-9358  52564-52667  71562-71712;
  ......
  charpartition mymodels =
    JTT+I+G4: OG0000874_OG0001754_OG0010164_OG0012298,
    ......
```

```
# Mrbayes_par.txt
charset subset1 = 1-125 8053-9358 52564-52667 71562-71712;
......
artition Names = 37:subset1, ......
set partition=Names;
lset applyto=(1) rates=invgamma;
prset applyto=(1) aamodelpr=fixed(jones);
......
```

### onego.py

Convert annotation files to one-to-one.

This script appears in [blog post](https://biojuse.com/2022/11/28/%E6%AF%94%E8%BE%83%E8%BD%AC%E5%BD%95%E7%BB%84%E5%88%86%E6%9E%90%EF%BC%88%E5%9B%9B%EF%BC%89%E2%80%94%E2%80%94%20%E7%BB%84%E8%A3%85%E7%9A%84%E6%B3%A8%E9%87%8A/).

```shell
$ python onego.py go_annotation.txt onego.txt
```

go_annotation.txt:

```
xxx1	GO:0003674,GO:0005488
```

onego.txt:

```
xxx1      GO:0003674
xxx1      GO:0005488
```

### ortho_select.py

Select orthogroup based on species number and sequence number. This script is designed for output of OrthoFinder but should be available for other situations.

This script appears in [blog post](https://biojuse.com/2023/02/17/%E6%AF%94%E8%BE%83%E8%BD%AC%E5%BD%95%E7%BB%84%E5%88%86%E6%9E%90%EF%BC%88%E4%B8%83%EF%BC%89%E2%80%94%E2%80%94%20%E7%B3%BB%E7%BB%9F%E5%8F%91%E8%82%B2%E5%88%86%E6%9E%90/).

Usage:

```shell
$ python ortho_select.py -l 30 -b 20 -f /pathto/OrthoFinder/Results_xxx/Orthogroup_Sequences -o ortho_seq
```

- `-l` specifies the minimum number of species (>), this is to filter orthogroups containing inadequate species.
- `-b` means that when the number of species sequences is greater than this parameter, the OG will be regarded as a **large** OG (e.g. `SpeA` with 21 sequences for above code)(<=), this is to split orthogroups that contain too much sequences (likely caused by excessive paralogs).
- `-f` is the `Orthogroup_Sequences` path run by orthofinder
- `-o` is the output directory

In the above use case, this command will generate two folders, `orthogroup_big` and `orthogroup_small`, in the `ortho_seq` folder.

### OTU_replace.py

Replace sequence id (`Spe_` to `Spe@`). 

IQtree will replace `@` with `_` when building a tree, but some software only recognizes `@` as a **species identifier**.

This script appears in [blog post](https://biojuse.com/2023/02/17/%E6%AF%94%E8%BE%83%E8%BD%AC%E5%BD%95%E7%BB%84%E5%88%86%E6%9E%90%EF%BC%88%E4%B8%83%EF%BC%89%E2%80%94%E2%80%94%20%E7%B3%BB%E7%BB%9F%E5%8F%91%E8%82%B2%E5%88%86%E6%9E%90/).

```shell
$ python OTU_replace.py dir species_list
```

- `dir` directory stores all sequence and tree files whose IDs need to be modified
- `species_list` each line corresponds to a species name

```
Human
Mouse
Fish
```

Example:

```
# Before
>Human_xxxxxx
>Mouse_xxxxxxx
>Fish_xxxxxxxxx
# After
>Human@xxxxxx
>Mouse@xxxxxxx
>Fish@xxxxxxxxx
```

### phylopypruner_batch.py

Running phylopypruner in batches avoids a recursion error, which has been deprecated since it was fixed via PR.

### ref2spename.py

Convert sequence files in RefSeq format to sequence format starting with the species name.

This script appears in [blog post](https://biojuse.com/2023/07/12/DiscoVista%20%E5%8F%AF%E8%A7%86%E5%8C%96%E7%B3%BB%E7%BB%9F%E5%8F%91%E8%82%B2%E4%B8%8D%E4%B8%80%E8%87%B4/).

```shell
$ python ref2spename.py ncbi_dataset/data/GCF_000001405.40/protein.faa human.fasta
```

Example:

```
>NP_000005.3 alpha-2-macroglobulin isoform a precursor [Homo sapiens] # before
>Homo_sapiens@NP_000005.3_alpha-2-macroglobulin_isoform_a_precursor # after
```

### sequence_con.py

Concatenate sequences and generate partition files for IQTREE using this script.

Note: This script uses `@` as the species identifier. If your data utilizes `_` as a species identifier, you can employ `OTU_replace.py` for conversion, or alternatively, modify this script to suit your requirements.

Please ensure to run the script in the directory containing the multiple sequence alignment files. Important: do not place the script or any unrelated files in this directory, as the script lacks suffix recognition capability.

This script appears in [blog post](https://biojuse.com/2023/01/29/%E7%94%A8%E4%BA%8E%20IQtree%20%E7%9A%84%E5%BA%8F%E5%88%97%E4%B8%B2%E8%81%94%E6%96%B9%E6%B3%95/).

```shell
$ python /pathto/sequence_con.py
```

Upon completion, a new folder `con_res` will be created. This folder includes the merged sequence file `concatenation_ortho.fasta` and the partition information file `IQ_partition.txt`, which are necessary for building trees in IQTREE.

Additionally, a log file `sequence_con.log` is generated, detailing the sequence length information for each species. In this log, a `+` in the last column indicates consistency with the first length for all species. A `-` sign, conversely, signals alignment errors in some species' sequences, denoting a length inconsistency.

![](https://biojuse.com/pic/iq.png)

For those seeking more comprehensive output information, consider downloading [JuseKit](https://github.com/JuseTiZ/JuseKit), a software I developed based on `PyQt5`. It not only includes the sequence concatenation function but also provides more detailed output.

### sliding_window.py

This script is designed for calculating dN/dS/ω values across a sliding window, providing insights into the selection pressure on different regions **within a specific gene**.

This script appears in [blog post](https://biojuse.com/2023/03/13/%E5%8D%95%E5%9F%BA%E5%9B%A0-dN%E3%80%81dS-%E5%92%8C-%CF%89-%E7%9A%84%E6%BB%91%E5%8A%A8%E7%AA%97%E5%8F%A3%E7%BB%98%E5%88%B6%E6%96%B9%E6%B3%95/).

Execute the script using the following command:

```shell
$ python sliding_window.py ogfile fa_dir sli_len gap_len cpu_num code_model
```

Prerequisite: The script requires `KaKs_calculatorv3`. Ensure that the path to `KaKs` is correctly set in your environment variables before running the script.

Parameters:

- `fa_dir`: Path to the directory containing the `fasta` files to be compared.
- `sli_len`: Length of the sliding window.
- `gap_len`: Interval between each sliding window.
- `cpu_num`: Number of CPU cores used by `KaKs_calculatorv3`.
- `code_model`: Codon translation model used in the calculations.

Example Usage:

```shell
$ python sliding_window.py ogfile fa_dir 57 6 20 1
```

This example sets a sliding window size of 57 bp, with a step size of 6 bp, utilizing 20 CPU cores, and employing the standard codon table.

Output Processing: The output `.res` file can be visualized using the following R code:

```R
library(ggplot2)
library(ggpubr)
library(ggprism)
library(readxl)

barplot = read.delim("xxx.res")
color = rep("black", times = length(barplot$Type))
color[barplot$value > 1 & barplot$Type == "omega"] = "red"
barplot = cbind(barplot, color)

pdf("slwd.pdf",width = 10,height = 8)
ggplot(barplot,aes(Position, value, fill = color)) + 
  geom_bar(stat = "identity",width = 0.9) + 
  theme_prism() + 
  theme(axis.line.y=element_line(linetype=1,color="black",size=1),
        axis.line.x=element_line(linetype=1,color="black",size=1),
        axis.ticks.x=element_line(color="black",size=1,lineend = 1),
        axis.ticks.y=element_line(color="black",size=1,lineend = 1),
        axis.text.x = element_text(angle = 90, size = 12,face = "plain"),
        axis.text.y = element_text(size = 12,face = "plain"), 
        axis.title=element_text(size=18,face="plain"), 
        legend.position = "none") + 
  xlab("Sliding windows starting positions (bp)") +
  facet_grid(Type ~ Gene, scales="free",space="free_x") + 
  scale_x_continuous(breaks = seq(0, 300, by = 100),labels = c("0", "600", "1200", "1800")) + 
  scale_fill_manual(values=c("#666666","red"))
dev.off()
```

This R code produces a bar plot displaying the calculated values, with specific color coding to highlight significant findings. The output visualization can be further refined using AI tools for enhanced clarity and presentation.

Example Plot:

![](https://biojuse.com/pic/slwd.png)

### trim_filter.py

Following alignment and trimming, some Multiple Sequence Alignments (MSAs) may exhibit reduced sequence length, potentially due to excessive trimming or the prevalence of gaps. These shortened MSAs often contain less informative content, making it prudent to filter them out to ensure only qualified MSAs are retained for subsequent analysis.

Note: This script uses `@` as the species identifier. If your data utilizes `_` as a species identifier, you can employ `OTU_replace.py` for conversion, or alternatively, modify this script to suit your requirements.

This script appears in [blog post](https://biojuse.com/2023/02/17/%E6%AF%94%E8%BE%83%E8%BD%AC%E5%BD%95%E7%BB%84%E5%88%86%E6%9E%90%EF%BC%88%E4%B8%83%EF%BC%89%E2%80%94%E2%80%94%20%E7%B3%BB%E7%BB%9F%E5%8F%91%E8%82%B2%E5%88%86%E6%9E%90/).

```shell
$ python /pathto/trim_filter.py -t 30
```

Parameters:

- `-t`: Sets the minimum number of taxa required to retain an Orthologous Group (OG). It effectively defines the minimum number of Operational Taxonomic Units (OTUs) needed.
- `-a`: Specifies the minimum length for a trimmed alignment in amino acids (or nucleotides), with the default being 80.
- `-s`: Removes original sequences shorter than this specified length. The default threshold is 80.

The process and status of trimming can be monitored in the `trim_filter.log` file.
