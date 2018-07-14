# William Leighton Dawson
# Center for Cyber Security
# New York University - Abu Dhabi
# Implementation of the NIST Randomness Test Suite
# 5. The Binary Matrix Rank Test

from math import floor, e as E
from helpers import LengthError
from helpers import forward_row_ops, backward_row_ops, make_matrix
from sys import stderr

def Rank(e):
    ce = list(e)
    n = len(ce)
    s = 32  # As per spec
    M = s
    Q = s
    N = int(floor(n / (M * Q)))
    run_test = True
    # if N < 38: # and not ignore_recommendations:
    #     raise LengthError()
    outstr = 'Binary Matrix Rank Test:\n'
    outstr += 'n = %d (%d bits discarded)\n' % (n, n - N * s * s)
    outstr += 'M = Q = %d\nN = %d\n' % (s, N)
    if N < 1:
        run_test = False
    else:
        blocks = []
        for i in xrange(N):
            blocks.append(make_matrix(ce[M * Q * i:M * Q * (i + 1)], s))
        # cblocks = list(blocks)
        ranks = []
        for block in blocks:
            forward_row_ops(block)
            backward_row_ops(block)
            rank = 0
            for row in block:
                if 1 in row:
                    rank += 1
            ranks.append(rank)
        F_M = 0
        F_Mminus1 = 0
        for rank in ranks:
            if rank == M:
                F_M += 1
            elif rank == M - 1:
                F_Mminus1 += 1

        Chi2_obs = (pow((F_M - 0.2888 * N), 2) / (0.2888 * N) +
                    pow((F_Mminus1 - 0.5776 * N), 2) / (0.5776 * N) +
                    pow((N - F_M - F_Mminus1 - 0.1336 * N), 2) / (0.1336 * N))
        p = pow(E, (Chi2_obs / -2.0))
        
        outstr += 'F_M = %d\nF_Mminus1 = %d\n' % (F_M, F_Mminus1)
        outstr += 'Chi2_obs = %.6f\nP-value = %.6f\n' % (Chi2_obs, p)
    if not run_test:
        outstr += 'Test not run: pre-test condition not met: '
        outstr += 'Too few bits for a %dx%d matrix\n' % (M, Q)
    open("./test_results/Rank.txt", "w").write(outstr)
    if run_test:
        if p < 0.01:
            return False
    return True
