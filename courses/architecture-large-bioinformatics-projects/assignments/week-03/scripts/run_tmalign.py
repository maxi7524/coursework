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
        total_queries = len(query_pdbs)
        
        list_query = "list_query.txt"
        list_target = "list_target.txt"
        
        # we create files with base names (this bash command) 
        with open(list_query, 'w') as f:
            for p in query_pdbs: f.write(os.path.basename(p).replace('.pdb', '') + '\n')
            
        with open(list_target, 'w') as f:
            for p in glob.glob(os.path.join(self.args.target_pdb_dir, "*.pdb")): 
                f.write(os.path.basename(p).replace('.pdb', '') + '\n')

        out_file = self.args.out_results + ".tmp"
        
        # Run TM-align
        cmd = [
            "TMalign", 
            "-dir1", self.args.query_pdb_dir + "/",
            list_query,
            "-dir2", self.args.target_pdb_dir + "/",
            list_target,
            "-suffix", ".pdb", 
            "-outfmt", "2", # 
            "-fast" # fast mode (instruction)
        ]
        
        with open(out_file, "w") as outfile:
            subprocess.run(cmd, stdout=outfile, check=True)
        
        try:
            df = pd.read_csv(out_file, sep='\t', comment='#', header=None)
            # TODO - check version for column name
            df.columns = ['query', 'target', 'TM1', 'TM2', 'RMSD', 'ID1', 'ID2', 'IDali', 'L1', 'L2', 'Lali']
            # Filtr: TM-score > 0.5 (dla query lub target) [cite: 8]
            df = df[(df['TM1'] > 0.5) | (df['TM2'] > 0.5)]
        except:
            df = pd.DataFrame(columns=['query', 'target', 'TM1', 'TM2'])
            
        return df, total_queries

if __name__ == "__main__":
    TmAlignRunner().run()