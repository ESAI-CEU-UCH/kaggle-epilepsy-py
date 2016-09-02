# This file is part of ESAI-CEU-UCH/kaggle-epilepsy-py (https://github.com/ESAI-CEU-UCH/kaggle-epilepsy-py)
#
# Copyright (c) 2016, ESAI, Universidad CEU Cardenal Herrera,
# (F. Zamora-Martinez, F. Mu\~noz-Malmaraz, J. Pardo)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.

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

HZ       = 400
WSIZE    = 60        # seconds
WADVANCE = 30        # seconds
FFT_SIZE = 2**14     # 16384
NUM_FB   = 6
filt     = elib.compress

# process all dogs applying FFT + FB + logarithm
all_dirs = glob(data_dir + "Dog_*/*.mat")

# run in parallel
def f(x): return elib.prep_fn(x,HZ,FFT_SIZE,WSIZE,WADVANCE,out_dir,filt)
pool = Pool(processes=4)
result = pool.map(f, all_dirs)
