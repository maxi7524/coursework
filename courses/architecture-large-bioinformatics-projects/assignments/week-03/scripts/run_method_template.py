import argparse
import time
import pandas as pd
import os

class BaseMethodRunner:
    """
    Base class for sequence/structure alignment methods.
    Handles argument parsing, timing, and standardized I/O.
    """
    def __init__(self, method_name):
        self.method_name = method_name
        self.args = self._parse_args()
        self.start_time = None
        self.end_time = None

    def _parse_args(self):
        parser = argparse.ArgumentParser(description=f"Wrapper for {self.method_name}")
        parser.add_argument("--query_fasta", help="Path to input FASTA file (for sequence methods)")
        parser.add_argument("--target_db", help="Path to target BLAST DB (for sequence methods)")
        parser.add_argument("--query_pdb_dir", help="Path to dir with query PDBs (for structure methods)")
        parser.add_argument("--target_pdb_dir", help="Path to dir with target PDBs (for structure methods)")
        parser.add_argument("--out_results", required=True, help="Path to save output CSV")
        parser.add_argument("--out_meta", required=True, help="Path to save metadata CSV")
        return parser.parse_args()

    def run(self):
        """Main execution flow."""
        print(f"Starting {self.method_name}...")
        
        # Ensure output directories exist
        os.makedirs(os.path.dirname(self.args.out_results), exist_ok=True)
        
        self.start_time = time.time()
        
        # This method MUST be implemented by the child class
        results_df, total_queries = self.execute_tool()
        
        self.end_time = time.time()
        
        # Calculate additional information
        unique_queries_with_hits = results_df['query'].nunique() if not results_df.empty else 0
        queries_0_hits = total_queries - unique_queries_with_hits
        
        self._save_results(results_df)
        self._save_metadata(unique_queries_with_hits, queries_0_hits, total_queries)
        print(f"Finished {self.method_name}. Hits found for {unique_queries_with_hits}/{total_queries} queries.")

    def execute_tool(self) -> pd.DataFrame:
        """
        To be overridden by specific tool wrappers (e.g., BlastRunner).
        Must return a pandas DataFrame with columns: ['query', 'target', 'score', 'evalue']
        """
        # TODO 
        raise NotImplementedError("Child classes must implement execute_tool()")

    def _save_results(self, df: pd.DataFrame):
        """Saves tool-specific results to a standard CSV format."""
        # Add a column indicating which method found this
        if not df.empty:
            df['method'] = self.method_name
        df.to_csv(self.args.out_results, index=False)

    def _save_metadata(self, hits_count: int, queries_0_hits: int, total_queries: int):
        """Calculates runtime and saves standardized metadata."""
        runtime = self.end_time - self.start_time
        meta_df = pd.DataFrame([{
            "method": self.method_name,
            "runtime_seconds": round(runtime, 2),
            "total_queries": total_queries,
            "queries_with_hits": hits_count,
            "queries_0_hits": queries_0_hits
        }])
        meta_df.to_csv(self.args.out_meta, index=False)