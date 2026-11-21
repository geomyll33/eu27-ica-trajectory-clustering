# EU-27 digital-economy trajectory clustering (ICA index, 1995–2023)

Code and derived results for the manuscript *"Convergence, Diffusion, or Divergence? A Trajectory-Based Classification of Digital-Economy Development in the EU-27"* (Iordanis Karavasilis, Georgios Myllis, Vasiliki Vrana, Alkiviadis Tsimpiris). Status: manuscript in preparation; citation details to be added on publication.

## Contents

- `scripts/stab_b2000b.py`: reference K-Means partition (K = 4, 50 starts) and 2,000-draw Jaccard bootstrap stability (80% subsamples, seed 42).
- `scripts/stab_b2000.py`: earlier version of the stability run, kept for reproducibility.
- `scripts/consensus2000.py`: 2,000-run co-clustering (consensus) matrix and within-cluster frequencies; regenerates `figures/figures_consensus_matrix_2000.png`.
- `scripts/rd_v2.py`, `scripts/rd_official.py`: fuzzy regression-discontinuity analysis at 75% of EU-27 GDP per head (PPS), using internet-use indicators.
- `results/cs_did.py`, `results/cs_boot.py`: staggered difference-in-differences for EU accession and its bootstrap.
- `results/`: intermediate outputs (stability JSON, DiD panel and event study, external merged country table, official category check).
- `figures/`: consensus matrix figure.

## Data

The input data are included under `data/`, with sources, Eurostat dataset codes and reuse terms listed in `data/SOURCES.md`. The ICA series is derived by the authors from Eurostat national accounts. The DESI file comes from the European Commission. The Eurostat extracts are unchanged downloads.

Reuse of Eurostat and European Commission data is permitted with acknowledgement of the source. The files in `results/` are derived from these sources and follow the same requirement.

## Reproduction

```bash
pip install -r requirements.txt
python scripts/stab_b2000b.py
python scripts/consensus2000.py
python scripts/rd_v2.py
python results/cs_did.py
python results/cs_boot.py
```

Random seeds are fixed (seed = 42). Scripts write results to `results/` and figures to `figures/`.

## Use of AI assistance

Claude Haiku 5.5 (Anthropic) assisted with writing and debugging the code in this repository. All outputs were checked by the authors against the source data.

## Licence

Code: MIT (see `LICENSE`). Derived data, results and figures: CC-BY 4.0. Source data remain subject to the Eurostat and European Commission reuse policies listed in `data/SOURCES.md`.

## Citation

If you use this code, please cite the manuscript (citation to be added on publication).
