#!/bin/bash
# Running SAMTools for BAM file generation

#sam_file="../read-mapping/mtb-normal/corrected-mappings-mtb-normal-700-100-5"
#sam_file="../read-mapping/mtb-mutated/corrected-mappings-mtb-mutated-700-100-1-10runs-fs"
sam_file="../read-mapping/mtb-mutated/mtb-mutated-se-mapping-report-all-unique"

# Creating BAM files for corrected mtb read mapping
samtools view -bS $sam_file.sam -o $sam_file.bam
samtools sort $sam_file.bam $sam_file.sorted
samtools index $sam_file.sorted.bam

echo "\n=== Done ===\n"
