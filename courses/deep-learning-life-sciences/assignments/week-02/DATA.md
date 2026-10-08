# Input data

```bash
python download_data.py --list
python download_data.py
```

Run the script by path from any directory. Outputs are relative to this assignment and ignored by Git. Matching checksums are reused; failed downloads preserve existing files.

| Input | Availability |
|---|---|
| `data/MNIST/raw/t10k-images-idx3-ubyte` | pinned-original-repository-and-local-archive |
| `data/MNIST/raw/t10k-labels-idx1-ubyte` | pinned-original-repository-and-local-archive |
| `data/MNIST/raw/train-images-idx3-ubyte` | pinned-original-repository-and-local-archive |
| `data/MNIST/raw/train-labels-idx1-ubyte` | pinned-original-repository-and-local-archive |
| `data/input.pkl` | pinned-original-repository-and-local-archive |
| `data` | `mnist` provider; use the original course environment |

## Exact archived inputs

```bash
python download_data.py --archive-root /path/to/github-organization/migration-archive
```

Keep this local archive when deleting original repositories. The GitHub fallback uses authenticated `gh` and stops working after source deletion. Add `--include-artifacts` to restore historical models, reports and figures. Providers use existing course dependencies (`torchvision` or `ucimlrepo`); they do not install or upgrade packages. UCI providers cache the original dataset object as pickle; notebooks retain their original fetch/preprocessing cells. Only load trusted local pickle files.

## Unavailable inputs

- airline-passengers.csv: absent from source snapshot; inspect the original input preparation cells

The script returns a nonzero status while these inputs remain unresolved. No substitute dataset has been invented.

Independent URLs without a checksum are not certified as reproducing historical bytes. Google Drive or other hosts may require access or interactive confirmation; HTML responses are rejected. Full notebook execution and scientific modernization are a later stage.
