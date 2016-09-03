#!/bin/bash
Rscript scripts/PREPROCESS/compute_ica.R &&
python scripts/PREPROCESS/apply_ica.py
