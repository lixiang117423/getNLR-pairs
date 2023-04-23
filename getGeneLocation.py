import re
import argparse

# Define argument parser
parser = argparse.ArgumentParser(description="Extract mRNA and Gene information from GFF file.")
parser.add_argument("-g", "--gff", type=str, help="Input GFF file path.")
parser.add_argument("-o", "--output", type=str, default="output.txt", help="Output file path.")
#parser.add_argument("-H", "--show_help", action="store_true", help="Show this help message.")

# Parse command line arguments
args = parser.parse_args()
# if args.show_help:
#     parser.print_help()
#     exit(0)

# Check if input GFF file is specified
if args.gff is None:
    print("Please specify input GFF file using -g parameter.")
    exit(1)

# Define regular expression to extract relevant information from attribute column
mRNA_id_re = re.compile('ID=(.*?);')
gene_id_re = re.compile('ID=(.*?);')
gene_name_re = re.compile('Name=(.*?)[;\n]')

# Read GFF file and extract information 
with open(args.gff, "r") as gff_file, open(args.output, "w") as out_file:
    out_file.write("gene.id\tChr\tgene.start\tgene.end\tgene.strand\tmRNA.id\tmRNA.start\tmRNA.end\n")
    # Initialize gene information dictionary
    gene_dict = {}
    
    for line in gff_file:
        # Skip comment lines and blank lines
        if line.startswith("#") or line.strip() == "":
            continue
        
        # Parse fields according to GFF format
        seqid, source, type_, start, end, score, strand, phase, attributes = line.strip().split("\t")
        
        # Extract relevant information for gene type
        if type_ == "gene":
            gene_id = gene_id_re.search(attributes).group(1)
            #gene_name = gene_name_re.search(attributes).group(1)
            
            # Store gene position information in dictionary
            gene_dict[gene_id] = {
                "name": gene_id,
                "seqid": seqid,
                "start": int(start),
                "end": int(end),
                "strand": strand,
            }
        
        # Extract relevant information for mRNA type
        elif type_ == "mRNA":
            mRNA_id = mRNA_id_re.search(attributes).group(1)
            gene_id = re.search('Parent=(.*?);', attributes).group(1)
            gene_info = gene_dict[gene_id]
            
            # Write output information to file
            #out_file.write(f"{mRNA_id}\t{start}\t{end}\t{strand}\t{gene_info['name']}\t{gene_info['start']}\t{gene_info['end']}\t{gene_info['strand']}\t{gene_info['seqid']}\n")
            out_file.write(f"{gene_info['name']}\t{gene_info['seqid']}\t{gene_info['start']}\t{gene_info['end']}\t{gene_info['strand']}\t{mRNA_id}\t{start}\t{end}\n")
