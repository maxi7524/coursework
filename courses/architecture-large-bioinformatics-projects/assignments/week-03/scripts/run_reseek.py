import pandas as pd
import subprocess
import os
import glob
from run_method_template import BaseMethodRunner

class ReseekRunner(BaseMethodRunner):
    def __init__(self):
        super().__init__(method_name="reseek")

    def execute_tool(self):
        print(f"Mock executing Reseek on {self.args.query_fasta}...")
        total_queries = len(glob.glob(os.path.join(self.args.query_pdb_dir, "*.pdb")))
        out_file = self.args.out_results + ".tmp"
        tmp_dir = "tmp_reseek"
        
        # foldseek runs through folder files 
        cmd = [
            "reseek", 
            "-search", self.args.query_pdb_dir,
            "-db", self.args.target_pdb_dir,
            "-output", out_file,
            "-columns", "query+target+aq+evalue",
            "-evalue", "1e-10", # we filter through tm score (10) 
            "-sensitive" 
        ]
        subprocess.run(cmd, check=True)
        
        try:
            df = pd.read_csv(out_file, sep='\t', names=['query', 'target', 'tmscore', 'evalue'])
            
            # we remove .pdb from queries so convention is same as with blast 
            df['query'] = df['query'].str.replace('.pdb', '', regex=False)
            df['target'] = df['target'].str.replace('.pdb', '', regex=False)
        except:
            df = pd.DataFrame(columns=['query', 'target', 'tmscore', 'evalue'])
            
        return df, total_queries

if __name__ == "__main__":
    ReseekRunner().run()