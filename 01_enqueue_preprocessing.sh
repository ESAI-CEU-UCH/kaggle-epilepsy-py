 #!/bin/bash
/home/experimentos/HERRAMIENTAS/bin/qsub-wrapper.sh --omp=4 -- python scripts/PREPROCESS/compute_fft_60s_30s_BFPLOS_Dogs.py
/home/experimentos/HERRAMIENTAS/bin/qsub-wrapper.sh --omp=4 -- python scripts/PREPROCESS/compute_fft_60s_30s_BFPLOS_Patients.py
/home/experimentos/HERRAMIENTAS/bin/qsub-wrapper.sh --omp=4 -- python scripts/PREPROCESS/compute_fft_60s_30s_compress_Dogs.py
/home/experimentos/HERRAMIENTAS/bin/qsub-wrapper.sh --omp=4 -- python scripts/PREPROCESS/compute_fft_60s_30s_compress_Patients.py
