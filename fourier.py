"""
Author:Gabriel R. Arellano (garellano88@gmail.com)

A module I created for a programming project that can execute a
Discrete Fourier Transformation (DFT) or a Fast Fourier Transformation
(FFT) algorithm, provided polynomials (in the form of vectors) as
input.  I also have a method for multiplying polynomials using either
DFT or FFT methods.

"""

import math, random, time, sys, gc
import timeDict

__DEBUG=False
__DEMO_MODE=True

##########################################################
###### IMPORTANT METHODS #################################
##########################################################

__optimal_threshold = 2**6

def optimalFT(a_list):
    """
    The optimalFT method accepts a list of coefficients and determines
    if the size of the list is suitable for either a Fast Fourier
    Transformation, or a less than optimal Discrete Fourier
    Transformation, which is determined by the global variable,
    __optimal_threshold.

    Essentially, this method is just a wrapper for calling my
    implementations of Fourier transformations depending on the input
    size.
    """
    list_length = len(a_list)
    if list_length <= __optimal_threshold:
        return performDFT(a_list)
    else:
        return optimal_recursiveFFT(a_list)

def run_test(input_size):
    """
    The run_test method will generate random lists and perform tests
    using the optimalFT method. Timing measurements are made and
    results are printed between timings/tests.
    """
    global __optimal_threshold 
    print "----Now running 5 tests"
    # note: the xrange function in Python uses an inclusive lower
    # bound and an exclusive upper bound.
    for i in xrange(1,6):
        print "----Now running test", i
        current_list = gen_random_list(2**input_size)
        for current_threshold in xrange(3,input_size if input_size < 12 else 11):
            __optimal_threshold = 2**current_threshold
            start_time = time.time()
            optimalFT(current_list)
            end_time = time.time()
            total_time = end_time - start_time
            print "Total_time,threshold_size,n:", \
                repr(total_time)+ \
                ","+str(current_threshold) + \
                ","+str(i)
            sys.stdout.flush()
        current_list = None
        gc.collect()
   
## variable for keeping track of times. For class definition please
## see timeDict.py
td = timeDict.TimeDict()

def optimal_recursiveFFT(a_list):
    """
    The recursiveFFT method is a direct implementation of the
    RECURSIVE-FFT method defined in our class text, Intro to
    Algorithms (Cormen and Lee). I used a couple helper methods as a
    difference, however.

    For example, the book has a sequence definition to split the
    passed list into odd and even indices, while I use a method I
    designed called unzip_list().

    Also, in the book, they use a running value for omega and the
    related roots of unity, so that they do not have to recalculate
    the root of unity each time through the for loop. I instead
    recalculate it, as the calculation only involves less than a dozen
    lines of code.
    """
    n = len(a_list)
    if n == 1:
        return a_list
    # if __DEBUG:
    #     print "size of list:", n
    (a_list0, a_list1) = unzip_list(a_list)
    y_list0 = optimalFT(a_list0)
    y_list1 = optimalFT(a_list1)
    # if __DEBUG:
    #     print "y_list0:", str(y_list0)
    #     print "y_list1:", str(y_list1)
    y = {}
    # the following for loop's definition is slightly different from
    # the book - I use n/2 instead of n/2 - 1. This is because
    # Python's xrange() uses the upper bound on the list as an
    # exclusive limit.
    for k in xrange(n/2):
        # if __DEBUG:
        #     print "on loop iteration:", k
        w_basen_powerk = getRoU(n, k) # omega_n ^k
        # if __DEBUG:
        #     print "omega base", n, "power", k, ":", w_basen_powerk
        y[k] = sanitize_value(y_list0[k] + \
                        (w_basen_powerk * y_list1[k]))
        y[k+(n/2)] = sanitize_value(y_list0[k] - \
                        (w_basen_powerk * y_list1[k]))
    # if __DEBUG:
    #     print "printing array y:", str(y)
    
    # the return variable uses list comprehension to create a list of
    # values from a dict of keys mapped to values in python. The list
    # comprehension translates roughly to: taking the second item from
    # every item in the entire dict, if each element was converted to
    # a 2-tuple consisting of (key, value), which is what .items() does.
    return_me = [x[1] for x in y.items()]
    return return_me

def timed_recursiveFFT(a_list):
    global td
    time0 = time.time()
    n = len(a_list)
    if n == 1:
        return a_list
    # if __DEBUG:
    #     print "size of list:", n
    (a_list0, a_list1) = unzip_list(a_list)
    time1 = time.time()
    y_list0 = recursiveFFT(a_list0)
    y_list1 = recursiveFFT(a_list1)
    # if __DEBUG:
    #     print "y_list0:", str(y_list0)
    #     print "y_list1:", str(y_list1)
    time2 = time.time()
    y = {}
    # the following for loop's definition is slightly different from
    # the book - I use n/2 instead of n/2 - 1. This is because
    # Python's xrange() uses the upper bound on the list as an
    # exclusive limit.
    for k in xrange(n/2):
        # if __DEBUG:
        #     print "on loop iteration:", k
        w_basen_powerk = getRoU(n, k) # omega_n ^k
        # if __DEBUG:
        #     print "omega base", n, "power", k, ":", w_basen_powerk
        y[k] = sanitize_value(y_list0[k] + \
                        (w_basen_powerk * y_list1[k]))
        y[k+(n/2)] = sanitize_value(y_list0[k] - \
                        (w_basen_powerk * y_list1[k]))
    # if __DEBUG:
    #     print "printing array y:", str(y)
    
    # the return variable uses list comprehension to create a list of
    # values from a dict of keys mapped to values in python. The list
    # comprehension translates roughly to: taking the second item from
    # every item in the entire dict, if each element was converted to
    # a 2-tuple consisting of (key, value), which is what .items() does.
    return_me = [x[1] for x in y.items()]
    time3 = time.time()
    td.add(time0, time1, time2, time3, n)
    return return_me

def get_time_dict():
    global td
    return td

def recursive_inverseFFT(y_list):
    """
    The recursive_inverseFFT method is just that - the inverse of the
    recursiveFFT() method. The modifications from recursiveFFT() are
    as follows:

    - Swapped all instances of a and y
    - Replaced omega_n with omega_n^-1
    - Divided each element of the result by n
    """
    n = len(y_list)
    if n == 1:
        return y_list[0]
    (y_list0, y_list1) = unzip_list(y_list)
    a_list0 = recursiveFFT(y_list0)
    a_list1 = recursiveFFT(y_list1)
    a = {}
    # the following for loop's definition is slightly different from
    # the book - I use n/2 instead of n/2 - 1. This is because
    # Python's xrange() uses the upper bound on the list as an
    # exclusive limit.
    for k in xrange(n/2):
        w_basen_powerk = getRoU(n, -k) # omega_n ^k
        a[k] = sanitize_value((a_list0[k] + \
                            (w_basen_powerk * a_list1[k])) / n)
        a[k+(n/2)] = sanitize_value((a_list0[k] - \
                            (w_basen_powerk * a_list1[k])) / n)
    # the return statement uses list comprehension to create a list of
    # values from a dict of keys mapped to values in python. The list
    # comprehension translates roughly to: taking the second item from
    # every item in the entire dict, if each element was converted to
    # a 2-tuple consisting of (key, value), which is what .items() does.
    return [x[1] for x in a.items()]


def multiply_polynomials(polynom1, polynom2):
    """
    The multiply_polynomials method accepts two polynomials as
    parameters and multiplies them by using the FFT on each of them,
    multiplying the resulting point values, and using the inverse FFT
    on the resulting vector to retrieve the final product of both
    polynomials.

    Please note that the polynomials are provided in the form of a
    list, with the elements of the list being the coefficients of each
    factor, starting with the constant (a_0), all the way up to the
    coefficient of the highest power factor (a_(n-1)).
    """
    if __DEMO_MODE:
        print "Multiplying the following polynomials represented by lists of coefficients (recursive FFT method):"
        print "Polynomial 1:", str(polynom1)
        print "Polynomial 2:", str(polynom2)
    fft_poly1 = recursiveFFT(polynom1)
    fft_poly2 = recursiveFFT(polynom2)
    product_vector = multiply_point_values(fft_poly1, fft_poly2)
    resultant_vector = recursive_inverseFFT(product_vector)
    ##print "in multiple polyunomials, returning:", str(resultant_vector)
    return resultant_vector


##########################################################
###### HELPER METHODS ####################################
##########################################################

def getRoU(base, power):
    """
    The getRoU method (or the get Root of Unity method) will accept a
    base and a power and compute the value of the root of unity given
    those parameters.
    """
    ## no matter what the base is, if the power is zero, then the
    ## value that should be returned is 1.
    if not power:
        return 1
    ## use of the modulo operator changes the resulting power to
    ## be between 0 and the base.
    power = power % base
    if not power:
        return 1
    ## the following if statement will divide the base and power
    ## further if the power is a common factor.
    if not base % power:
        ## then base is perfectly divisible by the power, divide
        ## both by power
        base = base / power
        power = 1 ## equals 1 because power/power=1
    current_angle = math.radians((360/base) * power)
    ## in python, imaginary numbers are represented with a j after the
    ## digit, and are multiples of i plus a constant, so the imaginary
    ## number i must be represented as (0+1j), with parentheses and
    ## the constant included, always.
    value = math.cos(current_angle) + \
            ((0+1j)*math.sin(current_angle))
    return value


def unzip_list(list_of_coefficients):
    """
    The unzip_list method accepts a list of coeffieicnts and splits
    this list into two lists, one list with the even indices from the
    passed list, and the other with the odd indices.

    I was helped by the following web site in writing the code for
    splitting the list into even/odd indices using map:
    http://desk.stinkpot.org:8080/tricks/index.php/2007/10/extract-odd-or-even-elements-from-a-python-list/
    """
    even_indices = map(lambda i: list_of_coefficients[i], 
              filter(lambda i: i%2 == 0, range(len(list_of_coefficients))))
    odd_indices = map(lambda i: list_of_coefficients[i], 
              filter(lambda i: i%2 == 1, range(len(list_of_coefficients))))
    return (even_indices, odd_indices)

def sanitize_value(value):
    """
    The following method was created because python has a funny way of
    evaluating complex numbers. I would get a very small fraction
    attached to values that should have just been rounded off, so I
    check to see if the results should be integers and round off
    appropriately.
    """
    if __DEBUG:
        print "value:", value
        if type(value) == type(1j): ##check if value is complex
            print "diff real:", math.fabs(value.real - int(value.real))
            print "diff real bool:", str(math.fabs(value.real - int(value.real)) < 1e-12)
            print "diff imag:", math.fabs(value.imag - int(value.imag))
            print "diff imag bool:", str(math.fabs(value.imag - int(value.imag)) < 1e-12)
        else:
            print "only diff:", math.fabs(value - int(value))
    if type(value) == type(1j): ##check if value is complex
        # round down small values like 1.223e-12 or 1.28346e-17
        if math.fabs(value.imag - int(value.imag)) < 1e-12:
            value = complex(value.real, int(value.imag))
        if math.fabs(value.real - int(value.real)) < 1e-12:
            value = complex(int(value.real), value.imag)
        # also round up values like 5.9999999 or -5.999999
        if 1 - math.fabs(value.real - int(value.real)) < 1e-12:
            if value.real > 0:
                value = complex(int(value.real)+1, value.imag)
            if value.real < 0:
                value = complex(int(value.real)-1, value.imag)
        if 1 - math.fabs(value.imag - int(value.imag)) < 1e-12:
            if value.imag > 0:
                value = complex(value.real, int(value.imag) + 1)
            if value.imag < 0:
                value = complex(value.real, int(value.imag) - 1)
    else:
        if math.fabs(value - int(value)) < 1e-12:
            value = int(value)
    return value

def multiply_point_values(list1, list2):
    """
    The multiply_point_values method will accept two lists of point
    values, and will multiply each element of both lists (where the
    product is based on the matching indices from each list), saving
    each product in a new list. This new list of products is then
    returned.

    I am assuming that the input to multiplying polynomials will be
    lists of equal size, but I included a method to pad out the lists
    in case lists of unequal sizes are provided.
    """
    list1len = len(list1)
    list2len = len(list2)
    if list1len != list2len:
        print "Lists are of unequal length. Buffering smaller list with zeroes."
        zeroes_to_add = max(list1len, list2len) - min(list1len, list2len)
        if min(list1len, list2len) == list1len:
            for i in xrange(zeroes_to_add):
                list1.insert(0,0) ##insert a zero at the front of the
                                  ##list
        else:
            for i in xrange(zeroes_to_add):
                list2.insert(0,0)
        if len(list1) == len(list2):
            print "sucessfully padded list"
        else:
            print "failed to pad list"
    resultant_list = []
    for i in xrange(len(list1)): ## which is also len(list2)
        resultant_list.append(list1[i] * list2[i])
    return resultant_list

def gen_random_list(list_size):
    """
    The gen_random_list method will create a list of random numbers of
    length of the size passed as an argument. The numbers within the
    list will be between [-20, 20].
    """
    random_list = []
    for i in xrange(list_size):
        random_list.append(random.randint(-20, 20))
    return random_list


##########################################################
###### DFT METHODS #######################################
##########################################################

def performDFT(list_of_coefficients):
    """
    The performDFT method accepts a list of coefficients and computes
    a list of point values to return.
    """
    y_point_values = []
    for i in xrange(len(list_of_coefficients)):
        y_point_values.append(gety(i, list_of_coefficients))
    ##print "in DFT, returning:", str(y_point_values)
    return y_point_values

def perform_inverse_dft(list_of_ys):
    """
    The perform_inverse_dft method accepts a list of point values and
    returns a list of computed coefficients that relate to the point
    values.
    """
    coefficients = []
    for i in xrange(len(list_of_ys)):
        coefficients.append(geta(i, list_of_ys))
    ##print "in inverse DFT, returning:", str(coefficients)
    return coefficients


def gety(y_base, list_of_coefficients):
    """
    The gety method accepts a base for the desired y and a list of
    coeeficients to compute the desired y_base. In the formula
    provided with this assignment, y_base is equivalent to k.
    """
    unity_root = len(list_of_coefficients)
    pwr = math.log(unity_root, 2)
    if 2**pwr != unity_root:
        print "List provided is not a power of 2 in length,", \
            "output may be incorrect."
    y = 0
    ## xrange will iterate over all integers 0 to unity_root
    for j in xrange(unity_root): 
        y += list_of_coefficients[j] * getRoU(unity_root, (y_base*j))
    return sanitize_value(y)
    
def geta(a_base, list_of_ys):
    """
    The geta method does the inverse of the gety method and computes a
    coefficient provided base for the coefficient and a list of all y
    values. In the formula provided with this assignment, a_base is
    equivalent to k.
    """
    unity_root = len(list_of_ys)
    pwr = math.log(unity_root, 2)
    if 2**pwr != unity_root:
        print "List provided is not a power of 2 in length,", \
            "output may be incorrect."
    a = 0
    ## xrange will iterate over all integers 0 to unity_root
    for j in xrange(unity_root): 
        a += list_of_ys[j] * getRoU(unity_root, (-1*a_base*j))
    ##print "in geta, returning:", str(a/unity_root)
    return sanitize_value(a/unity_root)

def multiply_polynomialsDFT(polynom1, polynom2):
    """
    This method is the same as multiply_polynomials above, but uses
    the dft method of solving the problem.
    """
    if __DEMO_MODE:
        print "Multiplying the following polynomials represented by lists of coefficients (DFT method):"
        print "Polynomial 1:", str(polynom1)
        print "Polynomial 2:", str(polynom2)
    dft_poly1 = performDFT(polynom1)
    dft_poly2 = performDFT(polynom2)
    product_vector = multiply_point_values(dft_poly1, dft_poly2)
    resultant_vector = perform_inverse_dft(product_vector)
    ##print "in multiple polyunomials, returning:", str(resultant_vector)
    return resultant_vector

