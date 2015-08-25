#EMAL 

EMAL is a program designed to allow for the accurate estimation of sample composition given tabular BLAST results. 

##Usage

EMAL is a three part program that has a select number of dependencies. The different stages of EMAL are designed to be run in sequence and require that one completes prior to the initialization of the next stage. The three different parts of EMAL are:

### 1. EMAL - DataPrep
####Required Files
| File     | Description   | Possible Values|
| ---|---|---|
|all.fna|A file containing all the sequences used to BLAST the sample against| Full file path|
|gi_taxid_nucl.dmp|A file containing all the Nucleotide Identifiers and their corresponding NCBI Taxonomy Identifiers|Full file path|

####all.fna Format Example
Users can provide their own custom reference sequences to EMAL so long as they provide a file in the following format where the genome identifier is between the first and second | characters. In the example below the genome identifier is *253682848*. The file must also contain the genome sequence so that EMAL can determine the length of the sequence.
*Example:*
```
>gi|253682848|ref|NZ_ACSJ01000012.1| Clostridium phage D-1873 CLG.Contig163, whole genome shotgun sequence
CAAAAATAATACCTGTTGAATATTTATAGTCATATTGAATATATGGTGTAGTAAGCAAGTTTTTCACCTCCATTATTTTT
```
####gi_taxid_nucl.dmp Format Example
The user may again provide their own dump file if working with a custom dataset by ensuring that file is in the tabular format below. The genome identifier is presented first followed by the taxonomy identifier. In the example bellow 2, 3, and 4 are genome identifiers while 9913, 9913, and 9646 are their respective identifiers. 
*Example:*
```
2	9913
3	9913
4	9646
```

###2. EMAL - Main
###3. EMAL - Post