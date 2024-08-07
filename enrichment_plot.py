# -*- coding: utf-8 -*-
# enrichment_plot.py
# Verson: 1.1
# Author: Juse
# Use R to plot enrichment dotplot.
# Usage: See github.

import argparse
import os
import time

def get_args():

	parser = argparse.ArgumentParser(description = "This is used to plot enrichment dotplot.")
	parser.add_argument("-gef", "--genefore", type = str, help = "The gene list as foregroud.")
	parser.add_argument("-geb", "--geneback", type = str, help = "The gene list and annotation as backgroud.")
	parser.add_argument("-go", "--golist", type = str, help = "The go_term.list file.")
	parser.add_argument("-w", "--width", default = '8', type = str, help = "Width of plot, default = 8.")
	parser.add_argument("-l", "--height", default = '8', type = str, help = "Height of plot, default = 8.")
	parser.add_argument("-y", "--yaxis", default = "Description", choices = ['Description','ID'], type = str, help = "The yaxis of plot, use GO Description as default.")
	parser.add_argument("-o", "--output", type = str, required = True, help = "The output directory, required.")
	parser.add_argument("-t", "--title", default = 'NULL', type = str, help = "The title of plot, default = NULL.")
	parser.add_argument("-c", "--csv", default = 'NULL', type = str, help = "Just plot with file given.")
	args = parser.parse_args()
	return args


def get_path(args):
	
	if args.csv == 'NULL':
		paths = {
			'fore_gene': os.path.abspath(args.genefore),
			'back_gene': os.path.abspath(args.geneback),
			'go_list': os.path.abspath(args.golist),
			'output_dir': os.path.abspath(args.output),
		}
	else:
		paths = {
			'output_dir': os.path.abspath(args.output),
			'csv_dir': os.path.abspath(args.csv)
		}
     
	return paths


def R_code(args, paths, run_time):

	rcode = '''

# 加载包
library("clusterProfiler")
library("ggplot2")
library("DOSE")

# 加载各个参数
goterm = "%juse%1"
backgene = "%juse%2"
foregene = "%juse%3"
wid = %juse%4
hei = %juse%5
title = "%juse%7"

# 生成背景注释集
go_class <- read.delim(goterm, header=FALSE, stringsAsFactors =FALSE) 
names(go_class) <- c('ID','Description','Ontology')  
go_anno <- read.delim(backgene, header=FALSE, stringsAsFactors =FALSE)
names(go_anno) <- c('gene_id','ID')
go_anno <-merge(go_anno, go_class, by = 'ID', all.x = TRUE)

# 生成前景基因集
gene_list <- read.delim(foregene,header=FALSE) 
names(gene_list) <- c('gene_id') 
gene_select <- gene_list$gene_id  

# 进行富集分析
go_rich <- enricher(gene = gene_select,
					TERM2GENE = go_anno[c('ID','gene_id')],
					TERM2NAME = go_anno[c('ID','Description')],
					pvalueCutoff = 0.05,
					pAdjustMethod = 'BH',
					qvalueCutoff = 0.05,
					maxGSSize = 200) 

# 提取富集分析结果制成表格
plot_data = cbind(go_rich$ID, go_rich$Description, go_rich$GeneRatio, go_rich$BgRatio, go_rich$Count, go_rich$p.adjust, go_rich$ID, go_rich$geneID)
colnames(plot_data) = c("ID", "Description", "GeneRatio", "BgRatio", "Count","qvalue", "Ontology", "GeneID")
plot_data = data.frame(plot_data)
for(i in 1:length(plot_data$Ontology)){
  if(is.na(plot_data$Description[i])){
	plot_data$Ontology[i] = 'NA'
  }else{
	plot_data$Ontology[i] = go_class$Ontology[go_class$ID == plot_data$ID[i]]
  }
}

# 处理数据
plot_data_noNA = plot_data[complete.cases(plot_data$Description),]
plot_data_noNA = transform(plot_data_noNA, Count = as.numeric(Count),
						   qvalue = as.numeric(qvalue))
plot_data_noNA = plot_data_noNA[order(plot_data_noNA$qvalue,-plot_data_noNA$Count),]
plot_data_noNA$Ontology[plot_data_noNA$Ontology == "cellular_component"] = "Cellular Component"
plot_data_noNA$Ontology[plot_data_noNA$Ontology == "biological_process"] = "Biological Process"
plot_data_noNA$Ontology[plot_data_noNA$Ontology == "molecular_function"] = "Molecular Function"

Top15 = c()
CC = 0
BP = 0
MF = 0
for(i in 1:length(plot_data_noNA$Ontology)){
  if(plot_data_noNA$Ontology[i] == "Cellular Component"){
	CC = CC + 1
	if(CC <= 5){
	  Top15 = append(Top15,(i))
	}
  }
  if(plot_data_noNA$Ontology[i] == "Biological Process"){
	BP = BP + 1
	if(BP <= 5){
	  Top15 = append(Top15,(i))
	}
  }
  if(plot_data_noNA$Ontology[i] == "Molecular Function"){
	MF = MF + 1
	if(MF <= 5){
	  Top15 = append(Top15,(i))
	}
  }
}

# 进行气泡图绘制
enrichment_plot = ggplot(plot_data_noNA[Top15,],aes(x = parse_ratio(GeneRatio),y = reorder(%juse%6, Count))) + geom_point(aes(size=Count,color=qvalue,)) +
  scale_color_gradient(low = "red", high = "blue") + theme_bw() + ylab(NULL) + xlab("GeneRatio") + 
  facet_wrap(~Ontology, scale="free",ncol = 1,strip.position = "right") + 
  theme(text = element_text(size = 15))

enrichment_plot_top10 = ggplot(plot_data_noNA[1:10,],aes(x = parse_ratio(GeneRatio),y = reorder(%juse%6, Count))) + geom_point(aes(size=Count,color=qvalue,)) +
  scale_color_gradient(low = "red", high = "blue") + theme_bw() + ylab(NULL) + xlab("GeneRatio") + 
  theme(text = element_text(size = 15))

if(title != "NULL"){
  enrichment_plot = enrichment_plot + ggtitle(title)
  enrichment_plot_top10 = enrichment_plot_top10 + ggtitle(title)
}

# 保存图及富集分析表格
pdf("output%1%",width = wid,height = hei)
enrichment_plot
dev.off()

pdf("output%2%",width = wid,height = hei)
enrichment_plot_top10
dev.off()

write.csv(plot_data,file="output%3%")


'''

	r_code_use = rcode.replace("%juse%1", paths['go_list'])\
		.replace("%juse%2", paths['back_gene'])\
		.replace("%juse%3", paths['fore_gene'])\
		.replace("%juse%4", args.width)\
		.replace("%juse%5", args.height)\
		.replace("%juse%6", args.yaxis)\
		.replace("%juse%7", args.title)\
		.replace("output%1%", f"{paths['output_dir']}/{run_time}/enrichment_plot.pdf")\
		.replace("output%2%", f"{paths['output_dir']}/{run_time}/enrichment_plot_top10.pdf")\
		.replace("output%3%", f"{paths['output_dir']}/{run_time}/enrichment_analysis.csv")\
	
	return r_code_use


def plot_R(args, paths, run_time):

	rcode = '''

# 加载包
library("DOSE")
library("ggplot2")

# 加载数据集
plot_data_noNA = read.csv("%juse%1", header=TRUE)
wid = %juse%4
hei = %juse%5
title = "%juse%7"

# 处理数据
plot_data_noNA = plot_data_noNA[complete.cases(plot_data_noNA$Description),]
plot_data_noNA = transform(plot_data_noNA, Count = as.numeric(Count),
						   qvalue = as.numeric(qvalue))
plot_data_noNA = plot_data_noNA[order(plot_data_noNA$qvalue,-plot_data_noNA$Count),]
plot_data_noNA$Ontology[plot_data_noNA$Ontology == "cellular_component"] = "Cellular Component"
plot_data_noNA$Ontology[plot_data_noNA$Ontology == "biological_process"] = "Biological Process"
plot_data_noNA$Ontology[plot_data_noNA$Ontology == "molecular_function"] = "Molecular Function"

Top15 = c()
CC = 0
BP = 0
MF = 0
for(i in 1:length(plot_data_noNA$Ontology)){
  if(plot_data_noNA$Ontology[i] == "Cellular Component"){
	CC = CC + 1
	if(CC <= 5){
	  Top15 = append(Top15,(i))
	}
  }
  if(plot_data_noNA$Ontology[i] == "Biological Process"){
	BP = BP + 1
	if(BP <= 5){
	  Top15 = append(Top15,(i))
	}
  }
  if(plot_data_noNA$Ontology[i] == "Molecular Function"){
	MF = MF + 1
	if(MF <= 5){
	  Top15 = append(Top15,(i))
	}
  }
}

# 进行气泡图绘制
enrichment_plot = ggplot(plot_data_noNA[Top15,],aes(x = parse_ratio(GeneRatio),y = reorder(%juse%6, Count))) + geom_point(aes(size=Count,color=qvalue,)) +
  scale_color_gradient(low = "red", high = "blue") + theme_bw() + ylab(NULL) + xlab("GeneRatio") + 
  facet_wrap(~Ontology, scale="free",ncol = 1,strip.position = "right") + 
  theme(text = element_text(size = 15))

enrichment_plot_top10 = ggplot(plot_data_noNA[1:10,],aes(x = parse_ratio(GeneRatio),y = reorder(%juse%6, Count))) + geom_point(aes(size=Count,color=qvalue,)) +
  scale_color_gradient(low = "red", high = "blue") + theme_bw() + ylab(NULL) + xlab("GeneRatio") + 
  theme(text = element_text(size = 15))

if(title != "NULL"){
  enrichment_plot = enrichment_plot + ggtitle(title)
  enrichment_plot_top10 = enrichment_plot_top10 + ggtitle(title)
}

# 保存图及富集分析表格
pdf("output%1%",width = wid,height = hei)
enrichment_plot
dev.off()

pdf("output%2%",width = wid,height = hei)
enrichment_plot_top10
dev.off()


'''

	r_code_use = rcode.replace("%juse%1", paths['csv_dir'])\
		.replace("%juse%4", args.width)\
		.replace("%juse%5", args.height)\
		.replace("%juse%6", args.yaxis)\
		.replace("%juse%7", args.title)\
		.replace("output%1%", f"{paths['output_dir']}/{run_time}/enrichment_plot.pdf")\
		.replace("output%2%", f"{paths['output_dir']}/{run_time}/enrichment_plot_top10.pdf")\
		
	return r_code_use

def run_r_script(r_code, paths, run_time):
	os.makedirs(f"{paths['output_dir']}/{run_time}", exist_ok=True)
	script_path = f"{paths['output_dir']}/{run_time}/enrichment_plot.R"
	with open(script_path, 'w') as f:
		f.write(r_code)
	os.system(f'Rscript {script_path}')


def main():

	run_time = time.strftime('%Y%m%d-%H%M%S')
	args = get_args()
	paths = get_path(args)
	r_code = R_code(args, paths, run_time) if args.csv == 'NULL' else plot_R(args, paths, run_time)
	run_r_script(r_code, paths, run_time)
	print(f'Finished! See output at {paths["output_dir"]}')


if __name__ == "__main__":
	main()
