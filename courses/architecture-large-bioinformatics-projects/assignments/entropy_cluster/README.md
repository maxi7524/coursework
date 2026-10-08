


### TODO 

#### Main idea 

- learn how to use 

#### Scripts 
Plan is to make again smk file which manages whole process

##### Download and prepare data (task 1)

General structure idea (this will be in snakemake, all other scripts with just return everything in given folder)

TODO:
1. Download
- download (wget)
- extract (gunzip)
- check how many sequences you have in each file (e.g. grep)
- params for: .... (what we download ??? )
2. Prepare (join)
- write script that will normalize (wrap) the sequence lines (join them into one line):

python3 normalize_fasta.py -i UP000000625_83333.fasta -o UP000000625_83333_flat.fasta

e.g. 
```shell
>sp|P04982|RBSD_ECOLI D-ribose pyranase OS=Escherichia coli (strain K12) OX=83333 GN=rbsD PE=1 SV=3
MKKGTVLNSDISSVISRLGHTDTLVVCDAGLPIPKSTTRIDMALTQGVPSFMQVLGVVTN
EMQVEAAIIAEEIKHHNPQLHETLLTHLEQLQKHQGNTIEIRYTTHEQFKQQTAESQAVI
RSGECSPYANIILCAGVTF
>sp|P0DPM9|YKGV_ECOLI Protein YkgV OS=Escherichia coli (strain K12) OX=83333 GN=ykgV PE=1 SV=1
MSAFKLPDTSQSQLISTAELAKIISYKSQTIRKWLCQDKLPEGLPRPKQINGRHYWLRKD
VLDFIDTFSVRESL

becames:
>sp|P04982|RBSD_ECOLI D-ribose pyranase OS=Escherichia coli (strain K12) OX=83333 GN=rbsD PE=1 SV=3
MKKGTVLNSDISSVISRLGHTDTLVVCDAGLPIPKSTTRIDMALTQGVPSFMQVLGVVTNEMQVEAAIIAEEIKHHNPQLHETLLTHLEQLQKHQGNTIEIRYTTHEQFKQQTAESQAVIRSGECSPYANIILCAGVTF
>sp|P0DPM9|YKGV_ECOLI Protein YkgV OS=Escherichia coli (strain K12) OX=83333 GN=ykgV PE=1 SV=1
MSAFKLPDTSQSQLISTAELAKIISYKSQTIRKWLCQDKLPEGLPRPKQINGRHYWLRKDVLDFIDTFSVRESL
```
3. Prepare (split into certain length) + additonal parameter that give test set (here we need to sample at random certain k number of sequenes) 
- one script for splitting (n_samples_per_file), with addiotnal params test n_samples_test (those probes in n_samples_test are not appearing later in splitting ~ for not calculating those twice)


##### Main part predicting 

4. Script for running predictions
- here we would like also gather information about what time takes for different file size etc. no get understading about how process scales 
    - here we use fastass files so we could create file with general structre that take into consideration stats given from fasta files 
        - like sequence length, (time per length for given program etc.) 
        - average time taken by sequence (we assume we have representative probe) 
        - how valid are those test (we can create function that compares f.e. certain lenght threshold in those join files vs this sampled (use just simply statitsics like std(length_distribution), mean(length_distribution)))
    - if we use additonal param - test it will caculate statitics (it will take probably a little longer because we calculate all timings)
    - normally we run without statitscs (but add additional saving moments - after certain time we should save results) 
    - 

5. Later - statistics scripts - here we will load data to some .ipynb 



### Remarks 

#### Jobs 

Limits
- You are limited to jobs amount (you need to mount new tasks to them ~ should have additional processors) 

Names
- 8 signs at maximum (programs to check) - we need to limit ourselfs to meaningful short answers 


#### 