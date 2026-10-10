# Protein Analysis Pipeline: Structural & Compositional Trends

A fully automated bioinformatics pipeline for analyzing protein data from PDB and UniProt databases. The project handles data retrieval, statistical processing, and generates comprehensive reports in HTML and PDF formats.

## Project Objectives
* **Methodological Trends:** Tracking the evolution of structure determination techniques (X-ray vs. Cryo-EM).
* **Amino Acid Composition:** Comparing AA distributions across different kingdoms and databases.
* **Length Distribution:** Analyzing the bias between experimental (PDB) and genomic (UniProt) protein lengths.
* **N-terminus Analysis:** Verifying protein sequence completeness based on the N-end rule.

## Reproducing Results

### Running the Pipeline (Snakemake)
To execute the entire workflow (downloading data, analysis, plotting, and reporting), run the following command from the project root:

```bash
snakemake --snakefile create_report.smk --cores all
```

if you want change settings you need only to edit `config.yaml` file.

### Manual Report Rendering (Quarto)

If the analysis results already exist in the results/ directory, you can render the reports manually:

```bash
quarto render report.md --to html
quarto render report.md --to pdf
```

***

## Project Structure

* `create_report.smk`: Main Snakemake workflow file defining the pipeline rules.
* `config.yaml`: Configuration file (URLs, species list, taxonomy mappings).
* `scripts/`:
  * `downloads/`: Scripts for fetching data from PDB and UniProt.
  * `analysis/`: Computational logic (protein stats, trend analysis, N-terminus).
  * `report/`: Script for generating the Markdown report file.
* `results/`:
  * `plots/`: PNG charts, GIF animations, and interactive Plotly (HTML) plots.
  * `tables/`: Processed statistical data in CSV format.
* `report.pdf` / report.html: Final generated reports containing methodology, results, and conclusions.


## Author

Max Stróżyk

## License

# License

MIT License

Copyright (c) 2026 Max Stróżyk

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
