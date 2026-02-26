
# ogólny motyw

## na każdym pliku wywołujemy skracanie

## spisujemy całość w jeden duży plik, bazująć na parametrach jakie dostaejmy będziemy zbierać różne fragmenty

# -----------------
# Code 
# -----------------

import os 
import re 
from pathlib import Path

# helpers

## Pattern finder 
def gp_matcher(index_name: str, raw_object) -> str:
    # TODO - check pattern - it changes from raw string 
    pattern = index_name + r'\s+(.*?)(?=\n^[A-Z]|\Z)'
    definition_match = re.search(pattern, raw_object, re.MULTILINE | re.DOTALL)
    definition = definition_match.group(1) if definition_match else 'Empty'
    return definition

## Parser - function for 
def gp_file_parser(file_path: Path | str) -> list:
    ### Params 
    file_path = Path(file_path)    

    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
        ### retract all proteins 
        raw_objects = content.split('//')
    
    object = []
    for raw_object in raw_objects:
        ### skipping empty record e
        if not raw_object.strip():
            continue
        ### Take information from one protein
        #### DEFINITION: (for Genename flag)
        definition = gp_matcher('DEFINITION', raw_object)
        #### SOURCE - ORGANISM: (for Additional flag)
        source = gp_matcher('SOURCE', raw_object)
        organism = gp_matcher('ORGANISM', source)
        #### REFERENCE (for sequence length validation)

        #### ORIGIN:

        ### Append result to dict 
        result = dict(
            definition = definition,
            source = source,
            organism = organism,
        )
    print(result)



# zbieramy wszystkie pliki w formacie .gp

# spisanie każdego pliki 

## wybieramy określone fragmenty z pliku które nas interesują 

### DEFINITION

### REFERENCE: do walidacji

### DEFINITION: flaga do Genename 


# nowy plik

## parametry które podaje muszą po prostu brać te informacje z pliku i zapisywać w odpowiednim formacie 

## mamy tutaj parametry jak każdy plik po kolei powinien zosstać obsłużony i dla każdego pliku organizmu z naszej listy, musimy zaaplikować te same ustawienia 

if __name__ == '__main__':
    path_for_multiple = Path('data') / 'before_conversion' / 'sequence (1).gp'
    path_for_single = Path('data') / 'before_conversion' / 'sequence.gp'
    gp_file_parser(path_for_multiple)