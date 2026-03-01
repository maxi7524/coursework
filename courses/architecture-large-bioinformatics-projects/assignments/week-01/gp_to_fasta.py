import os 
import re 
import glob
import argparse
from pathlib import Path

# ------------------------
# helpers
# ------------------------

## Pattern finder 
def gp_matcher(index_name: str, raw_object) -> str:
    r"""
    Extracts the multi-line value associated with a specific keyword (index_name) 
    from a raw GenBank/GenPept formatted text block.

    Args:
        index_name (str): The name of the field to search for (e.g., 'ORGANISM', 'SOURCE').
        raw_object (str): The raw text block containing the parsed sequence record.

    Returns:
        str: The extracted value as a string. Returns 'Empty' if the keyword is not found.

    Regex pattern breakdown:
        r'^\s*'                : Matches the start of a line (^), followed by zero or more 
                                 whitespace characters (\s*). This handles indented sub-fields.
        re.escape(index_name)  : Safely inserts the target keyword, escaping any special regex characters.
        r'\b'                  : Word boundary. Ensures an exact word match so that a search for 
                                 'SOURCE' does not accidentally match 'DBSOURCE'.
        r'\s+'                 : Matches one or more whitespace characters separating the keyword from its data.
        r'(.*?)'               : Capturing group 1. Non-greedily matches any characters (including newlines) 
                                 representing the actual value we want to extract.
        r'(?=\n^[A-Z]|\Z)'     : Positive lookahead. Stops the capture group when it encounters either:
                                 1) A newline followed by an uppercase letter at the start of a line (\n^[A-Z]),
                                    which indicates the start of the next major, unindented section.
                                 2) The absolute end of the string (\Z).

    Regex Flags used:
        re.MULTILINE : Allows the '^' anchor to match the start of each individual line, not just the whole string.
        re.DOTALL    : Allows the '.' wildcard to match newline characters (\n), enabling multi-line text extraction.
    """
    pattern = r'^\s*' + re.escape(index_name) + r'\b\s+(.*?)(?=\n^[A-Z]|\Z)' 
    definition_match = re.search(pattern, raw_object, re.MULTILINE | re.DOTALL)
    definition = definition_match.group(1) if definition_match else 'Empty'
    return definition

def add_prefix(gp_object: dict, flags: dict) -> str:
    r"""
    Generates a formatted FASTA header string based on provided flags.
    
    Args:
        gp_object (dict): Dictionary containing sequence metadata: 
                          'locus', 'gi', 'definition', and 'organism'.
        flags (dict): Configuration flags:
            - 'org_style': 'full', 'abbreviate', 'short'
            - 'id': 'locus' | 'gi' | 'none'
            - 'genename': bool (whether to include definition/genename)
            - 'separator': char (e.g., '-', '|')
    """
    separator = flags.get('separator', '-')
    parts = []

    # 1. Handle Organism Name
    raw_org = gp_object.get('organism', '')
    org_style = flags.get('org_style', 'full')
    
    # Split "Homo sapiens" -> ["Homo", "sapiens"]
    name_parts = raw_org.split()
    
    if org_style == 'full':
        parts.append(raw_org)
    elif org_style == 'abbreviate':
        # "H.sapiens"
        if len(name_parts) >= 2:
            parts.append(f"{name_parts[0][0]}.{name_parts[1]}")
        else:
            parts.append(raw_org)
    elif org_style == 'short':
        # "Homsap" (First 3 of Genus + First 3 of Species)
        if len(name_parts) >= 2:
            short_name = name_parts[0][:3].capitalize() + name_parts[1][:3].lower()
            parts.append(short_name)
        else:
            parts.append(raw_org[:6])

    # 2. Handle ID (Locus) 
    if flags.get('id', '') == 'locus':
        parts.append(gp_object.get('locus', ''))
    elif flags.get('id', '') == 'gi':
        if gp_object.get('gi', ''):
            parts.append(gp_object.get('gi', ''))


    # 3. Handle Definition
    if flags.get("genename", True):
        parts.append(gp_object.get('definition', ''))

    # Join everything with the separator
    return separator.join(parts)



# ------------------------
# main functions
# ------------------------

## Parser - function for 
def gp_file_parser(file_path: Path | str) -> list:
    ### Params 
    file_path = Path(file_path)    

    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        ### retract all proteins 
        raw_objects = re.split(r'(?m)^//', content)
    
    object = []
    for raw_object in raw_objects:
        ### skipping empty record e
        if not raw_object.strip():
            continue
        ### Take information from one protein
        #### LOCUS
        locus = gp_matcher('LOCUS', raw_object)
        locus = re.search(r'^\s*(\S+)', locus).group(1)
        #### DEFINITION: (for Genename flag)
        definition = gp_matcher('DEFINITION', raw_object)
        ##### Get rid of white symbols (\n for long names are problematic)
        definition = " ".join(definition.split())
        
        #### GI idx 
        gi = gp_matcher('VERSION', raw_object)
        gi = re.search(r'GI:(\d+)', gi)
        gi = gi.group(1) if gi else ''

        #### SOURCE - ORGANISM: (for Additional flag)
        source = gp_matcher('SOURCE', raw_object)
        organism = gp_matcher('ORGANISM', source).split('\n')[0] # take first line
        
        #### validation: FEATURES - source (information about sequence length)
        length = gp_matcher('FEATURES', raw_object)
        length = gp_matcher('source', length)  # take first line
        length = re.search(r'1\.\.(\d+)', length).group(1)
        
        #### ORIGIN:
        origin = gp_matcher('ORIGIN', raw_object)
        origin = re.sub(r'[\d\s]', '', origin) ##### we remove all numbers and white symbols 
        
        #### validate if obtain length is equal to source length:
        if len(origin) != int(length):
            print(origin)
            raise ValueError(f'Length of sequence {len(origin)} does not match length of reference data {length}')
        
        
        ### Append result to dict (all strings) 
        result = dict(
            locus = locus,
            gi = gi,
            definition = definition,
            organism = organism,
            origin = origin,
        )
        object.append(result)
    
    return object




def gp_to_fasta(input_paths: list, out: Path | str, flags: dict) -> None:
    # params 
    ## paths
    out_path = Path(out)
    ### check if out is dir (-> *.gp) or file path (-> file_name.fasta)
    is_out_dir = out_path.is_dir() or not out_path.suffix
    ### make right dir
    if is_out_dir:
        out_path.mkdir(parents=True, exist_ok=True)
    else:
        out_path.parent.mkdir(parents=True, exist_ok=True)
    
    # collect all .gp files 
    gp_files_list = []
    for ipath in input_paths:
        ipath_str = str(ipath)
        
        if '*' in ipath_str or '?' in ipath_str:
            matched = [Path(p) for p in glob.glob(ipath_str) if Path(p).suffix == '.gp']
            gp_files_list.extend(matched)
            continue
            
        p = Path(ipath)
        ## obtain file
        if p.is_file() and p.suffix == '.gp':
            gp_files_list.append(p)
        ## obtain folder
        elif p.is_dir():
            gp_files_list.extend(list(p.glob('*.gp')))
        else:
            print(f"[CLI: gp to fasta]: Warning - '{p}' does not exist or is not a .gp file")
    
    ## remove duplicates
    gp_files_list = list(set(gp_files_list))

    ## case: not gp files
    if not gp_files_list:
        print("[CLI: gp to fasta]: No .gp files found to process. Exiting.")
        return
    ## summary
    print(f"[CLI: gp to fasta]: Found {len(gp_files_list)} gp files to process.")

    # process files
    if is_out_dir:
        print(f"[CLI: gp to fasta]: Mode - Multiple files (Directory: '{out_path}')")
        for gp_file in gp_files_list:
            file_results = gp_file_parser(gp_file)
            current_out_path = out_path / f"{gp_file.stem}.fasta"
            
            print(f"[CLI: gp to fasta]: converting '{gp_file.name}' -> '{current_out_path.name}' ...")
            with open(current_out_path, 'w', encoding='utf-8') as file:
                for obj in file_results:
                    file.write('>' + add_prefix(obj, flags) + '\n')
                    file.write(obj['origin'].upper() + '\n\n')
    else:
        print(f"[CLI: gp to fasta]: Mode - Single aggregated file (File: '{out_path}')")
        with open(out_path, 'w', encoding='utf-8') as file:
            for gp_file in gp_files_list:
                file_results = gp_file_parser(gp_file)
                print(f"[CLI: gp to fasta]: appending '{gp_file.name}' to '{out_path.name}' ...")
                
                for obj in file_results:
                    file.write('> ' + add_prefix(obj, flags) + '\n')
                    file.write(obj['origin'].upper() + '\n\n')
                    
    print("[CLI: gp to fasta]: processed successfully")


# ------------------------
# parser 
# ------------------------

def main():
    '''
    argparser for CLI of go_to_fasta
    '''
    parser = argparse.ArgumentParser(description="Convert .gp (GenBank) files to .fasta format.")

    # obtain args
    ## obtain paths
    parser.add_argument("paths", nargs='+', help="Input .gp files, folders or wildcards (e.g. *.gp). The LAST path is the output .fasta file.")
    

    ##  Flags (optional)
    parser.add_argument("--org_style", choices=['full', 'abbreviate', 'short'], default='abbreviate',
                        help="Style of the organism name (default: abbreviate)")
    parser.add_argument("--id", choices=['locus', 'gi', 'none'], default='locus',
                        help="Which ID to include in the header (default: locus)")
    parser.add_argument("--separator", default='-', help="Separator for header parts (default: '-')")
    parser.add_argument("--no_genename", action="store_false", dest="genename",
                        help="Do not include the definition/genename in the header")

    # unpack args
    args = parser.parse_args()
    ## sanity check
    if len(args.paths) < 2:
        parser.error("You must provide at least one input path and one output path.")
    ## split paths (last value)
    output_path = args.paths[-1]
    input_paths = args.paths[:-1]

    ## packing flags to dict
    flags = {
        'org_style': args.org_style,
        'genename': args.genename,
        'id': args.id,
        'separator': args.separator
    }

    gp_to_fasta(input_paths, output_path, flags)

    

if __name__ == '__main__':
    # OLD - left for eventually debugging
    # path_for_multiple = Path('data') / 'before_conversion'
    # path_for_single = Path('data') / 'before_conversion' / 'sequence.gp'
    # path_for_fasta = Path('data') / 'after_conversion' / 'sequences.fasta'
    # flags = {
    #     'org_style': 'full',  # 'full' | 'abbreviate' | 'short'
    #     'genename': False,
    #     'id': 'locus',       # to add locus (what is GI id ?? )
    #     'separator': '-',        # separator
    # }
    # gp_to_fasta(path_for_multiple, path_for_fasta, flags)
    main()