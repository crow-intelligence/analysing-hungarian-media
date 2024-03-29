cimport cython
cimport numpy as np

import math

import numpy
from scipy.sparse import csc_matrix


@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
def count_skipgrams(skipfreqs, wordfreqs, vocabulary, shift):
    cdef np.float32_t skip_total = skipfreqs.total()
    cdef np.float32_t word_total = wordfreqs.total()
    cdef np.float32_t alpha = 0.75

    cdef np.int32_t n = wordfreqs.cardinality()
    cdef np.int32_t m = skipfreqs.cardinality()

    cdef np.ndarray[np.float32_t, ndim=1] data = numpy.zeros(m, dtype=numpy.float32)
    cdef np.ndarray[np.int32_t, ndim=1] row = numpy.zeros(m, dtype=numpy.int32)
    cdef np.ndarray[np.int32_t, ndim=1] col = numpy.zeros(m, dtype=numpy.int32)
    i = 0
    for k, v in skipfreqs.items():
        k = k.split('#')
        a = k[0]
        b = k[1]
        pa = wordfreqs[a] / word_total
        # context distribution smoothing
        pb = (wordfreqs[b] / word_total) ** alpha
        pab = v / skip_total
        denominator = pa * pb
        if denominator > 0:
            pmi = math.log(pab / denominator)
            # shifted pmi
            sppmi = max(pmi - math.log(shift), 0.0)
            if sppmi > 0.0: # add only positive pmi values
                data[i] = sppmi
                row[i] = vocabulary.index(a)
                col[i] = vocabulary.index(b)
                i += 1
    M = csc_matrix((data, (row, col)), shape=(n, n))
    return M
