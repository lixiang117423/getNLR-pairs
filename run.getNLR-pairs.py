import argparse
import os
import sys
import time

# 创建解析器对象
parser = argparse.ArgumentParser(description='A program to do something useful')

# 添加参数选项
parser.add_argument('--input_folder', '-i', help='path to input folder')
parser.add_argument('--sample_list', '-s', help='path to sample list file')
parser.add_argument('--temp_folder', '-o', help='path to temp folder')

# 解析命令行参数
args = parser.parse_args()

# 使用参数选项中的值进行操作
input_folder = args.input_folder
sample_list = args.sample_list
output_folder = args.temp_folder
temp1 = "{"
temp2 = "}"

# 定义函数
def check_files_and_extract_seq(sample_file):
    data_folder = input_folder # 更改为您的数据文件夹路径
    with open(sample_list, "r") as f:
        for line in f:
            start_time = time.time()
            sample = line.strip()
            fa_file = os.path.join(data_folder, sample + ".fa")
            gff_file = os.path.join(data_folder, sample + ".gff")
            
            # 提取序列+运行
            if os.path.isfile(fa_file) and os.path.isfile(gff_file):
                gffread_comm = f"{input_folder}/{sample}.gff -g {input_folder}/{sample}.fa -x {output_folder}/{sample}.cds -y {output_folder}/{sample}.pep"
                os.system("gffread " + gffread_comm)
                # print("gffread " + gffread_comm)

                # 提取转录本和基因信息
                gene_location = f"python3 script/getGeneLocation.py -g {input_folder}/{sample}.gff -o {output_folder}/{sample}.gene.info.txt"
                os.system(gene_location)

                # HMMEr鉴定结构域
                hmmer_comm = f"hmmsearch --cpu 10 --domtblout {output_folder}/{sample}.hmmsearch.res.txt --cut_tc PF00931.hmm {output_folder}/{sample}.pep "
                os.system(hmmer_comm)

                # 提取NLR ID
                hmmerres_comm = f"sed '/^#/d' {output_folder}/{sample}.hmmsearch.res.txt | awk {temp1}'print $1'{temp2} | uniq > {output_folder}/{sample}.unique.hmmsearch.id.txt"
                os.system(hmmerres_comm)

                # [NLR-Annotator](https://github.com/steuernb/NLR-Annotator)
                java_comm = f"java -jar ./NLR-Annotator/NLR-Annotator-v2.1b.jar -x ./NLR-Annotator/src/mot.txt -y ./NLR-Annotator/src/store.txt -i {output_folder}/{sample}.cds -g {output_folder}/{sample}.nlr.annotator.txt -t 20"
                os.system(java_comm)

                sed_comm = f"sed '/^#/d' {output_folder}/{sample}.nlr.annotator.txt | awk {temp1}'print $1'{temp2} | uniq > {output_folder}/{sample}.nlr.annotator.id.txt"
                os.system(sed_comm)

                # 合并ID
                # merge all IDs
                mergeid_comm = f"cat {output_folder}/{sample}.unique.hmmsearch.id.txt {output_folder}/{sample}.nlr.annotator.id.txt | uniq > {output_folder}/{sample}.candidate.id.txt"
                os.system(mergeid_comm)
                
                # extract CDS
                getcds_comm = f"python3 script/getseq.py -i {output_folder}/{sample}.candidate.id.txt -f {output_folder}/{sample}.cds -o {output_folder}/{sample}.all.candidate.cds.fa"
                os.system(getcds_comm)
                # run NLR-Annotator
                anno_comm = f"java -jar ./NLR-Annotator/NLR-Annotator-v2.1b.jar -x ./NLR-Annotator/src/mot.txt -y ./NLR-Annotator/src/store.txt -i {output_folder}/{sample}.all.candidate.cds.fa -g {output_folder}/{sample}.res.gff -t 10"
                os.system(anno_comm)
                
                # parse unique ID
                sed_comm = f"sed '/^#/d' {output_folder}/{sample}.res.gff | awk {temp1}'print $1'{temp2} | uniq > {output_folder}/{sample}.res.id.txt"
                os.system(sed_comm)

                # get nlr-pairs
                run_r = f"Rscript script/getNLRpairs.R {output_folder}/{sample}.gene.info.txt {output_folder}/{sample}.res.id.txt ./{sample}.nlr.pairs.txt"
                os.system(run_r)
                
            else:
                if not os.path.isfile(fa_file):
                    sys.exit(f"Error: Genome file not found for {sample}")
                if not os.path.isfile(gff_file):
                    sys.exit(f"Error: GFF file not found for {sample}")
            
            end_time = time.time()
            time_comm = "{} is OK! Running time：{:.2f} seconds.".format(sample, end_time-start_time)
            print(time_comm)
            print("====================")

check_files_and_extract_seq(sample_list)

os.system(f"rm -rf {output_folder}")


