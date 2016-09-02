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

WORK_DIR      = "/home/experimentos/KAGGLE/EPILEPSY_PREDICTION_IN_PYTHON/kaggle-epilepsy-py/"
FFT_DATA_PATH = "/home/experimentos/KAGGLE/EPILEPSY_PREDICTION_IN_PYTHON/FFT_60s_30s_BFPLOS/"
PCA_DATA_PATH = "/home/experimentos/KAGGLE/EPILEPSY_PREDICTION_IN_PYTHON/FFT_60s_30s_BFPLOS/"
OUTPUT_PATH   = "/home/experimentos/KAGGLE/EPILEPSY_PREDICTION_IN_PYTHON/FFT_60s_30s_BFPLOS_PCA/"
SUBJECTS      = [ "Dog_1", "Dog_2", "Dog_3", "Dog_4", "Dog_5", "Patient_1", "Patient_2" ]
NUM_CORES     = 4

import sys
sys.path.append(WORK_DIR)
import ESAIEpilepsyLib as elib
from glob import glob
from multiprocessing import Pool
import numpy as np
import os

os.chdir(WORK_DIR)
elib.mkdir(OUTPUT_PATH)

pool = Pool(processes=4)

for subject in SUBJECTS:
    print "# " + subject
    center = np.loadtxt("%s/%s_pca_center.txt"%(PCA_DATA_PATH, subject))
    scale = 1.0/(np.loadtxt("%s/%s_pca_scale.txt"%(PCA_DATA_PATH, subject)))
    rotation = np.loadtxt("%s/%s_pca_rotation.txt"%(PCA_DATA_PATH, subject))
    center = center.squeeze()
    scale = scale.squeeze()
    def transform(x): return np.matmul(np.multiply(x - center, scale), rotation)
    files = sorted(glob("%s/%s*channel_01*"%(FFT_DATA_PATH, subject)))
    assert len(files) > 0
    def f(filename):
        mask = filename.replace("channel_01", "channel_??")
        outname = "%s/%s.csv.gz"%(OUTPUT_PATH,
                                  os.path.basename(filename).replace(".channel_01.csv.gz",""))
        if not os.path.exists(outname):
            m = np.concatenate([ np.loadtxt(x) for x in sorted(glob(mask)) ], axis=1)
            out = transform(m)
            np.savetxt(outname, out, delimiter=' ', fmt='%.5g')
        
    result = pool.map(f, files)
