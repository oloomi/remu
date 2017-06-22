#!/bin/bash
# Running BCFtools for variant calling

#reference="../data/genomes/Orientia_tsutsugamushi_Ikeda_uid58869/NC_010793.fna"
#file_path="../read-mapping/ot-whole-genome-mutated-70-140/"

#alignment_files="corrected-ot-wg-mutated-se-mapping-remu-sorted"

#alignment_files="corrected-other-3mis-mmr-sorted"

#alignment_files="ot-wg-mutated-se-sorted
#ot-wg-mutated-se-mapping-best-match-sorted
#ot-wg-mutated-se-mapping-report-all-sorted
#corrected-other-3mis-mmr-sorted
#corrected-ot-wg-mutated-se-mapping-remu-sorted"

reference="../data/genomes/Mycobacterium_tuberculosis_H37Rv_uid57777/NC_000962.fna"
#file_path="../read-mapping/mtb-whole-genome-mutated-70-140/"
file_path="../read-mapping/mtb-whole-genome-mutated-100-140/"

alignment_files="simple-bayesian-mtb-wg-mutated-se-mapping-sorted"

#alignment_files="mtb-wg-mutated-se-sorted
#mtb-wg-mutated-se-mapping-best-match-sorted
#mtb-wg-mutated-se-mapping-report-all-sorted
#corrected-other-3mis-mmr-sorted
#corrected-mtb-wg-mutated-se-mapping-remu-sorted"


#alignments="../read-mapping/mtb-mutated-long-repeats/corrected-mappings-mtb-mutated-700-100-1-10runs.sorted"

#bcftools mpileup -f $reference $alignments.bam | bcftools call -mv --ploidy 1 -P 1.1e-1 -o $alignments-variants.vcf

for file in $alignment_files
do
	echo "\nVariant calling for: $file\n"
	bcftools mpileup -f $reference $file_path$file.bam | bcftools call -mv --ploidy 1 -P 1.1e-1 -o $file_path$file-variants-mv.vcf
#	bcftools mpileup -f $reference $file_path$file.bam | bcftools call -cv --ploidy 1 -p 0.1 -o $file_path$file-variants-consensus-p0.1.vcf
	bcftools mpileup -f $reference $file_path$file.bam | bcftools call -cv --ploidy 1 -p 0.5 -o $file_path$file-variants-consensus-p0.5.vcf
	freebayes -f $reference -p 1 $file_path$file.bam >$file_path$file-variants-freebayes.vcf
done

echo "\n=== Done ===\n"
