#!/bin/bash

function enqueue_job()
{
    name=$1
    script=$2
    OMP_NUM_THREADS=4 /home/experimentos/HERRAMIENTAS/bin/qsub-wrapper.sh -N $name -l nodes=1:ppn=4:CPD -- $script | tail -n 1
}
 
function enqueue_conditioned_job()
{
    name=$1
    dependencies=$2
    script=$3
    OMP_NUM_THREADS=4 /home/experimentos/HERRAMIENTAS/bin/qsub-wrapper.sh -N $name -l nodes=1:ppn=4:CPD -W depend=afterok:$dependencies -- $script | tail -n 1
}

bfplos_dogs_id=$(enqueue_job "BFPLOS_DOGS" "./steps/01_bfplos_preprocessing_dogs.sh")
bfplos_patients_id=$(enqueue_job "BFPLOS_PATIENTS" "./steps/02_bfplos_preprocessing_patients.sh")
enqueue_job "COMPRESS_DOGS" "./steps/03_compress_preprocessing_dogs.sh"
enqueue_job "COMPRESS_PATIENTS" "./steps/04_compress_preprocessing_patients.sh"
enqueue_conditioned_job "BFPLOS_PCA" "$bfplos_dogs_id:$bfplos_patients_id" "./steps/05_do_bfplos_pca.sh"
enqueue_conditioned_job "BFPLOS_ICA" "$bfplos_dogs_id:$bfplos_patients_id" "./steps/06_do_bfplos_ica.sh"
enqueue_job "CORW" "./steps/07_do_corw.sh"
enqueue_job "CORG" "./steps/08_do_corg.sh"
enqueue_job "COVARRED" "./steps/09_do_covarred.sh"
