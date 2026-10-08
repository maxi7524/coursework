# Input data

```bash
python download_data.py --list
python download_data.py
```

Run the script by path from any directory. Outputs are relative to this assignment and ignored by Git. Matching checksums are reused; failed downloads preserve existing files.

| Input | Availability |
|---|---|
| `econometrics-project/abalone_data_set.csv` | pinned-original-repository-and-local-archive |
| `econometrics-project/abalone_data_set.xlsx` | pinned-original-repository-and-local-archive |
| `econometrics-project/sex_f/F_test_before_reduction.csv` | pinned-original-repository-and-local-archive |
| `econometrics-project/sex_f/vifs_after_F_test.csv` | pinned-original-repository-and-local-archive |
| `econometrics-project/sex_f/vifs_basic_model.csv` | pinned-original-repository-and-local-archive |
| `econometrics-project/sex_i/F_test_before_reduction.csv` | pinned-original-repository-and-local-archive |
| `econometrics-project/sex_i/vifs_after_F_test.csv` | pinned-original-repository-and-local-archive |
| `econometrics-project/sex_i/vifs_basic_model.csv` | pinned-original-repository-and-local-archive |
| `econometrics-project/sex_m/F_test_before_reduction.csv` | pinned-original-repository-and-local-archive |
| `econometrics-project/sex_m/vifs_after_F_test.csv` | pinned-original-repository-and-local-archive |
| `econometrics-project/sex_m/vifs_basic_model.csv` | pinned-original-repository-and-local-archive |
| `assignment-02/dab.csv` | pinned-original-repository-and-local-archive |
| `assignment-05/Cell_output_6_[DW].csv` | pinned-original-repository-and-local-archive |
| `data/uci-1.pkl` | `uci` provider; use the original course environment |

## Exact archived inputs

```bash
python download_data.py --archive-root /path/to/github-organization/migration-archive
```

Keep this local archive when deleting original repositories. The GitHub fallback uses authenticated `gh` and stops working after source deletion. Add `--include-artifacts` to restore historical models, reports and figures. Providers use existing course dependencies (`torchvision` or `ucimlrepo`); they do not install or upgrade packages. UCI providers cache the original dataset object as pickle; notebooks retain their original fetch/preprocessing cells. Only load trusted local pickle files.

Independent URLs without a checksum are not certified as reproducing historical bytes. Google Drive or other hosts may require access or interactive confirmation; HTML responses are rejected. Full notebook execution and scientific modernization are a later stage.
