#!/usr/bin/env python
# William Leighton Dawson
# Center for Cyber Security
# New York University - Abu Dhabi
# Implementation of the NIST Randomness Test Suite

import sys
from tests.helpers import read_data
from tests.Frequency import Frequency
from tests.BlockFrequency import BlockFrequency
from tests.Runs import Runs
from tests.LongestRunOfOnes import LongestRunOfOnes
from tests.Rank import Rank
from tests.DiscreteFourierTransform import DiscreteFourierTransform
from tests.NonOverlappingTemplateMatching import NonOverlappingTemplateMatching
from tests.OverlappingTemplateMatching import OverlappingTemplateMatching
from tests.Universal import Universal
from tests.LinearComplexity import LinearComplexity
from tests.Serial import Serial
from tests.ApproximateEntropy import ApproximateEntropy
from tests.CumulativeSums import CumulativeSums
from tests.RandomExcursions import RandomExcursions
from tests.RandomExcursionsVariant import RandomExcursionsVariant


from time import time


ignore_recommendations = True
verbose = 1

usage = """Usage:
  rt-cli.py datafile [options]

Options:
  -h | --help                       - print this help
  -o | --output-file outfile        - specify output file for summary
  -f | --fast                       - all but Templates and Linear Complexity
  -s | --test-spec xxxxxxxxxxxxxxx  - x = 0 or 1, run test n if bit n is 1)
       --test-spec 000000010100000 (e.g.)
  -t | --timing                     - time each test
  Tests (for specifying a test without the full test spec):
    --frequency
    --block-frequency
    --runs
    --longest-run-of-ones
    --rank
    --discrete-fourier-transform
    --non-overlapping-template-matching
    --overlapping-template-matching
    --universal
    --linear-complexity
    --serial
    --approximate-entropy
    --cumulative-sums
    --random-excursions
    --random-excursions-variant

Examples:
  rt-cli.py mydata.bin -o testresults.txt  (all tests to file)
  rt-cli.py mydata.txt --fast
  rt-cli.py mydata.bin -s 111111101011111  (equiv. to --fast)

Developed by William Leighton Dawson with K.K. Pandian and Prof. Hoda Alkhzaimi
For NYU Abu Dhabi's Center for Cyber Security
"""

def put_out(s, verbose, outfile, noret=False):
    if verbose == 1:
        print s
    elif verbose == 2:
        sys.stderr.write(s + ['\n', ''][noret])
        with open(outfile, "a") as f:
            f.write(s + ['\n', ''][noret])

if len(sys.argv) > 1 and "-h" not in sys.argv and "--help" not in sys.argv:
    outfile = sys.argv[1]
else:
    print usage
    sys.exit(0)

funcmap = zip([
    Frequency,
    BlockFrequency,
    Runs,
    LongestRunOfOnes,
    Rank,
    DiscreteFourierTransform,
    Universal,
    Serial,
    ApproximateEntropy,
    CumulativeSums,
    RandomExcursions,
    RandomExcursionsVariant,
    NonOverlappingTemplateMatching,
    OverlappingTemplateMatching,
    LinearComplexity,  # VERY SLOW
],
    [
    "--frequency",
    "--block-frequency",
    "--runs",
    "--longest-run-of-ones",
    "--rank",
    "--discrete-fourier-transform",
    "--non-overlapping-template-matching",
    "--overlapping-template-matching",
    "--universal",
    "--linear-complexity",
    "--serial",
    "--approximate-entropy",
    "--cumulative-sums",
    "--random-excursions",
    "--random-excursions-variant",
])



# Check for invalid arguments
arglist = [j for (i, j) in funcmap] + [
    "-f", "--fast",
    "-s", "--test-spec",
    "-o", "--output-file",
    "-n", "--num-bits",
    "-t", "--timing"]
for arg in sys.argv[min(2, len(sys.argv)):]:
    if "-" in arg and arg not in arglist:
        sys.stderr.write("Invalid argument: %s\n" % arg)
        sys.stderr.write(usage)
        sys.exit(0)
hasargs = False
for arg in sys.argv[min(2, len(sys.argv)):]:
    if arg in arglist[:-2]:  # Specifies tests
        hasargs = True

funclist = []
if not hasargs:
    for func, tag in funcmap:
        funclist.append(func)


# Process binary setting if set
if "-s" in sys.argv or "--test-spec" in sys.argv:
    try:
        bitlist = []
        for i in sys.argv[sys.argv.index("--test-spec") + 1]:
            bitlist.append([0, 1][int(i)])
        flist = [i for (i, j) in funcmap]
        if len(bitlist) > len(flist):
            raise ValueError()
        for bit, func in zip(bitlist, flist):
            if bit:
                funclist.append(func)
    except:
        try:
            bitlist = []
            for i in sys.argv[sys.argv.index("-s") + 1]:
                bitlist.append([0, 1][int(i)])
            flist = [i for (i, j) in funcmap]
            if len(bitlist) > len(flist):
                raise ValueError()
            for bit, func in zip(bitlist, flist):
                if bit:
                    funclist.append(func)
        except:
            sys.stderr.write("Option '-s' requires a 15 bit binary number as an argument\n")
            sys.stderr.write(usage)
            sys.exit(0)

if "-n" in sys.argv or "--num-bits" in sys.argv:
    if "-n" in sys.argv:
        i = sys.argv.index("-n")
    else:
        i = sys.argv.index("--num-bits")
    try:
        lim = int(sys.argv[i + 1])
    except:
        print "Invalid argument: -n/--numbits requires an integer"
else:
    lim = 0


# Read in data
sys.stderr.write("File: %s\n" % outfile)
try:
    sys.stderr.write("Attempting to read data...\n")
    e = read_data(outfile)
    if lim:
        e = e[:lim]
except IOError:
    sys.stderr.write("File not found. Exiting...\n")
    sys.exit(0)
sys.stderr.write("Data read:\n")
out = "e = "
out += "".join([str(i) for i in e][:min(32, len(e))])
out += ["", "..."][len(e) > 32] + "\n"
sys.stderr.write(out + '\n')


# Process extras
specialset = False
for func, tag in funcmap:
    if tag in sys.argv:
        specialset = True
        if tag not in funclist:
            funclist.append(func)


# The very-short-cut (cut out the three long tests)
if "-f" in sys.argv or "--fast" in sys.argv:
    for func, tag in funcmap:
        if func != OverlappingTemplateMatching \
        and func != LinearComplexity \
        and func != NonOverlappingTemplateMatching:
            funclist.append(func)


# Handle output to file
if "-o" in sys.argv or "--output-file" in sys.argv:
    try:
        outfile = sys.argv[sys.argv.index("--output-file") + 1]
        verbose = 2
        with open(outfile, "w") as f:
            pass
    except ValueError:
        try:
            outfile = sys.argv[sys.argv.index("-o") + 1]
            verbose = 2
            with open(outfile, "w") as f:
                pass
        except:
            print "Option '-o' failed"
            sys.stderr.write(usage)
            sys.exit(0)

if "-t" in sys.argv or "--timing" in sys.argv:
    timing = True
else:
    timing = False

# Run tests
for func in funclist:
    start = time()
    put_out(func.__name__ + '():', verbose, outfile)
    try:
        if not func(e):
            put_out("The sequence is non-random.", verbose, outfile)
        else:
            put_out("The sequence is random.", verbose, outfile)
        t = time() - start
        if timing: put_out("%s(): %.2fs\n" % (func.__name__, t), verbose, outfile)
        print
    except Exception as err:
        t = (func, type(err).__name__, str(err))
        put_out("%s: %s: %s\n" % t, verbose, outfile)
