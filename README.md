# Viral Metagenomics Abunadnacne Pipeline (V0.9b)

VMAP is a pipeline designed to allow for the estimation community structure from DNA sequence data. VMAP has been designed to work with viral sequence data however it can also be used with other information sources such as bacterial and fungal communities.

## Features
  - Broad number of use cases
  - Graphic HTML report generation
  - Small number of dependecies 

### Dependecies
Because VMAP was designed to limit the number dependencies it runs using only Python3 and a select few required modules.

- Python3 
- [NumPy & SciPy](http://docs.scipy.org/doc/)
- [Biopython](http://biopython.org)

#### Programs Used by VMAP
VMAP uses and number of pieces of free open source software to allow for it to generate all that it does.

- [PRINSEQ](http://prinseq.sourceforge.net)
- [Bowtie 2](http://bowtie-bio.sourceforge.net)
- [SAMTools](http://samtools.sourceforge.net)
- [NCBI Blast](http://blast.ncbi.nlm.nih.gov/Blast.cgi?PAGE_TYPE=BlastDocs&DOC_TYPE=Download) 
- EMAL


----------


## Setup
 

 1. Download the current release of VMAP.
 2. Unzip it.
 3. Place the entire VMAP folder somewhere accessible on your computer.
 4. Make sure to have installed Numpy, Scipy, & Biopython.
	 - To test this run the following in the command line editor.

```python
python3
import numpy
import scipy
import Bio
```

Once that is done you have VMAP correctly setup on your computer.

##Configuration

Before running VMAP it is important to have a few things setup.

 1. Create a new folder where all of the results will be placed.
 2. Make sure that you have moved all the original FASTA files into a folder that contains only those files.
 3. Configure the parameters within the param.config file that can be found in the main VMAP folder. *See the parameters section bellow to see what can be modified to suit your needs.*

## Running VMAP

To run VMAP make sure you have installed it correctly and have configured the files and parameters correctly.

1. Open up a new terminal window.
2. Navigate to the VMAP folder.
3. The following is the most basic command that VMAP will run.


```
python3 VMAP.py -d /path/to/fasta/files/ -projDir /path/to/output/folder/ -mt 4
```
The above command will start sumbitting the different VMAP steps to the SLURM job manager. 


    

