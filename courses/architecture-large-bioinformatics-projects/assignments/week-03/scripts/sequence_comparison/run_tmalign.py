import pandas as pd
import subprocess
import os
import glob
from run_method_template import BaseMethodRunner

class TmAlignRunner(BaseMethodRunner):
    def __init__(self):
        super().__init__(method_name="tmalign")

    def execute_tool(self):
        # get .pdb files 
        query_pdbs = glob.glob(os.path.join(self.args.query_pdb_dir, "*.pdb"))
        target_pdbs = glob.glob(os.path.join(self.args.target_pdb_dir, "*.pdb"))
        total_queries = len(query_pdbs)
        
        # count PDBs files
        print(f"Found {total_queries} query PDBs and {len(target_pdbs)} target PDBs.")
        if total_queries == 0 or len(target_pdbs) == 0:
            print("WARNING: Missing PDB files. Check your paths!")
            return pd.DataFrame(), total_queries
        
        # create datasets in txt 
        list_query = os.path.join(self.tmp_dir, "list_query.txt")
        list_target = os.path.join(self.tmp_dir, "list_target.txt")

        # we create files with base names (this bash command) 
        with open(list_query, 'w') as f:
            for p in query_pdbs: f.write(os.path.basename(p).replace('.pdb', '') + '\n')
            
        with open(list_target, 'w') as f:
            for p in target_pdbs: f.write(os.path.basename(p).replace('.pdb', '') + '\n')

        out_tmp = os.path.join(self.tmp_dir, "tmalign_out.tsv")
        
        # Run TM-align
        cmd = [
            "TMalign", 
            "-dir1", os.path.abspath(self.args.query_pdb_dir) + "/", list_query,
            "-dir2", os.path.abspath(self.args.target_pdb_dir) + "/", list_target,
            "-suffix", ".pdb", 
            "-outfmt", "2", 
            "-fast"
        ]
        
        with open(out_tmp, "w") as outfile:
            subprocess.run(cmd, stdout=outfile, check=True)
        
        try:
            # regex here for tab and spaces
            df = pd.read_csv(out_tmp, sep=r'\s+', comment='#', header=None)
            df.columns = ['query', 'target', 'TM1', 'TM2', 'RMSD', 'ID1', 'ID2', 'IDali', 'L1', 'L2', 'Lali']
            # set float type to prevent error 
            df['TM1'] = pd.to_numeric(df['TM1'], errors='coerce')
            df['TM2'] = pd.to_numeric(df['TM2'], errors='coerce')
            # df = df[(df['TM1'] > 0.5) | (df['TM2'] > 0.5)] # later in analysis
        except:
            df = pd.DataFrame(columns=['query', 'target', 'TM1', 'TM2'])
        
        # IMPORTANT: it saves so strange last row, - need to remove it because it destroy metadata
        df = df.iloc[:-1, :]
        return df, total_queries

if __name__ == "__main__":
    TmAlignRunner().run()