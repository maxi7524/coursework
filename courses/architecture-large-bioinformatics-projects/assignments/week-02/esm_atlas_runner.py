import os 
from pathlib import Path
import argparse



# TODO
# input: folder with .fasta files of following format
# >M.genitalium-WP_318023720
# MKILHDGPPYANGSIHVGHALNKILKDFILRSWLYEGYDVVFIPGWDCHGLPIEHAVSKKNPSSYSNLSTVEKRKLCHQFALSQIAVQKEQFQRLGLLNDFQNCYYTIDESFQFKELELFLQAIKKRAHFSRFKTNLLITNFKNFTCWSGNWI
# >M.genitalium-WP_268741291
# MRSAKQKLTWLQKLICFEPKWIKDKILAILKEVNLNDYVSCIIKDLSAGQKQRVEIAKLFFKSPKLLLVDEPTTGLDPLTASKIMDLITDFVKREKITLVFVTHDIDLALKYSTRIIALKNHALVLDRLTEKLTKEQLYKIYDN
# >M.genitalium-WP_009885822
# MDGGQQGSFFGLLVIVIPIILLIVFFSKKKGAQKNDFSGEGGNRSSRKDEVWKTIKQFLQEKNERGKEIIKTFVAKKPNPLHSKKDRKLFNQEIQAYITSNNLGKSEAKRYKNEQTRLMQRELYCIYFVTKDAKSTEVDDARIIEAEVYQKPTKTKSTPERLIRILGLKNFETEMQWIQPLMVREEKRKEKEEQKKLKLAARELKKKKKKKIKKPKRNQKSEKCLKLFSLVLQRFQKNV
# 
# output: results of proteins returned to folder and log_esm_atlas_runner.txt (for saving information)

# parameters 
# folder
# ilość procesów na raz 
# 


# sama funkcja
# będziemy wywoływać komende:
# curl -X POST --data "KVFGRCELAAAMKRHGLDNYRGYSLGNWVCAAKFESNFNTQATNRNTDGSTDYGILQINSRWWCNDGRTPGSRNLCNIPCSALLSSDITASVNCAKKIVSDGNGMNAWVAWRNRCKGTDVQAWIRGCRL" https://api.esmatlas.com/foldSequence/v1/pdb/
# na każdym PLIKU (bo tym poprzednim skryptem rozdzielamy jak głęboko dzielimy te pliki, ten ma odpowiadać tylko za rozdizelenie pracy) 

# będzie trzeba odpowiednio zaimplementować wielowątkowośc, równoległośc - sugestia skrypt 

def esm_atlas_run_file(): 


def esm_atlas_manager():
    ...




def main():
    """Function for argparsing"""

    """
    argparser for CLI fasta_splitter
    """
    parser = argparse.ArgumentParser(description='Splits FASTA sequences into separate files.')

    # obtain args
    ## paths
    parser.add_argument(
        'paths', nargs='+', 
        help="Input .fasta files, folders or wildcards (e.g. *.fasta). The LAST path is the output folder."
    )
    
    parser.add_argument('-m', '--threads', type=int, default=0, help="Maximum sequence length (longer sequences will be skipped). 0 = no limit.") 
    
    parser.add_argument('--mode', choices=['separate', 'join'], default='separate', 
                        help="'separate' mode distinguishes input files (prefixes) and create distinguish folders. 'join' mode merges everything together.")

    args = parser.parse_args()

    if len(args.paths) < 2:
        parser.error("You must provide at least one input path and one output path at the end.")

    if args.size <= 0:
        parser.error("Size must be greater than 0!")

    ## split paths (last value)
    output_path = args.paths[-1]
    input_paths = args.paths[:-1]

    fasta_split(
        input_paths=input_paths, 
        output_path=output_path,
        size=args.size,
        mode=args.mode
    )