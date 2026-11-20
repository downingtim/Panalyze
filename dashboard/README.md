# Panalyze Interactive Dashboard

A [Streamlit](https://streamlit.io) app for exploring the outputs of a Panalyze
Pangenome Variation Graph (PVG) run in the browser.

The dashboard has six tabs:

| Tab | Shows |
|-----|-------|
| Pangenome Growth | Interactive Heaps' law curve, Panacus openness plot, Pangrowth/core genome plot |
| Graph Structure | GFA and ODGI statistics, download buttons for the VG and ODGI viz2 images |
| Variants & Mutations | Mutation density histogram from the VCF, presence/absence variants (PAVs), allele frequency spectrum |
| Phylogeny & Communities | RAxML tree image, communities network |
| Annotations & Metadata | Node-to-feature annotation table, sample metadata table |
| Raw Data Preview | Quick view of selected raw text outputs |

## Prerequisites

- Python 3.9 or newer
- A finished Panalyze run with a `results/` directory

## Installation

From the repository root:

```bash
python3 -m venv .venv-dashboard
source .venv-dashboard/bin/activate
pip install -r dashboard/requirements.txt
```

This installs `streamlit`, `plotly` and `pandas`.

## Running the dashboard

```bash
cd dashboard
streamlit run app.py
```

Streamlit prints a local URL, normally <http://localhost:8501>. Open it in a browser.

The sidebar field **Path to Panalyze 'results' folder** defaults to `../results`.
That is correct when you launch from the `dashboard/` directory of a repository
that holds the run outputs. For results stored elsewhere, type an absolute path
into the sidebar, for example `/data/runs/lsdv/results`.

To use a different port:

```bash
streamlit run app.py --server.port 8502
```

### Running on a remote server or HPC node

Start the app headless on the remote machine:

```bash
streamlit run app.py --server.headless true --server.port 8501
```

Then forward the port from your own computer and open <http://localhost:8501>:

```bash
ssh -L 8501:localhost:8501 user@remote-host
```

Alternatively, bind to all interfaces with `--server.address 0.0.0.0` if the
port is reachable on your network. Only do this on a trusted network, because
the app has no authentication.

## Expected input files

All paths are relative to the `results/` folder. Any file that is missing is
reported with an information message, so a partial run still loads.

| Tab | File(s) read |
|-----|--------------|
| Pangenome Growth | `heaps/heaps.txt`, `panacus/histgrowth.node.pdf`, `pangrowth/pangrowth.pdf` |
| Graph Structure | `gfastat/gfa.stats.txt`, `odgi/odgi.stats.txt`, `vg/out.vg.png`, `viz2/out.viz.png` |
| Variants & Mutations | `vcf/gfavariants.vcf`, `pavs/out.flatten.pavs.pdf`, `vcf/frequency_distribution.png` (falls back to `vcf/afs_counts.txt`) |
| Phylogeny & Communities | `tree/tree.png`, `communities/communities.pdf` |
| Annotations & Metadata | `annotation/node_to_feature.tsv` (falls back to `bandage/PVG_annotation.csv`), `download/metadata.tsv` |
| Raw Data Preview | `heaps/heaps.txt`, `pvg/sample_paths.txt`, `gfastat/genome.lengths.txt` |

## Troubleshooting

- **"Directory not found" in the sidebar.** The results path is wrong relative
  to where `streamlit run` was launched. Use an absolute path.
- **PDF panels are blank.** PDFs are embedded as base64 data URIs, which some
  browsers, notably Chrome, block. Try Firefox, or open the PDF from the
  `results/` folder directly.
- **The Variants tab is slow.** The whole VCF is parsed on each page load, so
  very large VCFs take a while.
- **`streamlit: command not found`.** Activate the virtual environment, or run
  `python -m streamlit run app.py`.
