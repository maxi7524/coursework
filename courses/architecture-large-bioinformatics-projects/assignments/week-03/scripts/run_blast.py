import pandas as pd
import subprocess
from run_method_template import BaseMethodRunner

class BlastRunner(BaseMethodRunner):
    def __init__(self):
        super().__init__(method_name="blast")

    def execute_tool(self) -> pd.DataFrame:
        """
        Executes BLAST tool using subprocess and parses the output.
        Note: You will need to implement the actual subprocess calls based on your env.
        """
        print(f"Mock executing BLAST on {self.args.query_fasta}...")
        
        out_file = self.args.out_results + ".tmp"

        # calculate sequence amount in fasta
        total_queries = int(subprocess.check_output(f"grep -c '^>' {self.args.query_fasta}", shell=True).strip())

        # blastp run
        cmd = [
            "blastp",
            "-query", self.args.query_fasta,
            "-db", self.args.target_db,
            "-out", out_file,
            "-outfmt", "6", # tabular format 
            "-evalue", "1e-10", # strict evalue filter 
            "-num_threads", "2" # 
        ]
        subprocess.run(cmd, check=True)

        # load dat in format 6
        columns = ['query', 'target', 'pident', 'length', 'mismatch', 'gapopen', 'qstart', 'qend', 'sstart', 'send', 'evalue', 'bitscore']
        try:
            df = pd.read_csv(out_file, sep='\t', names=columns)
            # filtration of valueable files (blast i s doing this automatically - just in case) 
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