import pandas as pd
import subprocess
import os
import glob
from run_method_template import BaseMethodRunner

class FoldseekRunner(BaseMethodRunner):
    def __init__(self):
        super().__init__(method_name="foldseek")

    def execute_tool(self):
        print(f"Mock executing Foldseek on {self.args.query_fasta}...")
        total_queries = len(glob.glob(os.path.join(self.args.query_pdb_dir, "*.pdb")))
        out_file = self.args.out_results + ".tmp"
        tmp_dir = "tmp_foldseek"
        
        # foldseek runs through folder files 
        cmd = [
            "foldseek", "easy-search",
            self.args.query_pdb_dir,
            self.args.target_pdb_dir,
            out_file,
            tmp_dir,
            "--format-output", "query,target,alntmscore,evalue",
            "-e", "1e-10" # we filter through tm score (10) 
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
    FoldseekRunner().run()