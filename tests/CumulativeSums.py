# William Leighton Dawson
# Center for Cyber Security
# New York University - Abu Dhabi
# Implementation of the NIST Randomness Test Suite
# 13. Cumulative Sums (Cusum) Test

from helpers import LengthError
from ncephes.cprob import ndtr as Phi
from math import sqrt
from sys import stderr

FORWARD, BACKWARD = 0, 1


def CumulativeSums(e):
    ce = list(e)
    n = len(ce)
    run_test = True
    retval = True
    outstr = "Cumulative Sums (Cusum) Test:\n"
    outstr += 'n = %d\n' % n
    if n < 100:
        run_test = False
    else:
        X = map(lambda i: 2 * i - 1, ce)
        z_v = [0, 0]
        p_v = [0, 0]
        for mode in [FORWARD, BACKWARD]:
            cursum = 0
            for bit in X[::1 - 2 * mode]:
                cursum += bit
                if abs(cursum) > z_v[mode]:
                    z_v[mode] = abs(cursum)
            z = z_v[mode]
            term1 = 1
            term2 = 0
            term3 = 0
            for k in xrange((-n / z + 1) / 4, (n / z - 1) / 4):
                term2a = Phi((4 * k + 1) * z / sqrt(n))
                term2b = Phi((4 * k - 1) * z / sqrt(n))
                term2 += term2a - term2b
            for k in xrange((-n / z - 3) / 4, (n / z - 1) / 4):
                term3a = Phi((4 * k + 3) * z / sqrt(n))
                term3b = Phi((4 * k + 1) * z / sqrt(n))
                term3 += term3a - term3b
            p_v[mode] = term1 - term2 + term3  # NB only accurate for n >= 100
            p = p_v[mode]
            if p < 0.01:
                retval = False
        outstr += 'mode = 0 (forward) || mode = 1 (reverse)\n'
        outstr += 'z = %.6f (forward) || z = %.6f (reverse)\n' % (z_v[FORWARD], z_v[BACKWARD])
        outstr += 'p = %.6f (forward) || p = %.6f (reverse)\n' % (p_v[FORWARD], p_v[BACKWARD])
    if not run_test:
        outstr += 'Test not run: pre-test condition not met: '
        outstr += 'n >= 100\n'
    open("./test_results/CumulativeSums.txt", "w").write(outstr)
    return retval
