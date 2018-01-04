#!/bin/bash
# Running other multi-mapping resolution methods

reference="../data/genomes/MTB-H37Rv-back-mutated-full.fna"
alignments="../read-mapping/mtb-h37rv-back-mutated/mtb-h37rv-back-mutated-mapping-report-all-sorted"
outfile="../read-mapping/mtb-h37rv-back-mutated/mtb-h37rv-back-mutated-mapping"

#reference="../data/genomes/Orientia_tsutsugamushi_Ikeda_uid58869/NC_010793.fna"
#alignments="../read-mapping/ot-whole-genome-mutated-70-140/ot-wg-mutated-se-mapping-report-all"
#outfile="../read-mapping/ot-whole-genome-mutated-70-140/corrected-other-3mis"

#reference="../data/genomes/Mycobacterium_tuberculosis_H37Rv_uid57777/NC_000962.fna"
#alignments="../read-mapping/mtb-whole-genome-mutated-100-140/mtb-wg-mutated-se-mapping-report-all"
#outfile="../read-mapping/mtb-whole-genome-mutated-100-140/corrected-other-3mis"
#alignments="../read-mapping/mtb-whole-genome-mutated-70-140/mtb-wg-mutated-se-mapping-report-all"
#outfile="../read-mapping/mtb-whole-genome-mutated-70-140/corrected-other-3mis"

#reference="../data/genomes/mtb-genome-extract.fna"
#alignments="../read-mapping/mtb-mutated-long-repeats/mtb-mutated-se-mapping-report-all"
#outfile="../read-mapping/mtb-mutated-long-repeats/corrected-other-3mis"

export PATH=$PATH:/mnt/e/Codes/other-methods/mmr/mmr

samtools sort -n -o $alignments-id-sorted.bam $alignments.bam
#mmr -o $outfile.mmr.bam -f -b -R 150 $alignments.id-sorted.bam
#mmr -o $outfile.mmr.bam -F 0 -b -R 150 $alignments.id-sorted.bam

STARTTIME=$(date +%s)

mmr -o $outfile-mmr.bam -F 3 -b -R 150 $alignments-id-sorted.bam

ENDTIME=$(date +%s)
echo "MMR running time $(($ENDTIME - $STARTTIME)) seconds\n"

sam_file=$outfile-mmr
samtools sort $sam_file.bam -o $sam_file-sorted.bam
samtools index $sam_file-sorted.bam

echo "\n=== Trying Other Multimapping Resolution Tools Done ===\n"