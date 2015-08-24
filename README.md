# Viral Metagenomics Abunadnacne Pipeline (V0.9b)

VMAP is a pipeline designed to allow for the estimation community structure from DNA sequence data. VMAP has been designed to work with viral sequence data however it can also be used with other information sources such as bacterial and fungal communities.

## Features
  - Broad number of use cases
  - Graphic HTML report generated at end of processing
  - Small number of dependecies 

### Dependecies
Because VMAP was designed to limit the number dependencies it runs using only Python3 and a select few required modules.

- Python3 
- NumPy & SciPy (http://docs.scipy.org/doc/)
- Biopython (http://biopython.org)

#### Programs Used by VMAP
VMAP uses and number of pieces of free open source software to allow for it to generate all that it does.

- [PRINSEQ](http://prinseq.sourceforge.net)
- [Bowtie 2](http://bowtie-bio.sourceforge.net)
- [SAMTools](http://samtools.sourceforge.net)
- [NCBI Blast](http://blast.ncbi.nlm.nih.gov/Blast.cgi?PAGE_TYPE=BlastDocs&DOC_TYPE=Download) 
- EMAL


----------


## Setup
 

 1. Download the current release of VMAP
 2. Unzip it.
 3. Place the entire VMAP folder somewhere accessible on your computer
 4. Make sure to have installed Numpy, Scipy, & Biopython.
	 - To tes this run the following in the command line.

```python
python3
import numpy
import scipy
import Bio
```