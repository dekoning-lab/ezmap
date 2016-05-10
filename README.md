# Ez Metagenomic Abundance Pipeline

EzMap is a pipeline designed to allow for the estimation community structure from raw DNA sequence data. EzMap has been designed to work with viral sequence data however it can also be used with other information sources such as bacterial and fungal communities. 

## Features
  - Support for Viral, Bacterial and Fungal community structure estimation
  - Graphical HTML report generation
  - Limited number of dependencies 

### Dependencies
EzMap was designed to limit the number dependencies, it runs using only Python3 and a select few required modules.

- Python3 
- [NumPy & SciPy](http://docs.scipy.org/doc/)
- [Biopython](http://biopython.org)

#### Programs Used by EzMap
EzMap uses a number of free open source programs to generate results. They are listed here with links to their webpages.  

- [PRINSEQ](http://prinseq.sourceforge.net)
- [Bowtie 2](http://bowtie-bio.sourceforge.net)
- [SAMTools](http://samtools.sourceforge.net)
- [NCBI Blast](http://blast.ncbi.nlm.nih.gov/Blast.cgi?PAGE_TYPE=BlastDocs&DOC_TYPE=Download) 
- EMAL (Custom script written by the de Koning Lab *included with installation files)


----------


## Setup
 

 1. Download the current release of EzMap.
 2. Unzip it.
 3. Place the entire EzMap folder somewhere accessible on your computer.
 4. To install Numpy, Scipy, & Biopython run the setup bash script inside of the EzMap folder.

```
sudo sh setup.sh
```
Once the script completes you have all the EzMap prerequisites correctly setup on your computer.

##Configuration

Before running EzMap it is important to have a few things setup.

 1. Create a **new folder** where all of the results will be placed (referred to as the project directory).
 2. Make sure that you have moved all the original FASTQ files into a folder that contains only those files.
 3. Configure the parameters within the param.config file that can be found in the main EzMap folder. *See the parameters section bellow to see what can be modified.*

## Running EzMap

To run EzMap make sure you have installed it correctly and have configured the files and parameters correctly.

1. Open up a new terminal window.
2. Navigate to the EzMap folder.
3. The following is the most basic command that EzMap will run.


```
python3 ezmap.py -d /path/to/fasta/files/ -projDir /path/to/output/folder/
```
The above command will start submitting the different EzMap steps to the SLURM job manager.

#### Starting the pipeline at a different step

The EzMap pipeline has 7 steps that it uses to process through the original FASTQ files. They are :

1. PRINSEQ - Cleans the FASTQ to remove bad or low quality reads.
2. Bowtie2 - Maps the reads to a genome to remove all reads related to the host organism (ex. Human, mouse, etc.).
3. SAMTools - Gathers all the reads that were not mapped to the host organism.
4. BLAST - BLAST the remaining reads against a specific set of organism genomes (Viral, Bacterial, Fungal, etc.).
5. EMAL Pre - Completes all preprocessing steps required for EMAL.
6. EMAL Main - Using the EM algorithm, estimate the relative amount of reads for each of the organisms BLASTed against.
7. EMAL Post - Generates readable output files in a csv format.

If the pipeline should stop or fail to run at any step the #start-at-step option in the param.config file can be set to any of the steps and then have the pipeline rerun to skip previosuly completed steps.
If #start-at-step is set to 8 or greater then the pipeline will only reprocess the results and generate a updated results webpage.

## Viewing Results

EzMap provides 2 different methods for viewing results. The program will generate an interactive HTML report as well as number of csv files containing the results. 

#### Finding Result Files

The project directory specified prior to running the pipeline will contain 6 folders once all of the steps have complete. Each folder will contain the output files as well as standard output and error files from the SLURM task manager. The folder structure will be inside of the project directory will be:
```
->projectDir
	->1-Cleaning
	->2-HumanMapping
	->3-UnmappedCollection
	->4-OrganismMapping
	->5-RelativeAbundanceEstimation
	->6-FinalResult
		->information
			csv files
		->WEB
		report.html
		viewResults.py
```
All of the csv files containing results will be found within projectDirecotry/6-FinalResult/information/

####Viewing the HTML Report

The final results an also be viewed as part of an HTML report:

 1. Open a new terminal window and navigate to the ```6-FinalResult``` folder.
 2. Run the following command.
 
```
python viewResults.py
```
A new browser window will now open displaying the results of your pipeline run.

Note: if a browser window does not open, open the browser window on the machine and naviagte to:

```
http://localhost:8000
```

##Parameters

####Command  Line Options
| Parameter     | Description   | Possible Values|
| ---|---|---|
|-d or --directory| The full system path to the folder containing only the original FASTQ files| `/path/to/dir` |
|--projDir| The full system path to the folder where all output will be placed|`/path/to/dir`|


####param.config Options
The config file is designed to allow a number of parameters to be set as hardcoded values rather then command line options. Each option occupies a single line within the file. The option always starts with a # and has a = between the option name and its value. When modifying these paramters please ensure there are no space before or after the =.

*Note: in the param.config file if you wish to use the default libraries packaged with EzMap then leave all lines with cwd/ in place.
#####General Parameters (Required)
| Parameter     | Description   | Possible Values|
|---|---|---|---|
|```#project-name```|The name of the project. This will be displayed exactly as spelled in the final report | ```<string>```|
|```#python3-path```|The full file path to python3 within the system. If python3 is installed across the system then enter only ```python3```| /path/python3 |
|```#start-at-step```|Use this parameter to start the pipeline at a different step in case of previous data processing or pipeline failure at a different step | 1 |


#####SLURM Parameters
| Parameter     | Description   | Possible Values| Default |
|---|---|---|---|
|```#slurm-account```| The account on the SLURM job manager| ```<string>``` | NONE |
|```#slurm-share```|Where the job will share multiple jobs on the same node| yes or no | yes|
|```#slurm-partition```|The partition that the job will be run on|  ```<string>```|NONE |
|```#slurm-max-num-threads```|The maximum number of threads that can be assigned to tasks that are multithreaded | 1-32| 1|

#####PRINSEQ Parameters
| Parameter     | Description   | Possible Values| Default |
|---|---|---|---|
|```#prinseq-min_qual_score```|Filter sequence with at least one quality score below min_qual_score.|```<int>```|21|
|```#prinseq-lc_method```| Method to filter low complexity sequences| dust or entropy|dust |
|```#prinseq-lc_threshold```| The threshold value used to filter sequences by sequence complexity. *The dust method uses this as maximum allowed score and the entropy method as minimum allowed value.*|```<int>``` | 7|

#####BLAST Parameters
Descriptions for the BLAST parameters can be found at http://www.ncbi.nlm.nih.gov/books/NBK279675/

| Parameter| Possible Values| Default
|---|---|---|
|```#blastn-db-path```| ```<string>```| NONE|
|```#blastn-dust```| no| no
|```#blastn-reward```| ```<int>```| 1|
|```#blastn-penalty```| ```<int>```| 3|
|```#blastn-word_size```| ```<int>```| 12|
|```#blastn-gapopen```| ```<int>```| 5|
|```#blastn-gapextend```| ```<int>```|2 |
|```#blastn-evalue```| ```<float>```|0.0001 |
|```#blastn-culling_limit```| ```<int>```| 2|
|```#blastn-perc_identity```|```<int>``` |90 |
|```#blastn-min-alignment-length```| ```<int>```| 45|

#####EMAL Parameters
| Parameter     | Description   | Possible Values| Default |
|---|---|---|---|
|```#emal-gi-taxid-nucldmp-path```|The full file path to the gi-taxid-nucldmp file.|```<string>``` |NONE |
|```#emal-acceptance-value```| The value by which the difference between estimate steps are checked. *If the difference between each value between steps is < the value then the estimation ends.*| ```<float>``` |0.0001 |

#####Output Parameters
| Parameter     | Description   | Possible Values| Default |
|---|---|---|---|
|```#extraTableSummedOver```|An additonal table is generated for the final report which shows  the caluaclated genome relative abundances summed by a different category then just the species. *Note: The chosen value must be spelled exactly as shown for this to function.*|SuperKingdom, Q1, Order, Family, SubFamily, Genus |Family|

