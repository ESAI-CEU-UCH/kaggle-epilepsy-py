work_dir = "/home/experimentos/KAGGLE/EPILEPSY_PREDICTION_IN_PYTHON/kaggle-epilepsy-py/"
data_dir = "/home/experimentos/CORPORA/KAGGLE/EPILEPSY_PREDICTION/"
out_dir = "/home/experimentos/KAGGLE/EPILEPSY_PREDICTION_IN_PYTHON/FFT_60s_30s_COMPRESS/"

import sys
sys.path.append(work_dir)
import ESAIEpilepsyLib as elib
from glob import glob
from multiprocessing import Pool
import os

os.chdir(work_dir)
elib.mkdir(out_dir)

HZ       = 5000
WSIZE    = 60        # seconds
WADVANCE = 30        # seconds
FFT_SIZE = 2**18     # 262144
NUM_FB   = 6
filt     = elib.compress

# process all dogs applying FFT + FB + logarithm
all_dirs = glob(data_dir + "Patient_*/*.mat")

# run in parallel
def f(x): return elib.prep_fn(x,HZ,FFT_SIZE,WSIZE,WADVANCE,out_dir,filt)
pool = Pool(processes=4)
result = pool.map(f, all_dirs)
