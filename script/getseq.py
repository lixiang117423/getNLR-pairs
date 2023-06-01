import argparse


def extract_sequence_from_fasta(fasta_file, id_file):
    with open(id_file, 'r') as f:
        ids = [line.strip() for line in f]
    
    with open(fasta_file, 'r') as f:
        records_dict = {}
        current_id = None
        for line in f:
            if line.startswith('>'):
                record_id = line.lstrip('>').rstrip('\n')
                current_id = record_id if record_id in ids else None
                if current_id is not None:
                    records_dict[current_id] = ''
            else:
                if current_id is not None:
                    records_dict[current_id] += line.strip()

    return records_dict


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Extract sequences with specified IDs from a fasta file')
    parser.add_argument('-i', '--id', required=True, help='Path to a file containing target IDs (one per line)')
    parser.add_argument('-f', '--fasta', required=True, help='Path to input fasta file')
    parser.add_argument('-o', '--output', required=True, help='Path to output fasta file')
    args = parser.parse_args()

    records_dict = extract_sequence_from_fasta(args.fasta, args.id)

    with open(args.output, 'w') as output_file:
        for seq_id in records_dict:
            sequence = records_dict[seq_id]
            output_file.write('>' + seq_id + '\n')
            for i in range(0, len(sequence), 60):
                output_file.write(sequence[i:i+60] + '\n')
