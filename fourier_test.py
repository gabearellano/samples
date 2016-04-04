import fourier, sys

sys.setrecursionlimit(6000)

# note: the xrange function in Python uses an inclusive lower
# bound and an exclusive upper bound.
input_size = 20
print "----Now Running Test on Input Size 2^n, n =", input_size
sys.stdout.flush()
fourier.run_test(input_size)
print "----Testing over--------------------------"
