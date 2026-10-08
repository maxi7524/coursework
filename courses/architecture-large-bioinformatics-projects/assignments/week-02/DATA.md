# Input data

```bash
python download_data.py --list
python download_data.py
```

Run the script by path from any directory. Outputs are relative to this assignment and ignored by Git. Matching checksums are reused; failed downloads preserve existing files.

| Input | Availability |
|---|---|
| `data/Mycgen/4ESM/Mycoplasmoides_genitalium_G37_000-019/.done` | pinned-original-repository-and-local-archive |
| `data/Mycgen/4ESM/Mycoplasmoides_genitalium_G37_020-039/.done` | pinned-original-repository-and-local-archive |
| `data/Mycgen/4ESM/Mycoplasmoides_genitalium_G37_040-059/.done` | pinned-original-repository-and-local-archive |
| `data/Mycgen/4ESM/Mycoplasmoides_genitalium_G37_060-079/.done` | pinned-original-repository-and-local-archive |
| `data/Mycgen/4ESM/Mycoplasmoides_genitalium_G37_080-099/.done` | pinned-original-repository-and-local-archive |
| `data/Mycgen/4ESM/Mycoplasmoides_genitalium_G37_100-119/.done` | pinned-original-repository-and-local-archive |
| `data/Mycgen/4ESM/Mycoplasmoides_genitalium_G37_120-139/.done` | pinned-original-repository-and-local-archive |
| `data/Mycgen/4ESM/Mycoplasmoides_genitalium_G37_140-159/.done` | pinned-original-repository-and-local-archive |
| `data/Mycgen/4ESM/Mycoplasmoides_genitalium_G37_160-179/.done` | pinned-original-repository-and-local-archive |
| `data/Mycgen/4ESM/Mycoplasmoides_genitalium_G37_180-199/.done` | pinned-original-repository-and-local-archive |
| `data/Mycgen/4ESM/Mycoplasmoides_genitalium_G37_200-219/.done` | pinned-original-repository-and-local-archive |
| `data/Mycgen/4ESM/Mycoplasmoides_genitalium_G37_220-239/.done` | pinned-original-repository-and-local-archive |
| `data/Mycgen/4ESM/Mycoplasmoides_genitalium_G37_240-259/.done` | pinned-original-repository-and-local-archive |
| `data/Mycgen/4ESM/Mycoplasmoides_genitalium_G37_260-279/.done` | pinned-original-repository-and-local-archive |
| `data/Mycgen/4ESM/Mycoplasmoides_genitalium_G37_280-299/.done` | pinned-original-repository-and-local-archive |
| `data/Mycgen/4ESM/Mycoplasmoides_genitalium_G37_300-319/.done` | pinned-original-repository-and-local-archive |
| `data/Mycgen/4ESM/Mycoplasmoides_genitalium_G37_320-339/.done` | pinned-original-repository-and-local-archive |
| `data/Mycgen/4ESM/Mycoplasmoides_genitalium_G37_340-359/.done` | pinned-original-repository-and-local-archive |
| `data/Mycgen/4ESM/Mycoplasmoides_genitalium_G37_360-379/.done` | pinned-original-repository-and-local-archive |
| `data/Mycgen/4ESM/Mycoplasmoides_genitalium_G37_380-399/.done` | pinned-original-repository-and-local-archive |
| `data/Mycgen/4ESM/Mycoplasmoides_genitalium_G37_400-419/.done` | pinned-original-repository-and-local-archive |
| `data/Mycgen/4ESM/Mycoplasmoides_genitalium_G37_420-432/.done` | pinned-original-repository-and-local-archive |
| `data/Mycgen/raw/Mycoplasmoides_genitalium_G37.gp` | pinned-original-repository-and-local-archive |
| `data/hsp23/4ESM/hsp23_000-019/.done` | pinned-original-repository-and-local-archive |
| `data/hsp23/4ESM/hsp23_020-039/.done` | pinned-original-repository-and-local-archive |
| `data/hsp23/4ESM/hsp23_040-059/.done` | pinned-original-repository-and-local-archive |
| `data/hsp23/4ESM/hsp23_060-079/.done` | pinned-original-repository-and-local-archive |
| `data/hsp23/4ESM/hsp23_080-099/.done` | pinned-original-repository-and-local-archive |
| `data/hsp23/4ESM/hsp23_100-119/.done` | pinned-original-repository-and-local-archive |
| `data/hsp23/4ESM/hsp23_120-139/.done` | pinned-original-repository-and-local-archive |
| `data/hsp23/4ESM/hsp23_140-159/.done` | pinned-original-repository-and-local-archive |
| `data/hsp23/4ESM/hsp23_160-179/.done` | pinned-original-repository-and-local-archive |
| `data/hsp23/4ESM/hsp23_180-199/.done` | pinned-original-repository-and-local-archive |
| `data/hsp23/4ESM/hsp23_200-221/.done` | pinned-original-repository-and-local-archive |
| `data/hsp23/raw/hsp23.gp` | pinned-original-repository-and-local-archive |
| `data/CP014940.1.fasta` | external-url-not-verified |

## Exact archived inputs

```bash
python download_data.py --archive-root /path/to/github-organization/migration-archive
```

Keep this local archive when deleting original repositories. The GitHub fallback uses authenticated `gh` and stops working after source deletion. Add `--include-artifacts` to restore historical models, reports and figures. Providers use existing course dependencies (`torchvision` or `ucimlrepo`); they do not install or upgrade packages. UCI providers cache the original dataset object as pickle; notebooks retain their original fetch/preprocessing cells. Only load trusted local pickle files.

Independent URLs without a checksum are not certified as reproducing historical bytes. Google Drive or other hosts may require access or interactive confirmation; HTML responses are rejected. Full notebook execution and scientific modernization are a later stage.
