# William Leighton Dawson
# Center for Cyber Security
# New York University - Abu Dhabi
# Implementation of the NIST Randomness Test Suite
# 11. The Serial Test

from helpers import bin_strings
from cephes import igam as igamc
from sys import stderr

def Serial(e):
    m = 2  # not fixed, but should be small and >=2
    ce = list(e)
    n = len(ce)
    ce += list(e)[:m-1]
    v = {}
    bs = map(bin_strings, [m-2, m-1, m])
    for l in bs:
        for idx in l:
            v[idx] = 0
    for curb in [m, m-1, m-2]:
        if curb:
            for i in xrange(n):
                curpat = tuple(ce[i:i+curb])
                v[curpat] += 1

    def rvs(i):
        return pow(v[i], 2)

    def psi2(b):
        return pow(2.0, b) / n * sum(map(rvs, bin_strings(b))) - n
    psi2_m = psi2(m)
    psi2_m_1 = psi2(m-1)
    if m == 2:
        psi2_m_2 = 0.0
    else:
        psi2_m_2 = psi2(m-2)
    d_psi2_m = psi2_m - psi2_m_1
    d2_psi2_m = psi2_m - 2 * psi2_m_1 + psi2_m_2
    p_1 = 1 - igamc(pow(2, m-2), d_psi2_m / 2.0)  # BUG Wrong for 10b ex
    p_2 = 1 - igamc(pow(2, m-3), d2_psi2_m / 2.0)
    outstr = 'The Serial Test:\n'
    outstr += 'n = %d\n' % n
    outstr += 'm = %d\n' % m
    outstr += 'psi2_%d = %.6f; ' % (m, psi2_m)
    outstr += 'psi2_%d = %.6f; ' % (m-1, psi2_m_1)
    outstr += 'psi2_%d = %.6f\n' % (m-2, psi2_m_2)
    outstr += 'd_psi2_%d = %.6f; ' % (m, d_psi2_m)
    outstr += 'd2_psi2_%d = %.6f\n' % (m, d2_psi2_m)
    outstr += 'P-value_1 = %.6f; ' % p_1
    outstr += 'P-value_2 = %.6f\n' % p_2
    open("./test_results/Serial.txt", "w").write(outstr)
    if p_1 < 0.01 or p_2 < 0.01:
        return False
    else:
        return True
