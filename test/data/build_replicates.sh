

ID,type,condition,replicat,sample_name
1, IP,    WT,   1, 1_S1_L001
2, IP,    yeiL, 1, 2_S2_L001
3, IP,    yeiL_bis, 1, 3_S3_L001
4, Input, WT, 1, 4_S4_L001
5, Input, yeiL, 1, 5_S5_L001
6, Input, yeiL_bis,   1, 6_S6_L001

# build replicates for IP WT sample
gunzip -c 1_S1_L001_R1_001.fastq.gz | head -n 13000000 > IP_WT_rep1_R1_.fastq
gunzip -c 1_S1_L001_R2_001.fastq.gz | head -n 13000000 > IP_WT_rep1_R2_.fastq
gunzip -c 1_S1_L001_R1_001.fastq.gz | tail -n 13000000 > IP_WT_rep2_R1_.fastq
gunzip -c 1_S1_L001_R2_001.fastq.gz | tail -n 13000000 > IP_WT_rep2_R2_.fastq

# build replicates for IP yeil sample
gunzip -c 2_S2_L001_R1_001.fastq.gz | head -n 11000000 > IP_yeiL_rep1_R1_.fastq
gunzip -c 2_S2_L001_R2_001.fastq.gz | head -n 11000000 > IP_yeiL_rep1_R2_.fastq
gunzip -c 2_S2_L001_R1_001.fastq.gz | tail -n 11000000 > IP_yeiL_rep2_R1_.fastq
gunzip -c 2_S2_L001_R2_001.fastq.gz | tail -n 11000000 > IP_yeiL_rep2_R2_.fastq

