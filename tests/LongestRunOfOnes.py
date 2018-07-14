# William Leighton Dawson
# Center for Cyber Security
# New York University - Abu Dhabi
# Implementation of the NIST Randomness Test Suite
# 4. Test for the Longest-Run-of-Ones in a Block

from helpers import LengthError, split_list, longest_run, pi_i
from cephes import igam as igamc
from sys import stderr


def LongestRunOfOnes(e):
    ce = list(e)
    n = len(ce)
    run_test = True
    outstr = "Test for the Longest Run of Ones in a Block:\n"
    outstr += "n = %d\n" % n
    if n < 128:
        run_test = False
    else:
        if n >= 750000:  # set constants & instantiate the v_i table
            M, K, N, iv = 10000, 6, 75, 10
            vt = {10: 0, 11: 0, 12: 0, 13: 0, 14: 0, 15: 0, 16: 0}
        elif n >= 6272:
            M, K, N, iv = 128, 5, 49, 4
            vt = {4: 0, 5: 0, 6: 0, 7: 0, 8: 0, 9: 0}
        else:  # 128 <= n < 6272
            M, K, N, iv = 8, 3, 16, 1
            vt = {1: 0, 2: 0, 3: 0, 4: 0}
        ce = ce[:n - (n % M)]  # discard bits that don't fit
        n = len(ce)
        block_list = split_list(ce, M)  # list of M-bit blocks
        runs = []
        for block in block_list:  # Tabulate freq.s of longest runs
            lr = longest_run(block)
            runs.append((block, lr))
            if lr in vt.keys():
                vt[lr] += 1
            elif lr < min(vt.keys()):
                vt[min(vt.keys())] += 1
            elif lr > max(vt.keys()):
                vt[max(vt.keys())] += 1
        pre_Chi2_l = []
        for i in xrange(K + 1):
            idx = iv + i
            num = pow((vt[idx] - N * pi_i[(K, M)][iv + i]), 2)
            den = float(N * pi_i[(K, M)][idx])
            pre_Chi2_l.append(num / den)
            Chi2_obs = sum(pre_Chi2_l)
            p = 1 - igamc(K / 2.0, Chi2_obs / 2.0)
        if n <= 256:
            outstr += "Blocks (& longest runs):"
            for i in xrange(len(runs)):
                (b, l) = runs[i]
                outstr += "  %s (%d)\t" % ("".join([str(c) for c in b]), l)
                if i % 2:
                    outstr += '\n'
        outstr += "V_i values:\n"
        for i in sorted(vt.keys()):
            outstr += "  V_%d = %d\n" % (i - iv, vt[i])
        outstr += "Chi2_obs = %.6f\n" % Chi2_obs
        outstr += "P-value = %.6f\n" % p
    if not run_test:
        outstr += 'Test not run: pre-test condition not met: '
        outstr += 'n >= 128\n'
    open("./test_results/LongestRunOfOnes.txt", "w").write(outstr)
    if run_test:
        if p < 0.01:
            return False
    return True
