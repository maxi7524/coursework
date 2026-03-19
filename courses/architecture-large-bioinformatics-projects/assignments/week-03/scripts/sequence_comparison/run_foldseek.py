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
        db_path = os.path.join(self.args.binary_db_dir, "target_db")
        
        # foldseek database
        if not os.path.exists(db_path):
            print(f"Foldseek DB not found. Building it in {self.args.binary_db_dir}...")
            subprocess.run(["foldseek", "createdb", self.args.target_pdb_dir, db_path], check=True)

        out_tmp = os.path.join(self.tmp_dir, "foldseek_out.tsv")
        fs_tmp = os.path.join(self.tmp_dir, "fs_workspace")
        os.makedirs(fs_tmp, exist_ok=True)

        # foldseek runs through folder files 
        cmd = [
            "foldseek", "easy-search",
            self.args.query_pdb_dir, db_path,
            out_tmp, fs_tmp,
            "--format-output", "query,target,alntmscore,evalue",
            "-e", "1e-10"
        ]
        subprocess.run(cmd, check=True)
        
        try:
            df = pd.read_csv(out_tmp, sep='\t', names=['query', 'target', 'tmscore', 'evalue'])
            # df = df[df['tmscore'] > 0.5]
            # we remove .pdb from queries so convention is same as with blast 
            df['query'] = df['query'].str.replace('.pdb', '', regex=False)
            df['target'] = df['target'].str.replace('.pdb', '', regex=False)
        except:
            df = pd.DataFrame(columns=['query', 'target', 'tmscore', 'evalue'])
            
        return df, total_queries

if __name__ == "__main__":
    FoldseekRunner().run()