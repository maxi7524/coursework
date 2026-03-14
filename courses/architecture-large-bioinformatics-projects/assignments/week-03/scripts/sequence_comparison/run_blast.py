import pandas as pd
import subprocess
import os 
from run_method_template import BaseMethodRunner

class BlastRunner(BaseMethodRunner):
    def __init__(self):
        super().__init__(method_name="blast")

    def execute_tool(self) -> pd.DataFrame:
        """
        Executes BLAST tool using subprocess and parses the output.
        """
        print(f"Mock executing BLAST on {self.args.query_fasta}...")
        # dataset
        ## take all sequences 
        total_queries = int(subprocess.check_output(f"grep -c '^>' {self.args.query_fasta}", shell=True).strip())
        ## path for db 
        db_prefix = os.path.join(self.args.binary_db_dir, "target_db")

        # check if database exits, else create
        if not os.path.exists(db_prefix + ".phr"):
            print(f"BLAST DB not found. Building it in {self.args.binary_db_dir}...")
            cmd_db = ["makeblastdb", "-in", self.args.target_fasta, "-dbtype", "prot", "-out", db_prefix]
            subprocess.run(cmd_db, check=True)

        # run search 
        out_tmp = os.path.join(self.tmp_dir, "blast_out.tsv")
        cmd_search = [
            "blastp",
            "-query", self.args.query_fasta,
            "-db", db_prefix,
            "-out", out_tmp,
            "-outfmt", "6",
            "-evalue", "1e-10",
            "-num_threads", "2"
        ]
        subprocess.run(cmd_search, check=True)

        # load dat in format 6
        columns = ['query', 'target', 'pident', 'length', 'mismatch', 'gapopen', 'qstart', 'qend', 'sstart', 'send', 'evalue', 'bitscore']
        try:
            df = pd.read_csv(out_tmp, sep='\t', names=columns)
            # filtration of valueable files (blast should already already done it) 
            df = df[df['evalue'] <= 1e-10]
        except pd.errors.EmptyDataError:
            df = pd.DataFrame(columns=columns)
            
        return df, total_queries
        

        # TODO - for .md testing 
        # Mock data representing tabular BLAST output
        # mock_data = {
        #     'query': ['seq1', 'seq2', 'seq3'],
        #     'target': ['targetA', 'targetB', 'targetC'],
        #     'score': [95.5, 80.0, 45.2], # Bitscore or identity
        #     'evalue': [1e-15, 1e-10, 0.5]
        # }
        # df = pd.DataFrame(mock_data)
        
        # # Filter reliable hits (e.g., evalue < 1e-10)
        # filtered_df = df[df['evalue'] <= 1e-10]
        
        return filtered_df, 3

if __name__ == "__main__":
    BlastRunner().run()