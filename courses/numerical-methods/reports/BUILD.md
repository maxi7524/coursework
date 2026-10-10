# Building the bilingual reports

The exact Polish exports are under each report's original directory. Marked translations are under english; their source and asset paths use English names. Rebuilt PDFs are report-pl.pdf and report-en.pdf. submitted-pl.pdf, where available, is the byte-preserved PDF from the historical repository.

Install [Tectonic](https://github.com/tectonic-typesetting/tectonic), then run from the repository root:

    python3 scripts/build_numerical_reports.py

To select one report:

    python3 scripts/build_numerical_reports.py --report lab-04

Use --tectonic /path/to/tectonic for an executable outside PATH. Validation used Tectonic 0.17.0. The first build may download its TeX bundle; subsequent builds can reuse its cache.

The builder stages an isolated temporary copy. It uses Unicode fonts and Polish/English babel language support to preserve accented characters. It removes the legacy pdfTeX driver option and obsolete editor-synchronization packages for XeTeX compatibility. Missing report dates are rendered as the course term; explicit dates remain intact. A stray word outside the Importance Sampling slides is omitted only during compilation. The additional draft uses an undefined algorithm-list environment; the build copy supplies its missing definition without changing the pseudocode. Exact originals are not rewritten. These are presentation/build adjustments, not changes to scientific results.

English PDFs are translations of the Polish documents, not new experiments. Formulae, table values, plots and author attribution are preserved. Text inside the historical plot images can remain Polish. Original draft statements and unfinished passages are retained or marked; scientific correction and algorithm modernization are separate work.

Only authored report PDFs and fixed document illustrations are excepted from the general artifact ignore rules. External datasets, temporary build products, model files and generated experiment exports remain ignored.

Repository links in the English versions point to the organized implementation folders. The Lab 5 English title corrects the original template label Lab04; the exact Polish source/title remains preserved.
