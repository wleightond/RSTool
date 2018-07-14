# William Leighton Dawson
# Center for Cyber Security
# New York University - Abu Dhabi
# Implementation of the NIST Randomness Test Suite
# 12. Approximate Entropy Test

from helpers import bin_strings
from cephes import igam as igamc
from math import log
from sys import stderr

def ApproximateEntropy(e):
    m = 3  # not fixed, but should be small and >=2
    ce = list(e)
    n = len(ce)
    ce += list(e)[:m]
    C = {}
    bs = bin_strings(m)

    def rc(i):
        if C[i]:
            return C[i] * log(C[i])
        else:
            return 0

    for idx in bs:
        C[idx] = 0
    for i in xrange(n):
        curpat = tuple(ce[i:i + m])
        C[curpat] += 1.0 / n
    phi_m = sum(map(rc, bs))

    C = {}
    bs = bin_strings(m + 1)
    for idx in bs:
        C[idx] = 0
    for i in xrange(n):
        curpat = tuple(ce[i:i + m + 1])
        C[curpat] += 1.0 / n
    phi_m_1 = sum(map(rc, bs))

    ApEn = phi_m - phi_m_1
    chi2_obs = 2 * n * (log(2) - ApEn)
    p = 1 - igamc(pow(2, m - 1), chi2_obs / 2.0)
    outstr = 'Approximate Entropy Test:\n'
    outstr += 'n = %d\n' % n
    outstr += 'm = %d\n' % m
    outstr += 'ApEn = %.6f\n' % ApEn
    outstr += 'chi2_obs = %.6f\n' % chi2_obs
    outstr += 'P-value = %.6f\n' % p
    open("./test_results/ApproximateEntropy.txt", "w").write(outstr)

    if p < 0.01:
        return False
    else:
        return True
