#!/bin/bash
# Running other multi-mapping resolution methods

if [ "$1" = "-s" ]; then
  ref_genome="../../genome-ref/ref-genome.fna"
elif [ "$1" = "-r" ]; then
  ref_genome="./genome-mutated/mutated-genome.fna"
else
  echo "Invalid argument in variant-calling.sh!"
fi

# ----------- Bowtie2 ----------
alignments="./mappings/bowtie/bowtie-mapping-report-all-sorted"
alignments_sam="./mappings/bowtie/bowtie-mapping-report-all"
outfile="./mappings/bowtie/bowtie"

# MMR method
samtools sort -n $alignments.bam -o $alignments-id-sorted.bam

/usr/bin/time -v mmr -o $outfile-mmr.bam -F 3 -b -R $2 $alignments-id-sorted.bam

sam_file=$outfile-mmr
samtools sort $sam_file.bam -o $sam_file-sorted.bam
samtools index $sam_file-sorted.bam

echo "\n=== Bowtie + MMR Multimapping Resolution Done ===\n"

chmod +x /mnt/remu/remu.py

# REMU method
/usr/bin/time -v remu.py -g $ref_genome -i $alignments_sam.sam -o $outfile-remu.sam -r 10

sam_file=$outfile-remu
samtools view -bS $sam_file.sam -o $sam_file.bam
samtools sort $sam_file.bam -o $sam_file-sorted.bam
samtools index $sam_file-sorted.bam

echo "\n=== Bowtie + REMU Multimapping Resolution Done ===\n"

# ----------- BWA ----------
alignments="./mappings/bwa/bwa-mapping-report-all-sorted"
alignments_sam="./mappings/bwa/bwa-mapping-report-all"
outfile="./mappings/bwa/bwa"

# MMR method
samtools sort -n $alignments.bam -o $alignments-id-sorted.bam

/usr/bin/time -v mmr -o $outfile-mmr.bam -F 3 -b -R $2 $alignments-id-sorted.bam

sam_file=$outfile-mmr
samtools sort $sam_file.bam -o $sam_file-sorted.bam
samtools index $sam_file-sorted.bam

echo "\n=== BWA + MMR Multimapping Resolution Done ===\n"

# REMU method
/usr/bin/time -v remu.py -g $ref_genome -i $alignments_sam.sam -o $outfile-remu.sam -r 10

sam_file=$outfile-remu
samtools view -bS $sam_file.sam -o $sam_file.bam
samtools sort $sam_file.bam -o $sam_file-sorted.bam
samtools index $sam_file-sorted.bam

echo "\n=== BWA + REMU Multimapping Resolution Done ===\n"
