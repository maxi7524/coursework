import argparse
import ast
import os 
import pandas as pd

def generate_markdown(species_list, kingdoms_list, sample_size, plots_dir, tables_dir):
    """Generates the Markdown content for the final report."""
    
    # Format the lists for text presentation
    species_str = ", ".join([s.replace("_", " ") for s in species_list])
    kingdoms_str = ", ".join(kingdoms_list)

    theoretical_introduction = f"""---
title: "Protein Analysis Report"
format:
  html:
    embed-resources: true   
    resources:
      - "{plots_dir}/pdb_trends_interactive.html"
    toc: true
    theme: cosmo
  pdf:
    toc: true
    geometry: "margin=2cm"
---

# Bioinformatics Analysis Report: Protein Structural and Compositional Trends

## Theoretical Introduction

The analysis of protein data provides crucial insights into both the evolution of biological mechanisms and the advancement of structural biology techniques. This report investigates two main areas: the historical progression of structure determination methods and the statistical composition of proteins across different organisms.

Historically, X-ray crystallography has dominated the Protein Data Bank (PDB). However, X-ray crystallography requires a challenging, time-consuming, and highly expensive protein crystallization process. In contrast, recent technological leaps in detector technology and computational processing have caused a "Resolution Revolution" in Cryo-Electron Microscopy (Cryo-EM)[cite: 1]. Cryo-EM allows for the study of large macromolecular complexes in their native, aqueous state without the need for crystals, fundamentally shifting how structures are solved and drastically reducing historical bottlenecks.

Biologically, the primary structure of a protein dictates more than just its fold; it governs its cellular lifespan. According to the **N-end rule**, the *in vivo* half-life of a protein is heavily influenced by its N-terminal amino acid residue[cite: 2]. Destabilizing N-terminal residues trigger rapid ubiquitin-dependent (in eukaryotes) or distinct proteolytic degradation (in bacteria). Consequently, statistical analysis of N-termini and overall amino acid content across diverse species ({species_str}) and broad taxonomic kingdoms ({kingdoms_str}) can reveal evolutionary pressures and distinct metabolic strategies employed by different organisms.

***
"""

    methodology = f"""## Methodology

### Structural Database Trends Analysis (PDB)
Metadata was acquired directly from the PDB (`entries.idx` and `pdb_seqres.txt`). By filtering specifically for protein entries and weighting the data using the formula $\sum(n \cdot 1/r)$ (where $n$ is the sequence length, and $r$ is resolution). This solution took into consideration not only length but also quality of data.

### Protein Length and Composition Analysis
Sequences for targeted species ({species_str}) and randomly sampled sequences from kingdoms ({sample_size} sequences each) were retrieved from the UniProtKB REST API. Random sampling of kingdoms partially prevents database bias from skewing the macroscopic view. To estimate the standard error of mean protein lengths and amino acid frequencies, statistical bootstrapping (95% confidence interval) was employed.

***

## Results and Analysis
"""

    trends_analysis = f"""

### Structural Database Trends Analysis (PDB)

::: {{.content-visible when-format="html"}}
#### Animated Trends (GIFs)

The following charts illustrate the historical dominance and recent shifts in techniques used to determine protein structures deposited in the PDB.

![PDB Techniques Over Time]({plots_dir}/pdb_trends_absolute.gif)
*Figure 0.1: Animated progression of accumulated structures by method over time.*

![PDB Techniques Over Time]({plots_dir}/pdb_trends_percentage.gif)
*Figure 0.2: Animated progression of structures percentage by method over time.*
:::

#### Structural Analysis, Interactive Data

::: {{.content-visible when-format="html"}}
Below is the interactive structural growth timeline (2005-2025). You can use the slider to change the year.

<object data="{plots_dir}/pdb_trends_interactive.html" width="100%" height="500px">
    <embed src="{plots_dir}/pdb_trends_interactive.html" width="100%" height="500px"> </embed>
    Error: Embedded content could not be displayed.
</object>
:::

::: {{.content-visible when-format="pdf"}}
*Note: The interactive structural growth timeline (2005-2025) is available in the HTML version of this report.*
:::

![PDB Techniques Pie Chart]({plots_dir}/pdb_pie_chart.png)
*Figure 1: Overall distribution of structural determination methods in the PDB.*

We can observe that in recent years *electron microscopy* became more popular. That is because it provides general method for investigating proteins with high resolution. It also does not incorporate protein crystallization which is hardest part in X ray crystallography. 

"""


    N_terminus_analysis = f"""### Protein Length and Composition Analysis

Based on the parsed UniProt FASTA files, we analyzed the frequency of specific amino acids at the N-terminus, as well as the overall sequence length distributions.

#### Length comparison between groups

![Length Comparison Species]({plots_dir}/length_comparison_species.png)
*Figure 2: Distribution of protein lengths across selected species grouped by taxonomy.*

![Length Comparison Kingdoms]({plots_dir}/length_comparison_kingdoms.png)
*Figure 3: Distribution of protein lengths across kingdoms.*

![AA Content Species]({plots_dir}/aa_content_E_coli_Human_Yeast.png)
*Figure 4: Percentage content of amino acids across E.coli, Human, and Yeast.*

![AA Content Kingdoms]({plots_dir}/aa_content_kingdoms.png)
*Figure 5: Average amino acid content across taxonomic kingdoms.*


***
"""


    N_terminus_analysis += "\n#### Protein Length Histograms\n"
    for s in species_list:
        N_terminus_analysis += f"![Hist {s}]({plots_dir}/histograms/hist_{s}.png)\n"

    N_terminus_analysis += "\n#### Statistical Tables\n"
    table_files = {
        "Species - Length Statistics": f"{tables_dir}/species_stats.csv",
        "Species - Amino Acid Content (with StdErr)": f"{tables_dir}/aa_species_stats.csv",
        "Kingdom - Length Statistics": f"{tables_dir}/kingdom_stats.csv",
        "Kingdom - Amino Acid Content (with StdErr)": f"{tables_dir}/aa_kingdoms_stats.csv"
    }

    for title, path in table_files.items():
        if os.path.exists(path):
            df = pd.read_csv(path)
            N_terminus_analysis += f"##### {title}\n\n{df.to_markdown(index=False)}\n\n"

    N_terminus_analysis += """

We can observe that length of proteins differ significantly between kingdoms and model organisms. We also can observe that There is significant difference between kinndoms and our model organism (couple percentages changes acidicity drastically). 

> Remark: I use word significant because our probe is big enough to obtain high p-value through wilcoxons tests. 


"""

    databases_comparison_analysis = f"""\n#### Comparison between data bases

##### Length Distribution Comparison
![Length Comparison PDB vs UniProt]({plots_dir}/length_comparison_pdb_vs_uniprot.png)
*Figure 6: Length distribution comparison between PDB structures and UniProt sequences (log scale).*

##### Amino Acid Composition Comparison
![AA Content PDB vs UniProt]({plots_dir}/aa_content_pdb_vs_uniprot.png)
*Figure 7: Average amino acid content comparison between PDB and UniProt.*

##### Detailed Comparison Table
"""



    path_comp = f"{tables_dir}/comparison_pdb_uniprot.csv"
    if os.path.exists(path_comp):
        df_comp = pd.read_csv(path_comp)
        databases_comparison_analysis += f"\n{df_comp.to_markdown(index=False)}\n\n"

    path_aa_comp = f"{tables_dir}/aa_pdb_vs_uniprot.csv" 
    if os.path.exists(path_aa_comp):
        databases_comparison_analysis += "##### AA Composition Stats (PDB vs UniProt)\n"
        df_aa_comp = pd.read_csv(path_aa_comp)
        databases_comparison_analysis += f"\n{df_aa_comp.to_markdown(index=False)}\n"

    databases_comparison_analysis += f"\nWe can observe huge difference between PDB (287 AA) and UniProt (391 AA) databases. That is because PDB, contains only experimentally determinted structures which overrepresented shorter structures. For this process proteins needed to be crystalized for X-ray difffraction, which is problematic with longer proteins. UniProt contains also predicted proteins which are longer."


    bibliography = """\n## Bibliography

1. Kühlbrandt, W. (2014). The Resolution Revolution. *Science*, 343(6178), 1443-1444.
2. Varshavsky, A. (2011). The N-end rule pathway and regulation by proteolysis. *Protein Science*, 20(8), 1298-1345.

"""



    return theoretical_introduction + methodology + trends_analysis + N_terminus_analysis + databases_comparison_analysis + bibliography 

def main():
    parser = argparse.ArgumentParser(description="Generate Markdown Report")
    parser.add_argument("--output", required=True)
    parser.add_argument("--species", required=True)
    parser.add_argument("--kingdoms", required=True)
    parser.add_argument("--sample_size", required=True)
    parser.add_argument("--plots_dir", required=True)
    parser.add_argument("--tables_dir", required=True)
    
    args = parser.parse_args()

    # create evaluation function (we parse both formats, in list [...] and in)
    def parse_list(input_str):
        if '[' in input_str: # list format ['a', 'b']
            try:
                return ast.literal_eval(input_str)
            except:
                pass
        # be default we split value by spaces (as should be given) 
        return input_str.replace(',', ' ').split() 
    # Safely evaluate the string representation of lists passed from Snakemake
    try:
        species_list = parse_list(args.species)
    except ValueError:
        species_list = args.species.split(",") # Fallback if passed as comma-separated

    try:
        kingdoms_list = parse_list(args.kingdoms)
    except ValueError:
        kingdoms_list = args.kingdoms.split(",")

    markdown_text = generate_markdown(
        species_list, 
        kingdoms_list, 
        args.sample_size, 
        args.plots_dir, 
        args.tables_dir
    )

    with open(args.output, "w", encoding="utf-8") as f:
        f.write(markdown_text)
    
    print(f"Successfully generated report at: {args.output}")

if __name__ == "__main__":
    main()