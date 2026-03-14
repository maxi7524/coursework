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
        db_path = os.path.join(self.args.binary_db_dir, "target_db.bca")
        
        # create reseek database
        if not os.path.exists(db_path):
            print(f"Reseek DB not found. Building it in {self.args.binary_db_dir}...")
            subprocess.run(["reseek", "-convert", self.args.target_pdb_dir, "-bca", db_path], check=True)

        out_tmp = os.path.join(self.tmp_dir, "reseek_out.tsv")
        fs_tmp = os.path.join(self.tmp_dir, "rs_workspace")
        os.makedirs(fs_tmp, exist_ok=True)

        # foldseek runs through folder files 
        cmd = [
            "reseek", 
            "-search", self.args.query_pdb_dir,
            "-db", db_path,
            "-output", out_tmp,
            "-columns", "query+target+aq+evalue",
            "-evalue", "1e-10", # we filter through tm score (10) 
            "-sensitive" 
        ]
        subprocess.run(cmd, check=True)
        
        try:
            df = pd.read_csv(out_tmp, sep='\t', names=['query', 'target', 'tmscore', 'evalue'])
            # df = df[df['tmscore'] > 0.5]
            df['query'] = df['query'].str.replace('.pdb', '', regex=False)
            df['target'] = df['target'].str.replace('.pdb', '', regex=False)
        except:
            df = pd.DataFrame(columns=['query', 'target', 'tmscore', 'evalue'])
            
        return df, total_queries

if __name__ == "__main__":
    ReseekRunner().run()