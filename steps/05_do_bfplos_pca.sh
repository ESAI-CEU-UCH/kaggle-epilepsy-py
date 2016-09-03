#!/bin/bash
Rscript scripts/PREPROCESS/compute_pca.R &&
python scripts/PREPROCESS/apply_pca.py
