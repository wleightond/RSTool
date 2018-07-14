# RSTool

## CLI version of RSTool:

```
$ ./rt-cli.py datafile [options]

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
```


## GUI version of RSTool

To run from source:
```
$ ./main.py
     OR
$ python2 main.py
```
It will automatically display the gui.

If running from command-line on a mac, and receiving a message like this one:

```
2017-12-26 20:32:27.202 Python[16186:378132] ApplePersistenceIgnoreState: Existing state will not be touched. New state will be written to /var/folders/mc/2h5qgmz151348hcvm9hsdsrh0000gn/T/org.python.python.savedState ```

It is not an error, but if you don't want it to appear, this command will do:
  defaults write org.python.python ApplePersistenceIgnoreState NO
