import random


def extract_genome(ref_genome_file, start_pos, length, output_file, mutate=False, repeats_file_name=None):
    """
    Gets a Fasta file, extracts a part of genome, and writes it back to a new Fasta file as a new reference genome.
    """
    genome_seq = ""
    with open(ref_genome_file) as ref_genome:
        with open(output_file, 'w') as new_genome:
            for line in ref_genome:
                # Skip header lines
                if line[0] == ">":
                    #header_line = line.rstrip().split("|")
                    # new_genome.write("{} {}-{}\n".format("|".join(header_line), start_pos, start_pos + length - 1))
                    # new_genome.write("{}|{}_{}|\n".format("|".join(header_line[:4]),start_pos, start_pos + length - 1))
                    new_genome.write(line)
                else:
                    genome_seq += line.rstrip()

            # Extracted genome sequence
            new_genome_seq = genome_seq[start_pos - 1: start_pos + length - 1]

            if mutate:
                new_genome_seq = mutate_genome(repeats_file_name, new_genome_seq, start_pos, length,
                                                "{}-mutations.txt".format(output_file[:-4]))

            # Writing the new genome sequence to file, 70 characters per line
            line_width = 70
            for i in range(length // line_width):
                new_genome.write(new_genome_seq[i * line_width: (i + 1) * line_width])
                new_genome.write("\n")
            # Writing the last remainder part of genome
            if length % line_width != 0:
                new_genome.write(new_genome_seq[-(length % line_width):])
    return True


def mutate_genome(repeats_file_name, genome_sequence, start_pos, genome_length, mutation_locations_file):
    random.seed(12)

    # [[length, start_1, start_2, ...], ...]
    repeats_list = []
    # [range(start, start + length), ...]
    repeats_ranges = set()
    with open(repeats_file_name) as repeats_file:
        for line in repeats_file:
            fields = line.split()
            # For repeats on reverse strand, remove 'r' from end position
            if fields[1][-1] == 'r':
                fields[1] = fields[1][:-1]
            # Deducting start_pos to make absolute positions for the new genome extract
            (start, end, length) = (int(fields[0]) - start_pos, int(fields[1]) - start_pos, int(fields[2]))
            # Filtering repeats that are smaller than read length
            #if length > 150:
            # Some repeat coordinates may exceed the extract of the genome we are looking for
            if start + length < genome_length and end + length < genome_length:
                if repeats_list and repeats_list[-1][0] == length and repeats_list[-1][1] == start:
                    repeats_list[-1].append(end)
                else:
                    repeats_list.append([length, start, end])

                # Adding this range to ranges of repeat positions
                repeats_ranges.add(range(start, start + length))
                repeats_ranges.add(range(end, end + length))

    # Saving repeat ranges to file
    ranges_list = []
    for rng in repeats_ranges:
        ranges_list.append((list(rng)[0], list(rng)[-1], list(rng)[-1] - list(rng)[0] + 1))
    ranges_list.sort()
    with open("{}-ranges.txt".format(repeats_file_name[:-4]), "w") as repeats_ranges_file:
        for rng in ranges_list:
            repeats_ranges_file.write("{}\t{}\t{}\n".format(rng[0], rng[1], rng[2]))

    # Merging repeat ranges and writing them to file
    merged_ranges = []
    for begin, end, rng_len in ranges_list:
        if merged_ranges and merged_ranges[-1][1] >= begin - 1:
            merged_ranges[-1][1] = max(merged_ranges[-1][1], end)
            # Update repeat length
            merged_ranges[-1][2] = merged_ranges[-1][1] - merged_ranges[-1][0] + 1
        else:
            merged_ranges.append([begin, end, end - begin + 1])

    with open("{}-ranges-merged.txt".format(repeats_file_name[:-4]), "w") as repeats_ranges_file:
        for rng in merged_ranges:
            repeats_ranges_file.write("{}\t{}\t{}\n".format(rng[0], rng[1], rng[2]))


    long_repeats = []
    for rng in merged_ranges:
        if rng[2] > 150:
            long_repeats.append(rng)

    # Mutating genome
    new_genome_seq = list(genome_sequence)
    mutations_list = []

    # 25% of regions
    # num_snps = len(merged_ranges) // 4
    num_snps = len(long_repeats) // 2
    # selected_regions = random.sample(merged_ranges, num_snps)
    selected_regions = random.sample(long_repeats, num_snps)
    nucleotides = set(['A', 'C', 'G', 'T'])
    for region in selected_regions:
        mapping_location = region[0]
        base_position = random.choice(range(100, 140))
        # base_position = 140
        final_position = mapping_location + base_position
        print(region, mapping_location, base_position, final_position)
        # Mutating the base
        possible_snps = nucleotides - set(genome_sequence[final_position])
        new_genome_seq[final_position] = random.choice(sorted(list(possible_snps)))
        # Saving this mutation characteristics
        mutations_list.append((final_position + 1, genome_sequence[final_position], new_genome_seq[final_position],
                               base_position, region))

    # Writing mutation locations to file
    mutations_list.sort()
    with open(mutation_locations_file, "w") as mutations_file:
        mutations_file.write("Number of mutations: {}\n".format(num_snps))
        for item in mutations_list:
            mutations_file.write("{}\t{}\t{}\t{}\t{}\n".format(item[0], item[1], item[2], item[3], item[4]))

    # Returning mutated genome sequence
    return "".join(new_genome_seq)



def toy_genome(ref_genome_file, output_file, mutate=False):
    """
    Gets a Fasta file, extracts a part of genome, and writes it back to a new Fasta file as a new reference genome.
    """
    random.seed(12)
    genome_seq = ""
    with open(ref_genome_file) as ref_genome:
        with open(output_file, 'w') as new_genome:
            for line in ref_genome:
                # Skip header lines
                if line[0] == ">":
                    # new_genome.write("{} {}-{}\n".format("|".join(header_line), start_pos, start_pos + length - 1))
                    # new_genome.write("{}|{}_{}|\n".format("|".join(header_line[:4]),start_pos, start_pos + length - 1))
                    #header_line = line.rstrip().split("|")
                    new_genome.write(line)
                else:
                    genome_seq += line.rstrip()

            # Extracted genome sequence
            new_genome_seq = genome_seq[0:5000] + genome_seq[2000:3000] + genome_seq[6000:8000] \
                             + genome_seq[2000:3000] + genome_seq[9000:11000]

            new_genome_seq = list(new_genome_seq)

            # Mutating the genome
            if mutate:
                nucleotides = set(['A', 'C', 'G', 'T'])
                pos = 2129
                print(new_genome_seq[pos])
                possible_snps = nucleotides - set(new_genome_seq[pos])
                new_genome_seq[pos] = random.choice(sorted(list(possible_snps)))
                print(new_genome_seq[pos])

            new_genome_seq = "".join(new_genome_seq)
            # Writing the new genome sequence to file, 70 characters per line
            length = 11000
            line_width = 70
            for i in range(length // line_width):
                new_genome.write(new_genome_seq[i * line_width: (i + 1) * line_width])
                new_genome.write("\n")
            # Writing the last remainder part of genome
            if length % line_width != 0:
                new_genome.write(new_genome_seq[-(length % line_width):])
    return True


def merge_repeat_ranges(repeats_file_name):
    #[[length, start_1, start_2, ...], ...]
    repeats_list = []
    # [range(start, start + length), ...]
    repeats_ranges = set()
    with open(repeats_file_name) as repeats_file:
        for line in repeats_file:
            fields = line.split()
            # Skip header lines
            if not fields[0].isdigit():
                continue
            # For repeats on reverse strand, remove 'r' from end position
            if fields[1][-1] == 'r':
                fields[1] = fields[1][:-1]
            # Deducting start_pos to make absolute positions for the new genome extract
            (start, end, length) = (int(fields[0]), int(fields[1]), int(fields[2]))
            # Filtering repeats that are smaller than read length
            # if length > 150:
            if repeats_list and repeats_list[-1][0] == length and repeats_list[-1][1] == start:
                repeats_list[-1].append(end)
            else:
                repeats_list.append([length, start, end])

            # Adding this range to ranges of repeat positions
            repeats_ranges.add(range(start, start + length))
            repeats_ranges.add(range(end, end + length))

    # Saving repeat ranges to file
    ranges_list = []
    for rng in repeats_ranges:
        ranges_list.append((list(rng)[0], list(rng)[-1], list(rng)[-1] - list(rng)[0] + 1))
    ranges_list.sort()
    with open("{}-ranges.txt".format(repeats_file_name[:-4]), "w") as repeats_ranges_file:
        for rng in ranges_list:
            repeats_ranges_file.write("{}\t{}\t{}\n".format(rng[0], rng[1], rng[2]))

    # Merging repeat ranges and writing them to file
    merged_ranges = []
    for begin, end, rng_len in ranges_list:
        if merged_ranges and merged_ranges[-1][1] >= begin - 1:
            merged_ranges[-1][1] = max(merged_ranges[-1][1], end)
            # Update repeat length
            merged_ranges[-1][2] = merged_ranges[-1][1] - merged_ranges[-1][0] + 1
        else:
            merged_ranges.append([begin, end, end - begin + 1])

    with open("{}-ranges-merged.txt".format(repeats_file_name[:-4]), "w") as repeats_ranges_file:
        for rng in merged_ranges:
            repeats_ranges_file.write("{}\t{}\t{}\n".format(rng[0], rng[1], rng[2]))

    return merged_ranges


def find_repeats_snp(seq1_repeats_file_name, seq2_repeats_file_name, snps_file_name):
    seq1_merged_ranges = merge_repeat_ranges(seq1_repeats_file_name)
    seq2_merged_ranges = merge_repeat_ranges(seq2_repeats_file_name)

    with open(snps_file_name, 'r') as snps_file:
        for line in snps_file:
            fields = line.split()
            # Skip header lines
            if fields[0] == "SNP":
                continue
            seq1_pos = int(fields[3])
            seq2_pos = int(fields[6])

            snp_in_repeat = False

            for start, end, length in seq1_merged_ranges:
                if seq1_pos in range(start, end + 1):
                    print("Seq 1 in repeat: {}-{} : {}".format(start, end, length))
                    print("Distance from repeat margins: {}, {}".format(seq1_pos - start, end - seq1_pos))
                    snp_in_repeat = True

            for start, end, length in seq2_merged_ranges:
                if seq2_pos in range(start, end + 1):
                    print("Seq 2 in repeat: {}-{} : {}".format(start, end, length))
                    print("Distance from repeat margins: {}, {}".format(seq2_pos - start, end - seq2_pos))
                    snp_in_repeat = True

            if snp_in_repeat:
                print(line)


# toy_genome("./data/genomes/Mycobacterium_tuberculosis_H37Rv_uid57777/NC_000962.fna",
#            "./data/genomes/toy-genome-mutated.fna", mutate=True)

# extract_genome("./data/genomes/Mycobacterium_tuberculosis_H37Rv_uid57777/NC_000962.fna", 1, 4411532,
#                "./data/genomes/mtb-whole-genome-mutated-100-140-half.fna", mutate=True,
#                repeats_file_name="./data/genomes/mtb-repeats-sorted.txt")

# merge_repeat_ranges("/home/mohammad/pneumoniae-genomes/h1repeats.txt")
find_repeats_snp("/home/mohammad/pneumoniae-genomes/h1repeats.txt", "/home/mohammad/pneumoniae-genomes/h10repeats.txt",
                 "/home/mohammad/pneumoniae-genomes/mauve-snps.txt")

# extract_genome("./data/genomes/Orientia_tsutsugamushi_Ikeda_uid58869/NC_010793.fna", 1, 2008987,
#                "./data/genomes/ot-whole-genome-mutated-70-140.fna", mutate=True,
#                repeats_file_name="./data/genomes/ot-repeats-sorted.txt")

# def merge_ranges(ranges_file):
#     ranges = []
#     with open(ranges_file) as infile:
#         for line in infile:
#             fields = line.split()
#             ranges.append((int(fields[0]), int(fields[1])))
#     a = sorted(ranges)
#     b = []
#     for begin, end in a:
#         if b and b[-1][1] >= begin - 1:
#             b[-1][1] = max(b[-1][1], end)
#         else:
#             b.append([begin, end])
#
#     with open("{}-merged.txt".format(ranges_file[:-4]), "w") as outfile:
#         for s, e in b:
#             outfile.write("{}\t{}\t{}\n".format(s, e, e - s + 1))
#
# merge_ranges("./data/genomes/mtb-repeats-sorted-ranges.txt")