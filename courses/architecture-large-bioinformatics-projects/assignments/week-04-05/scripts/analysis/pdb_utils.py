import os
import pandas as pd
from datetime import datetime
from collections import defaultdict

def patch_pandas_fillna():
    """
    Patches pandas fillna to maintain compatibility with bar_chart_race 
    in newer pandas versions (2.1+).
    """
    original_df_fillna = pd.DataFrame.fillna
    original_series_fillna = pd.Series.fillna

    def universal_fillna(self, value=None, method=None, **kwargs):
        if method == 'ffill':
            return self.ffill()
        if method == 'bfill':
            return self.bfill()
        
        if isinstance(self, pd.DataFrame):
            return original_df_fillna(self, value=value, **kwargs)
        return original_series_fillna(self, value=value, **kwargs)

    pd.DataFrame.fillna = universal_fillna
    pd.Series.fillna = universal_fillna

def load_sequence_lengths(file_path):
    """
    Parses pdb_seqres.txt to extract the total length of protein chains per PDB ID.
    """
    protein_lengths = {}
    with open(file_path, 'r') as f:
        for line in f:
            if line.startswith(">") and "mol:protein" in line:
                parts = line.split()
                pdb_id = parts[0][1:5].upper()
                length_part = [p for p in parts if p.startswith("length:")][0]
                length = int(length_part.split(":")[1])
                protein_lengths[pdb_id] = protein_lengths.get(pdb_id, 0) + length
    return protein_lengths

def load_experimental_metadata(file_path, protein_ids):
    """
    Parses entries.idx for dates, resolution, and methods. 
    Applies resolution r=2.5 for NMR as per instructions.
    """
    metadata = {}
    with open(file_path, 'r') as f:
        for _ in range(2): next(f) # Skip header
        for line in f:
            parts = line.strip().split('\t')
            if len(parts) < 8: continue
                
            pdb_id = parts[0].upper()
            if pdb_id not in protein_ids: continue
                
            date_str, resolution_str, method = parts[2], parts[6], parts[7].upper()
            
            try:
                dt = datetime.strptime(date_str, "%m/%d/%y")
                year = dt.year if dt.year <= 2026 else dt.year - 100
            except ValueError: continue

            if "NMR" in method:
                r = 2.5
            else:
                try:
                    r = float(resolution_str)
                except ValueError: r = 0.0
            
            if r <= 0: continue # Avoid division by zero
                
            metadata[pdb_id] = {'year': year, 'method': method, 'r': r}
    return metadata

def process_pdb_data(data_dir):
    """
    Combines sequence and metadata to calculate the trend formula: sum(n * 1/r).
    """
    seq_path = os.path.join(data_dir, "pdb_seqres.txt")
    idx_path = os.path.join(data_dir, "entries.idx")
    
    lengths = load_sequence_lengths(seq_path)
    metadata = load_experimental_metadata(idx_path, lengths.keys())
    
    results = []
    for pdb_id, info in metadata.items():
        results.append({
            'year': info['year'],
            'method': info['method'],
            'value': lengths[pdb_id] * (1.0 / info['r'])
        })
    return pd.DataFrame(results)