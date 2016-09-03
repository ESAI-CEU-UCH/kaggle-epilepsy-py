#!/bin/bash

function enqueue_job()
{
    OMP_NUM_THREADS=4 /home/experimentos/HERRAMIENTAS/bin/qsub-wrapper.sh -l nodes=1:ppn=4:CPD -- $1 | tail -n 1
}
 
function enqueue_conditioned_job()
{
    OMP_NUM_THREADS=4 /home/experimentos/HERRAMIENTAS/bin/qsub-wrapper.sh -l nodes=1:ppn=4:CPD -W depend=afterok:$1 -- $2 | tail -n 1
}

bfplos_dogs_id=$(enqueue_job "./steps/01_bfplos_preprocessing_dogs.sh")
bfplos_patients_id=$(enqueue_job "./steps/02_bfplos_preprocessing_patients.sh")
enqueue_job "./steps/03_compress_preprocessing_dogs.sh"
enqueue_job "./steps/04_compress_preprocessing_patients.sh"
enqueue_conditioned_job "$bfplos_dogs_id:$bfplos_patients_id" "./steps/05_do_bfplos_pca.sh"
enqueue_conditioned_job "$bfplos_dogs_id:$bfplos_patients_id" "./steps/06_do_bfplos_ica.sh"
enqueue_job "./steps/07_do_corw.sh"
enqueue_job "./steps/08_do_corg.sh"
enqueue_job "./steps/09_do_covarred.sh"
