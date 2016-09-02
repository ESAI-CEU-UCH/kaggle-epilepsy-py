#!/bin/bash
OMP_NUM_THREADS=4 /home/experimentos/HERRAMIENTAS/bin/qsub-wrapper.sh -l nodes=1:ppn=4:CPD -- python scripts/PREPROCESS/compute_fft_60s_30s_BFPLOS_Dogs.py
OMP_NUM_THREADS=4 /home/experimentos/HERRAMIENTAS/bin/qsub-wrapper.sh -l nodes=1:ppn=4:CPD -- python scripts/PREPROCESS/compute_fft_60s_30s_BFPLOS_Patients.py
OMP_NUM_THREADS=4 /home/experimentos/HERRAMIENTAS/bin/qsub-wrapper.sh -l nodes=1:ppn=4:CPD -- python scripts/PREPROCESS/compute_fft_60s_30s_compress_Dogs.py
OMP_NUM_THREADS=4 /home/experimentos/HERRAMIENTAS/bin/qsub-wrapper.sh -l nodes=1:ppn=4:CPD -- python scripts/PREPROCESS/compute_fft_60s_30s_compress_Patients.py
