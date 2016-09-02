import errno
import math
import numpy as np
import os
import scipy as sp
import scipy.io
import scipy.sparse

######### PREPROCESS SECTION ##########

def mkdir(path):
    """Uses os.makedirs() to be equivalent to "mkdir -p" in a console. This
    function ignores exceptions in case the directory exists.

    """
    try:
        os.makedirs(path)
    except OSError as exc:
        if not exc.errno == errno.EEXIST or not os.path.isdir(path): raise
        pass

def compress(m):
    """Apply log1p compression to each data point."""
    return np.log1p(m)
#return m:clone():clamp(1.0, (m:max())):log()

def compute_PLOS_filter(HZ, FFT_SIZE, NUM_FB):
    """Returns a filter function (receives a matrix and produces its filtered
    result.)

    """
    assert NUM_FB == 6
    BIN_WIDTH = 0.5*HZ / FFT_SIZE
    # create a bank filter matrix (sparse matrix)
    limits = (
        (  0.1,  4 ), # delta
        (  4,    8 ), # theta
        (  8,   12 ), # alpha
        ( 12,   30 ), # beta
        ( 30,   70 ), # low-gamma
        ( 70,  180 ), # high-gamma
    )
    fb = np.zeros((FFT_SIZE,NUM_FB), dtype=np.float32)
    for i in xrange(NUM_FB):
        ini = math.ceil(limits[i][0] / BIN_WIDTH)
        fin = math.floor(limits[i][1] / BIN_WIDTH) + 1
        sz  = fin - ini + 1
        fb[ini:fin,i].fill(1/sz)
    fb = sp.sparse.csc_matrix(fb)
    def filt(m):
        out = compress( m*fb )
        assert out.shape[0] == m.shape[0]
        assert out.shape[1] == NUM_FB
        return out
    return filt

def load_kaggle_epilepsy_matlab_file(filename):
    """Loads the Kaggle matlab file and returns the data matrix and the sampling
    frequency.

    """
    data = [ v for k,v in sp.io.loadmat(filename).iteritems() if k.find("segment")!=-1 ][0]
    m  = data["data"].item(0).astype(np.float32)
    hz = data["sampling_frequency"].item(0)
    return m,hz

def compute_fftwh_windows(m, wsize, wadvance):
    """Given a channel data vector, applies real FFT over it using a sliding window
    of wsize and advancing wadvance steps.

    """
    nfft = 2**int(math.ceil( math.log(wsize,2) ))
    total_segments = int(math.ceil((len(m) - wsize) / wadvance))
    hamming_window = np.hamming(wsize)
    result = np.zeros((total_segments, nfft//2 + 1))
    for k in xrange(total_segments):
        i = k*wadvance
        j = i + wsize
        m_hw_slice = np.multiply(m[i:j], hamming_window)
        z = np.fft.rfft(m_hw_slice, nfft)
        result[k] = z.real**2 + z.imag**2
    return result

def apply_fft_to_all_channels(m, hz, WSIZE, WADVANCE):
    """Receives a data matrix (with row-wise channels) and applies windowed real FFT
    to each cannel. The function returns a Python list with the FFT result for
    each channel.

    """
    wsize,wadvance = math.floor(WSIZE*hz),math.floor(WADVANCE*hz)
    fft_tbl = []
    for i in xrange(m.shape[0]):
        fft_tbl.append( compute_fftwh_windows(m[i], wsize, wadvance) )
    assert len(fft_tbl) == m.shape[0]
    return fft_tbl

def prep_fn(mat_filename, HZ, FFT_SIZE, WSIZE, WADVANCE, out_dir, filt):
    """Preprocessing function. Given a Kaggle matlab file, this function computes
    the windowed real FFT, applies the given filt function and writes the result to
    out_dir.

    In case of failure, all the related channels are deleted. If the output file
    exists all the preprocessing is skipped.

    """
    out_filename = "%s.channel_%02d.csv.gz" % ( os.path.basename(mat_filename.replace(".mat","")), 1 )
    if not os.path.exists(out_dir + out_filename):
        created_file_paths = []
        print "#",mat_filename
        try:
            m,hz = load_matlab_file(mat_filename)
            assert( abs(hz - HZ) < 1 )
            fft_tbl = apply_fft_to_all_channels(m, hz, WSIZE, WADVANCE)
            for i,x in enumerate(fft_tbl):
                out_filename = "%s.channel_%02d.csv.gz" % ( os.path.basename(mat_filename.replace(".mat","")), i+1 )
                assert fft_tbl[i].shape[1] == FFT_SIZE
                out_fb = filt( fft_tbl[i] )
                out_path = out_dir + out_filename
                np.savetxt(out_path, out_fb, delimiter=' ', fmt='%.5g')
                created_file_paths.append(out_path)
        except:
            for x in created_file_paths: os.remove(x)
            raise

######### END PREPROCESS SECTION ##########

