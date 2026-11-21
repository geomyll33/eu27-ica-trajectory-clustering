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

Source data are **not** included in this repository. Place the following files under `data/` before running:

- `data/ICA_27_members_until_2023.xlsx`: ICA index series for the 27 Member States, 1995–2023 (compiled from Eurostat).
- `data/external/`: Eurostat extracts used for the RD analysis (`nama_10r_2gdp_pps_nuts2.csv`, `isoc_r_iuse_i_nuts2.csv`, `isoc_r_broad_h_nuts2.csv`, `demo_r_d2jan_2015_2017.csv`) and the NUTS-2 GDP index file.

Sources: Eurostat (https://ec.europa.eu/eurostat) and the Digital Economy and Society Index (DESI), European Commission. Eurostat data may be reused, including commercially, provided the source is acknowledged and changes are indicated (Eurostat copyright notice). Data identified as coming from other sources may be reused for non-commercial purposes only; check the dataset page for each series. The files in `results/` contain values derived from these sources and are shared under the same acknowledgement requirement.

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

Code: MIT (see `LICENSE`). Results and figures: CC-BY 4.0. The source data remain subject to the terms of Eurostat and the European Commission.

## Citation

If you use this code, please cite the manuscript (citation to be added on publication).
