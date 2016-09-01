import ESAIEpilepsyLib as elib
from glob import glob

data_dir = "/home/experimentos/CORPORA/KAGGLE/EPILEPSY_PREDICTION/"
out_dir = "/home/pako/tmp/epilepsy/FFT_60s_30s_BFPLOS/"

elib.mkdir(out_dir)

HZ       = 400
WSIZE    = 60        # seconds
WADVANCE = 30        # seconds
FFT_SIZE = 2**14 + 1 # 16385 (FIXME: In Lua it was 16384)
NUM_FB   = 6
filt     = elib.compute_PLOS_filter(HZ, FFT_SIZE, NUM_FB)

# process all dogs applying FFT + FB + logarithm
all_dirs = glob(data_dir + "Dog_*/*.mat")

# run in parallel
for x in all_dirs:
    elib.prep_fn(x,HZ,FFT_SIZE,WSIZE,WADVANCE,out_dir,filt)
