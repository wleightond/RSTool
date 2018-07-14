# William Leighton Dawson
# Center for Cyber Security
# New York University - Abu Dhabi
# Implementation of the NIST Randomness Test Suite
# 6. The Discrete Fourier Transform (Spectral) Test

from helpers import compute_dft_complex, modulus, prime_factors
from math import sqrt, erfc, log
from sys import stderr


def DiscreteFourierTransform(e):
    ce = list(e)
    n = len(ce)
    # Decrement n until its prime factors are low (to keep fft fast)
    pf = prime_factors(n, sorting=False, setting=False)
    if pf == []: pf.append(1001)
    while max(pf) > 1000 and n > 1000:
        n -= 1
        pf = prime_factors(n, sorting=False, setting=False)
        if pf == []: pf.append(1001)
    ce = ce[:n]
    disc_bits = len(e) - n
    S = compute_dft_complex(ce)
    M = modulus(S)
    T = sqrt(log(1 / 0.05) * n)
    N_0 = 0.95 * n / 2
    pre_N_1 = [(peak < T) for peak in M]
    N_1 = sum(pre_N_1)  # BUG: bigger than NIST example vals
    d = (N_1 - N_0) / sqrt(n * 0.95 * 0.05 / 4)
    p = erfc(abs(d) / sqrt(2))
    outstr = "Discrete Fourier Transform (Spectral) Test:\n"
    outstr += "n = %d (note: %d bits were discarded)\n" % (n, disc_bits)
    outstr += "T = %.6f\n" % T
    outstr += "N_1 = %d\n" % N_1
    outstr += "N_0 = %d\n" % N_0
    outstr += "d = %.6f\n" % d
    outstr += "P-value = %.6f\n" % p
    open("./test_results/DiscreteFourierTransform.txt", "w").write(outstr)
    if p < 0.01:
        return False
    else:
        return True
