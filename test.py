import argparse
from collections import defaultdict

genes = defaultdict(list)
mrnas = {}

with open("./test.gff") as f:
    for line in f:
        # 忽略以 '#' 开头的注释行
        if not line.startswith('#'):
            fields = line.split('\t')

            if fields[2] == 'gene':
                # 对于 gene 类型的特征，直接保存该特征
                attributes = dict(field.split('=') for field in fields[8].split(';') if '=' in field)
                gene_id = attributes['ID']
                genes[gene_id].append((fields[0], int(fields[3]), int(fields[4]), fields[6]))
            
            elif fields[2] == 'mRNA':
                # 对于 mRNA 类型的特征，先将其存储起来，在找到其对应的基因后再处理
                attributes = dict(field.split('=') for field in fields[8].split(';') if '=' in field)
                mrna_id = attributes['ID']
                parent_id = attributes['Parent']  # 找到该 mRNA 的父亲 ID
                mrnas[mrna_id] = (parent_id, fields[0], int(fields[3]), int(fields[4]), fields[6])

# 将 MRNA 转换为其所属基因的 ID，并将每个基因 ID 与其位置列表关联起来
for mrna_id, (gene_id, chromosome, start, stop, strand) in mrnas.items():
    if gene_id in genes:
        genes[gene_id].append((chromosome, start, stop, strand))
    else:
        # 如果找不到该 mRNA 对应的基因，输出警告信息，并忽略该 mRNA 的位置信息。
        print(f"warning: MRNA {mrna_id} has a parent ({gene_id}) that is not in the GFF file")
