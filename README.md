# viral-metagen
NGS pipeline for viral metagenomics analysis

#Using on SLURM
prinseqBatchScript.sbacth needs to be run which will grab all the different FASTQ files and then pass that array fo files to prinseqIndividualScript.sh to run all files through prinseq

Default PRINSEQ parameters:

out_format=3 (FATSQ Files)
min_qual_score=33
lc_method="dust"
lc_threshold=7 

Note: PRINSEQ parameters can be changes in prinseqIndvidualScript.sbatch