# William Leighton Dawson
# Center for Cyber Security
# New York University - Abu Dhabi
# Implementation of the NIST Randomness Test Suite
# 9. Maurer's "Universal Statistical" Test

from helpers import split_list, find_LQ
from math import log, sqrt, erfc
from sys import stderr

def Universal(e):
    ce = list(e)
    n = len(ce)
    L, Q, expectedValue, variance = find_LQ(n)
    K = int(n / L) - Q
    init_seg = split_list(ce[:Q * L], L)
    test_seg = split_list(ce[Q * L:(Q + K) * L], L)
    T = [int(0) for i in xrange(pow(2, L))]
    for i in xrange(Q):
        cur_block = ''.join([str(j) for j in init_seg[i]])
        cur_val = int(cur_block, 2)
        T[cur_val] = i
    f_n = 0
    for i in xrange(K):
        cur_block = ''.join([str(j) for j in test_seg[i]])
        cur_val = int(cur_block, 2)
        last_occurrence = T[cur_val]
        T[cur_val] = i
        distance = Q + i - last_occurrence
        f_n += log(distance, 2)
    s = f_n
    f_n /= K

    c = 0.7 - 0.8 / L + (4.0 + 32.0 / L) * pow(K, (-3.0 / L)) / 15.0
    sigma = c * sqrt(variance / K)
    p = erfc(abs((f_n - expectedValue) / (sqrt(2) * sigma)))  # BUG
    # QUESTION: Use sigma or variance in p?
    outstr = 'Maurer\'s "Universal Statistical" Test:\n'
    outstr += "n = %d, L = %d, Q = %d\n" % (n, L, Q)
    outstr += "Note: %d bits are discarded\n" % (n - (Q + K) * L)
    outstr += "c = %.6f, sigma = %.6f, K = %d, sum = %.6f\n" % (
                        c,        sigma,        K,      s)
    outstr += "f_n = %.6f, expectedValue = %.6f, variance = %.4f\n" % (
                        f_n,        expectedValue,        variance)
    outstr += "P-value = %.6f\n" % p
    open("./test_results/Universal.txt", "w").write(outstr)
    if p < 0.01:
        return False
    else:
        return True
