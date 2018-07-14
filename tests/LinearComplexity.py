# William Leighton Dawson
# Center for Cyber Security
# New York University - Abu Dhabi
# Implementation of the NIST Randomness Test Suite
# 10. The Linear Complexity Test

from helpers import LengthError, split_list, reprint
from cephes import igam as igamc
from sys import stderr
from array import array

verbose = True

def LinearComplexity(e):
    K = 6  # fixed value as per spec
    ce = list(e)
    n = len(ce)
    M = 1000
    N = n / M
    blocks = split_list(ce, M)
    v = array('i', [0 for i in xrange(7)])
    prevlen = 0
    outstr = "Linear Complexity Test:\n"
    outstr += "n = %d\n" % n
    outstr += "M = %d\n" % M
    outstr += "N = %d\n" % N
    run_test = True
    if N < 1:
        run_test = False
    else:
        pi_i = array('d', [0.010417, 0.03125, 0.125, 0.5, 0.25, 0.0625, 0.020833])
        for block_idx in xrange(N):
            block = blocks[block_idx]
            B = array('i', [0 for i in xrange(M)])
            C = array('i', [0 for i in xrange(M)])
            T = array('i', [0 for i in xrange(M)])
            L_i = 0
            m = -1
            d = 0
            C[0] = 1
            B[0] = 1
            # Determine linear complexity L_i (adapted from NIST testing code)
            for idx in xrange(M):
                d = block[idx]
                for i in xrange(1, L_i + 1):
                    d += C[i] * block[idx - i]  # NOTE ii is block index
                d = d % 2
                if d == 1:
                    T = list(C)
                    P = array('i', [0 for j in xrange(M)])
                    for j in xrange(M):
                        if B[j] == 1:
                            P[j + idx - m] = 1
                    C = [(C[i] + P[i]) % 2 for i in xrange(M)]
                    if L_i <= idx / 2.0:
                        L_i = idx + 1 - L_i
                        m = idx
                        B = [i for i in T]
            if verbose:
                prgstr = "%.1f" % (100.0 * block_idx / N) + '%'
                for i in xrange(len(prgstr), 5):
                    prgstr = '0' + prgstr
                reprint(prgstr, prevlen)
                prevlen = len(prgstr)
            if (M + 1) % 2 == 0:
                sn = -1
            else:
                sn = 1
            mu = M / 2.0
            mu += (9 + sn) / 36.0
            mu -= 1.0 / pow(2, M) * (M / 3.0 + 2.0 / 9.0)
            if M % 2 == 0:
                sn = 1
            else:
                sn = -1
            T_i = sn * (L_i - mu) + 2.0 / 9.0
            if T_i <= -2.5:
                v[0] += 1
            elif -2.5 < T_i <= -1.5:
                v[1] += 1
            elif -1.5 < T_i <= -0.5:
                v[2] += 1
            elif -0.5 < T_i <= 0.5:
                v[3] += 1
            elif 0.5 < T_i <= 1.5:
                v[4] += 1
            elif 1.5 < T_i <= 2.5:
                v[5] += 1
            else:
                v[6] += 1
        if verbose:
            prgstr = '100.0%\n'
            reprint(prgstr, prevlen)
        pre_Chi2_obs = []
        for i in xrange(K + 1):  # BUG
            term = pow((v[i] - N * pi_i[i]), 2) / (N * pi_i[i])
            pre_Chi2_obs.append(term)
        Chi2_obs = sum(pre_Chi2_obs)
        p = 1 - igamc(K / 2.0, Chi2_obs / 2.0)
        for i in range(7):
            outstr += "v_%d = %d; " % (i, v[i])
        outstr += "\n"
        outstr += "Chi^2_obs = %.6f\n" % Chi2_obs
        outstr += "P-value = %.6f\n" % p
    if not run_test:
        outstr += 'Test not run: pre-test condition not met: '
        outstr += 'N >= 1\n'
    open("./test_results/LinearComplexity.txt", "w").write(outstr)
    if run_test:
        if p < 0.01:
            return False
    return True
