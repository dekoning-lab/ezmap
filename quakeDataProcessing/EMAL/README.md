#EMAL

EMAL is a program designed to allow for the accurate estimation of sample composition given tabular BLAST results.

##Usage

EMAL is a three part program that has a select number of dependencies. The different stages of EMAL are designed to be run in sequence and require that one completes prior to the initialization of the next stage. The three different parts of EMAL are:

#### 1. EMAL - DataPrep
#####Required Files
| File     | Description   | Possible Values|
| ---|---|---|
|all.fna|A file containing all the sequences used to BLAST the sample against| Full file path|
|gi_taxid_nucl.dmp|A file containing all the Nucleotide Identifiers and their corresponding NCBI Taxonomy Identifiers|Full file path|

####2. EMAL - Main
####3. EMAL - Post