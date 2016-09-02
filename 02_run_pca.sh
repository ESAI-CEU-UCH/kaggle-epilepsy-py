#!/bin/bash
id=$(OMP_NUM_THREADS=4 /home/experimentos/HERRAMIENTAS/bin/qsub-wrapper.sh -l nodes=1:ppn=4:CPD -- Rscript scripts/PREPROCESS/compute_pca.R | tail -n 1)
OMP_NUM_THREADS=4 /home/experimentos/HERRAMIENTAS/bin/qsub-wrapper.sh -l nodes=1:ppn=4:CPD -W depend=afterok:$id -- python scripts/PREPROCESS/apply_pca.py
